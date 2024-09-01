# -*- coding: utf-8 -*-
from util import Concurrent
from tqdm import tqdm
import pandas as pd
import numpy as np

def iv_binning(data, var_list, target, min_cnt=100, min_pct=0.05, min_gain=0.001, max_bins=10, weight=None, ascending=None, n_pro=30):
    def subtask(q_in, q_out, data, min_cnt, min_pct, min_gain, max_bins, ascending):
        while 1:
            try:
                var = q_in.get(timeout=1)
            except:
                continue
            data['value'] = data.eval(var).round(3)
            grouped = data.groupby(by='value',as_index=False)[['Total','Bad','Good']].sum()
            grouped['cutoff'] = (grouped['value'] + grouped['value'].shift(-1)) / 2
            intervals = []
            iv_list = [0]
            badrates = [grouped['Bad'].sum()/grouped['Total'].sum()]
            index = 0
            while index <= len(intervals):
                lbound = -np.inf if index == 0 else intervals[index-1]
                ubound = np.inf if index == len(intervals) else intervals[index]
                temp = grouped[(grouped['value'] > lbound) & (grouped['value'] < ubound)].sort_values(by='value',ascending=True)
                temp[['Total_1','Bad_1','Good_1']] = temp[['Total','Bad','Good']].cumsum()
                temp['Total_2'] = temp['Total'].sum() - temp['Total_1']
                temp['Bad_2'] = temp['Bad'].sum() - temp['Bad_1']
                temp['Good_2'] = temp['Good'].sum() - temp['Good_1']
                temp['PctTotal_1'] = temp['Total_1'] / grouped['Total'].sum()
                temp['PctTotal_2'] = temp['Total_2'] / grouped['Total'].sum()
                temp['PctBad_1'] = temp['Bad_1'] / grouped['Bad'].sum()
                temp['PctBad_2'] = temp['Bad_2'] / grouped['Bad'].sum()
                temp['PctGood_1'] = temp['Good_1'] / grouped['Good'].sum()
                temp['PctGood_2'] = temp['Good_2'] / grouped['Good'].sum()
                temp['Badrate_1'] = temp['Bad_1'] / temp['Total_1']
                temp['Badrate_2'] = temp['Bad_2'] / temp['Total_2']
                temp['IV_1'] = (temp['PctBad_1'] - temp['PctGood_1']) * np.log(temp['PctBad_1']/temp['PctGood_1'])
                temp['IV_2'] = (temp['PctBad_2'] - temp['PctGood_2']) * np.log(temp['PctBad_2']/temp['PctGood_2'])
                temp['gain'] = temp['IV_1'] + temp['IV_2'] - iv_list[index]
                temp = temp[(temp['Total_1'] >= min_cnt) & (temp['Total_2'] >= min_cnt)]
                temp = temp[(temp['PctTotal_1'] >= min_pct) & (temp['PctTotal_2'] >= min_pct)]
                temp = temp[(temp['gain'] >= min_gain) & (temp['gain'] < np.inf)]
                if ascending == True:
                    temp = temp[temp['Badrate_1'] <= temp['Badrate_2']]
                    if index > 0:
                        temp = temp[temp['Badrate_1'] >= badrates[index-1]]
                    if index < len(intervals):
                        temp = temp[temp['Badrate_2'] <= badrates[index+1]]
                elif ascending == False:
                    temp = temp[temp['Badrate_1'] >= temp['Badrate_2']]
                    if index > 0:
                        temp = temp[temp['Badrate_1'] <= badrates[index-1]]
                    if index < len(intervals):
                        temp = temp[temp['Badrate_2'] >= badrates[index+1]]
                if not temp.empty:
                    opt = temp.sort_values(by='gain',ascending=False).iloc[0]
                    intervals.insert(index,opt['cutoff'])
                    iv_list[index] = opt['IV_2']
                    iv_list.insert(index,opt['IV_1'])
                    badrates[index] = opt['Badrate_2']
                    badrates.insert(index,opt['Badrate_1'])
                else:
                    index += 1
            while len(intervals) + 1 > max_bins:
                iv_merge = []
                for index,cutoff in enumerate(intervals):
                    lbound = -np.inf if index == 0 else intervals[index-1]
                    ubound = np.inf if index == len(intervals)-1 else intervals[index+1]
                    temp = grouped[(grouped['value'] > lbound) & (grouped['value'] < ubound)].copy()
                    PctBad = temp['Bad'].sum() / grouped['Bad'].sum()
                    PctGood = temp['Good'].sum() / grouped['Good'].sum()
                    iv = (PctBad - PctGood) * np.log(PctBad/PctGood)
                    iv_merge.append(iv)
                gain_list = [(iv_list[i]+iv_list[i+1]-iv) for i,iv in enumerate(iv_merge)]
                index = [i for i,iv in enumerate(gain_list) if iv == min(gain_list)][0]
                _ = intervals.pop(index)
                _ = iv_list.pop(index)
                iv_list[index] = iv_merge[index]
            intervals.insert(0,-np.inf)
            intervals.append(np.inf)
            data['bucket'] = pd.cut(data['value'], intervals, include_lowest=True).astype('str')
            result = data.groupby(by='bucket',as_index=False)[['Total','Bad','Good']].sum()
            result['PctTotal'] = result['Total'] / result['Total'].sum()
            result['PctBad'] = result['Bad'] / result['Bad'].sum()
            result['PctGood'] = result['Good'] / result['Good'].sum()
            result['Badrate'] = result['Bad'] / result['Total']
            result['WOE'] = np.log(result['PctBad']/result['PctGood'])
            result['IV'] = (result['PctBad'] - result['PctGood']) * result['WOE']
            result['lbound'] = result['bucket'].apply(lambda x : round(float(x.split(',')[0].strip('(')),3))
            result['ubound'] = result['bucket'].apply(lambda x : round(float(x.split(',')[1].strip(']')),3))
            result['bucket'] = '(' + result['lbound'].astype('str') + ',' + result['ubound'].astype('str') + ']'
            result['bin'] = result.index + 1
            result['var'] = var
            q_out.put(result)
    if weight:
        if type(weight) == str:
            data['Total'] = (data[target] >= 0) * data[weight]
            data['Bad'] = (data[target] == 1) * data[weight]
        else:
            data['Total'] = (data[target] >= 0) * data[weight[0]]
            data['Bad'] = (data[target] == 1) * data[weight[1]]
    else:
        data['Total'] = (data[target] >= 0) * 1
        data['Bad'] = (data[target] == 1) * 1
    data['Good'] = data['Total'] - data['Bad']
    con = Concurrent(n_pro, subtask, data, min_cnt, min_pct, min_gain, max_bins, ascending)
    con.put(var_list)
    columns = ['var','bin','bucket','lbound','ubound','Total','Bad','Good','PctTotal','PctBad','PctGood','Badrate','WOE','IV']
    result = pd.DataFrame(columns=columns)
    for i in tqdm(var_list):
        output = con.get()
        result = result.append(output[columns],ignore_index=True)
    con.exit()
    iv_tbl = result.groupby(by='var',as_index=False)['IV'].agg({'bins':'count','IV':'sum'}).sort_values(by='IV',ascending=False)
    iv_tbl['order'] = - iv_tbl['IV']
    bin_tbl = result.merge(iv_tbl[['var','order']], how='inner', on='var').sort_values(by=['order','bin'],ascending=True).reset_index(drop=True)[columns]
    iv_tbl = iv_tbl[['var','bins','IV']]
    return iv_tbl, bin_tbl

def cart_binning(data, var_list, target, min_cnt=100, min_pct=0.05, min_gain=0.001, max_bins=10, weight=None, ascending=None, method='gini', n_pro=30):
    def subtask(q_in, q_out, data, min_cnt, min_pct, min_gain, max_bins, ascending, method):
        while 1:
            try:
                var = q_in.get(timeout=1)
            except:
                continue
            data['value'] = data.eval(var).round(3)
            mesh = pd.merge(data[['cnt','value']].drop_duplicates(), data[['cnt','target']].drop_duplicates(), how='inner', on='cnt')[['value','target']]
            grouped = mesh.merge(data.groupby(by=['value','target'],as_index=False)[['cnt','sum','sqr']].sum(), how='left', on=['value','target']).fillna(0)
            grouped.sort_values(by='value',ascending=True,inplace=True)
            grouped['cutoff'] = (grouped['value'] + grouped.groupby(by='target')['value'].shift(-1)) / 2
            temp = grouped.groupby(by='target',as_index=False)[['cnt','sum','sqr']].sum()
            temp['cnt_sqr'] = np.square(temp['cnt'])
            intervals = []
            if method == 'gini':
                perf_list = [1-temp['cnt_sqr'].sum()/np.square(temp['cnt'].sum())]
            elif method == 'variance':
                perf_list = [temp['sqr'].sum()-temp['cnt'].sum()*np.square(temp['sum'].sum()/temp['cnt'].sum())]
            mean_list = [grouped['sum'].sum()/grouped['cnt'].sum()]
            index = 0
            while index <= len(intervals):
                lbound = -np.inf if index == 0 else intervals[index-1]
                ubound = np.inf if index == len(intervals) else intervals[index]
                temp = grouped[(grouped['value'] > lbound) & (grouped['value'] < ubound)].copy()
                temp.sort_values(by='value',ascending=True,inplace=True)
                temp[['cnt_1','sum_1','sqr_1']] = temp.groupby(by='target')[['cnt','sum','sqr']].cumsum()
                temp['cnt_2'] = temp['cnt'].sum() - temp['cnt_1']
                temp['sum_2'] = temp['sum'].sum() - temp['sum_1']
                temp['cnt_sqr_1'] = np.square(temp['cnt_1'])
                temp['cnt_sqr_2'] = np.square(temp['cnt_2'])
                temp = temp.groupby(by='cutoff',as_index=False)[['cnt_1','cnt_2','sum_1','sum_2','sqr_1','sqr_2','cnt_sqr_1','cnt_sqr_2']].sum()
                temp['pct_1'] = temp['cnt_1'] / grouped['cnt'].sum()
                temp['pct_2'] = temp['cnt_2'] / grouped['cnt'].sum()
                temp['avg_1'] = temp['sum_1'] / temp['cnt_1']
                temp['avg_2'] = temp['sum_2'] / temp['cnt_2']
                if method == 'gini':
                    temp['gini_1'] = 1 - temp['cnt_sqr_1'] / np.square(temp['cnt_1'])
                    temp['gini_2'] = 1 - temp['cnt_sqr_2'] / np.square(temp['cnt_2'])
                    temp['gain'] = perf_list[index] - (temp['gini_1'] * temp['cnt_1'] + temp['gini_2'] * temp['cnt_2']) / grouped['cnt'].sum()
                elif method == 'variance':
                    temp['vari_1'] = temp['sqr_1'] - temp['cnt_1'] * np.square(temp['avg_1'])
                    temp['vari_2'] = temp['sqr_2'] - temp['cnt_2'] * np.square(temp['avg_2'])
                    temp['gain'] = perf_list[index] - (temp['vari_1'] + temp['vari_2'])
                temp = temp[(temp['cnt_1'] >= min_cnt) & (temp['cnt_2'] >= min_cnt)]
                temp = temp[(temp['pct_1'] >= min_pct) & (temp['pct_2'] >= min_pct)]
                temp = temp[(temp['gain'] >= min_gain) & (temp['gain'] < np.inf)]
                if ascending == True:
                    temp = temp[temp['avg_1'] <= temp['avg_2']]
                    if index > 0:
                        temp = temp[temp['avg_1'] >= mean_list[index-1]]
                    if index < len(intervals):
                        temp = temp[temp['avg_2'] <= mean_list[index+1]]
                elif ascending == False:
                    temp = temp[temp['avg_1'] >= temp['avg_2']]
                    if index > 0:
                        temp = temp[temp['avg_1'] <= mean_list[index-1]]
                    if index < len(intervals):
                        temp = temp[temp['avg_2'] >= mean_list[index+1]]
                if not temp.empty:
                    opt = temp.sort_values(by='gini',ascending=True).iloc[0]
                    intervals.insert(index, opt['cutoff'])
                    if method == 'gini':
                        perf_list[index] = opt['gini_2']
                        perf_list.insert(index, opt['gini_1'])
                    elif method == 'variance':
                        perf_list[index] = opt['vari_2']
                        perf_list.insert(index, opt['vari_1'])
                    mean_list[index] = opt['avg_2']
                    mean_list.insert(index, opt['avg_1'])
                else:
                    index += 1
            while len(intervals) + 1 > max_bins:
                perf_merge = []
                for index,cutoff in enumerate(intervals):
                    lbound = -np.inf if index == 0 else intervals[index-1]
                    ubound = np.inf if index == len(intervals)-1 else intervals[index+1]
                    temp = grouped[(grouped['value'] > lbound) & (grouped['value'] < ubound)].copy()
                    temp = temp.groupby(by='target',as_index=False)[['cnt','sum','sqr']].sum()
                    temp['cnt_sqr'] = np.square(temp['cnt'])
                    if method == 'gini':
                        gini = (1 - temp['cnt_sqr'].sum()/np.square(temp['cnt'].sum())) * temp['cnt'].sum() / grouped['cnt'].sum()
                        perf_merge.append(gini)
                    elif method == 'variance':
                        vari = temp['sqr'].sum()-temp['cnt'].sum()*np.square(temp['sum'].sum()/temp['cnt'].sum())
                        perf_merge.append(vari)
                gain_list = [(perf-perf_list[i]-perf_list[i+1]) for i,perf in enumerate(perf_merge)]
                index = [i for i,gain in enumerate(gain_list) if i == min(gain_list)][0]
                _ = intervals.pop(index)
                _ = perf_list.pop(index)
                perf_list[index] = perf_merge[index]
            intervals.insert(0,-np.inf)
            intervals.append(np.inf)
            data['bucket'] = pd.cut(data['value'], intervals, include_lowest=True).astype('str')
            grouped = data.groupby(by=['bucket','target'],as_index=False)[['cnt','sum','sqr']].sum()
            grouped['cnt_sqr'] = np.square(grouped['cnt'])
            result = grouped.groupby(by='bucket',as_index=False)[['cnt','sum','sqr','cnt_sqr']].sum()
            result['pct'] = result['cnt'] / result['cnt'].sum()
            result['avg'] = result['sum'] / result['cnt']
            result['gini'] = (1 - result['cnt_sqr']/np.square(result['cnt'])) * result['cnt'] / result['cnt'].sum()
            result['vari'] = result['sqr'] - result['cnt'] * np.square(result['avg'])
            result['lbound'] = result['bucket'].apply(lambda x : round(float(x.split(',')[0].strip('(')),3))
            result['ubound'] = result['bucket'].apply(lambda x : round(float(x.split(',')[1].strip(']')),3))
            result['bucket'] = '(' + result['lbound'].astype('str') + ',' + result['ubound'].astype('str') + ']'
            result['bin'] = result.index + 1
            result['var'] = var
            q_out.put(result)
    if weight:
        if type(weight) == str:
            data['cnt'] = (data[target] >= 0) * data[weight]
            data['sum'] = (data[target] >= 0) * data[weight] * data[target]
            data['sqr'] = (data[target] >= 0) * data[weight] * np.square(data[target])
        else:
            data['cnt'] = (data[target] >= 0) * data[weight[0]]
            data['sum'] = (data[target] >= 0) * data[weight[1]] * data[target]
            data['sqr'] = (data[target] >= 0) * data[weight[1]] * np.square(data[target])
    else:
        data['cnt'] = (data[target] >= 0) * 1
        data['sum'] = (data[target] >= 0) * data[target]
        data['sqr'] = (data[target] >= 0) * np.square(data[target])
    data['target'] = data.eval(target).round(3)
    con = Concurrent(n_pro, subtask, data, min_cnt, min_pct, min_gain, max_bins, ascending, method)
    con.put(var_list)
    columns = ['var','bin','bucket','lbound','ubound','cnt','pct','avg','gini','vari']
    result = pd.DataFrame(columns=columns)
    for i in tqdm(var_list):
        output = con.get()
        result = result.append(output[columns],ignore_index=True)
    con.exit()
    result['bins'] = 1
    perf_tbl = result.groupby(by='var',as_index=False)[['bins','gini','vari']].sum()
    if method == 'gini':
        perf_tbl = perf_tbl.sort_values(by='gini',ascending=True).reset_index(drop=True)
        perf_tbl['order'] = perf_tbl['gini']
    elif method == 'variance':
        perf_tbl = perf_tbl.sort_values(by='vari',ascending=True).reset_index(drop=True)
        perf_tbl['order'] = perf_tbl['vari']
    bin_tbl = result.merge(perf_tbl[['var','order']], how='inner', on='var').sort_values(by=['order','bin'],ascending=True).reset_index(drop=True)[columns]
    perf_tbl = perf_tbl[['var','bins','gini','vari']]
    return perf_tbl, bin_tbl

def bin_mean(data, bin_tbl, target_list):
    var_list = list(bin_tbl['var'].drop_duplicates())
    index_list = []
    for target in target_list:
        data['cnt_%s' % target] = (data[target] >= 0) * 1
        data['sum_%s' % target] = (data[target] >= 0) * data[target]
        index_list += ['cnt_%s' % target, 'sum_%s' % target]
    result = pd.DataFrame()
    for var in tqdm(var_list):
        bin_var = bin_tbl[bin_tbl['var'] == var].copy()
        data['bin'] = 0
        for i in range(bin_var.shape[0]):
            value = bin_var.iloc[i]
            data.loc[(data[var] > value['lbound']) & (data[var] < value['ubound']), 'bin'] = value['bin']
        grouped = data.groupby(by='bin',as_index=False)[index_list].sum()
        grouped['var'] = var
        result = result.append(grouped,ignore_index=True)
    for target in target_list:
        result['avg_%s' % target] = result['sum_%s' % target] / result['cnt_%s' % target]
    columns = ['var','bin'] + ['avg_%s' % target for target in target_list]
    result = bin_tbl.merge(result[columns], how='left', on=['var','bin'])
    return result

def bin_perf(data, bin_tbl, target_list):
    var_list = list(bin_tbl['var'].drop_duplicates())
    index_list = []
    for target in target_list:
        data['Total_%s' % target] = (data[target] >= 0) * 1
        data['Bad_%s' % target] = (data[target] == 1) * 1
        data['Good_%s' % target] = data['Total_%s' % target] - data['Bad_%s' % target]
        index_list += ['Total_%s' % target, 'Bad_%s' % target, 'Good_%s' % target]
    result = pd.DataFrame()
    for var in tqdm(var_list):
        bin_var = bin_tbl[bin_tbl['var'] == var].copy()
        data['bin'] = 0
        for i in range(bin_var.shape[0]):
            value = bin_var.iloc[i]
            data.loc[(data[var] > value['lbound']) & (data[var] < value['ubound']), 'bin'] = value['bin']
        grouped = data.groupby(by='bin',as_index=False)[index_list].sum()
        for target in target_list:
            grouped['PctBad_%s' % target] = grouped['Bad_%s' % target] / grouped['Bad_%s' % target].sum()
            grouped['PctGood_%s' % target] = grouped['Good_%s' % target] / grouped['Good_%s' % target].sum()
            grouped[['PctCumBad_%s' % target,'PctCumGood_%s' % target]] = grouped[['PctBad_%s' % target,'PctGood_%s' % target]].cumsum()
            grouped['WOE_%s' % target] = np.log(grouped['PctBad_%s' % target]/grouped['PctGood_%s' % target])
            grouped['IV_%s' % target] = grouped['WOE_%s' % target] * (grouped['PctBad_%s' % target] - grouped['PctGood_%s' % target])
            grouped['KS_%s' % target] = abs(grouped['PctCumBad_%s' % target]-grouped['PctCumGood_%s' % target])
            grouped['AUC_%s' % target] = (grouped['PctCumBad_%s' % target] + grouped['PctCumBad_%s' % target].shift(1).fillna(0)) * (grouped['PctCumGood_%s' % target] - grouped['PctCumGood_%s' % target].shift(1).fillna(0)) / 2
        grouped['var'] = var
        result = result.append(grouped,ignore_index=True)
    columns = ['var','bin']
    for index in ['WOE','IV','KS','AUC']:
        columns += ['%s_%s' % (index,target) for target in target_list]
    result = bin_tbl.merge(result[columns], how='left', on=['var','bin'])
    return result













