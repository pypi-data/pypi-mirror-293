# -*- coding: utf-8 -*-
from util import Concurrent
from tqdm import tqdm
import pandas as pd
import numpy as np

def single_cutting(data, var_list, target_list, counter, min_cnt=100, min_pct=0.05, min_gain=0.001, ascending=None, reverse=False, method='min_Gini'):
    data['cnt'] = (data[counter] >= 0) * 1
    index_list = ['cnt']
    for target in target_list:
        data['Total_%s' % target] = (data[target] >= 0) * 1
        data['Bad_%s' % target] = (data[target] == 1) * 1
        data['Good_%s' % target] = data['Total_%s' % target] - data['Bad_%s' % target]
        index_list += ['Total_%s' % target,'Bad_%s' % target,'Good_%s' % target]
    if method == 'min_Gini':
        total_list = [(1-np.square(data['Bad_%s' % target].sum()/data['Total_%s' % target].sum())-np.square(data['Good_%s' % target].sum()/data['Total_%s' % target].sum())) for target in target_list]
    elif method == 'min_Vari':
        total_list = [(data['Bad_%s' % target].sum()-data['Total_%s' % target].sum()*np.square(data['Bad_%s' % target].sum()/data['Total_%s' % target].sum())) for target in target_list]
    result = []
    for var in var_list:
        data['value'] = data.eval(var).round(3)
        grouped = data.groupby(by='value',as_index=False)[index_list].sum()
        grouped['cutoff'] = (grouped['value'] + grouped['value'].shift(-1)) / 2
        grouped[index_list] = grouped[index_list].cumsum()
        grouped['cnt_1'] = grouped['cnt']
        grouped['cnt_2'] = grouped['cnt'].max() - grouped['cnt']
        grouped['pct_1'] = grouped['cnt'] / grouped['cnt'].max()
        grouped['pct_2'] = 1 - grouped['pct_1']
        for target in target_list:
            grouped['PctBad_1_%s' % target] = grouped['Bad_%s' % target] / grouped['Bad_%s' % target].max()
            grouped['PctBad_2_%s' % target] = 1 - grouped['PctBad_1_%s' % target]
            grouped['PctGood_1_%s' % target] = grouped['Good_%s' % target] / grouped['Good_%s' % target].max()
            grouped['PctGood_1_%s' % target] = 1 - grouped['PctGood_1_%s' % target]
            grouped['PctTotal_1_%s' % target] = grouped['Total_%s' % target] / grouped['Total_%s' % target].max()
            grouped['PctTotal_2_%s' % target] = 1 - grouped['PctTotal_1_%s' % target]
            grouped['Badrate_1_%s' % target] = grouped['Bad_%s' % target] / grouped['Total_%s' % target]
            grouped['Badrate_2_%s' % target] = (grouped['Bad_%s' % target].max() - grouped['Bad_%s' % target]) / (grouped['Total_%s' % target].max() - grouped['Total_%s' % target])
            if method == 'min_Gini':
                grouped['Gini_1_%s' % target] = 1 - np.square(grouped['Badrate_1_%s' % target]) - np.square(1-grouped['Badrate_1_%s' % target])
                grouped['Gini_2_%s' % target] = 1 - np.square(grouped['Badrate_2_%s' % target]) - np.square(1-grouped['Badrate_2_%s' % target])
                grouped['Gini_%s' % target] = grouped['Gini_1_%s' % target] * grouped['PctTotal_1_%s' % target] + grouped['Gini_2_%s' % target] * grouped['PctTotal_2_%s' % target]
                grouped['gain_%s' % target] = total_list[target_list.index(target)] - grouped['Gini_%s' % target]
            elif method == 'min_Vari':
                grouped['Vari_1_%s' % target] = grouped['PctBad_1_%s' % target] - grouped['PctTotal_1_%s' % target] * np.square(grouped['Badrate_1_%s' % target])
                grouped['Vari_2_%s' % target] = grouped['PctBad_2_%s' % target] - grouped['PctTotal_2_%s' % target] * np.square(grouped['Badrate_2_%s' % target])
                grouped['Vari_%s' % target] = grouped['Vari_1_%s' % target] + grouped['Vari_2_%s' % target]
                grouped['gain_%s' % target] = total_list[target_list.index(target)] - grouped['Vari_%s' % target]
            elif method == 'max_IV':
                grouped['IV_1_%s' % target] = (grouped['PctBad_1'] - grouped['PctGood_1']) * np.log(grouped['PctBad_1']/grouped['PctGood_1'])
                grouped['IV_2_%s' % target] = (grouped['PctBad_2'] - grouped['PctGood_2']) * np.log(grouped['PctBad_2']/grouped['PctGood_2'])
                grouped['IV_%s' % target] = grouped['IV_1_%s' % target] + grouped['IV_2_%s' % target]
                grouped['gain_%s' % target] = grouped['IV_%s' % target]
            elif method == 'max_KS':
                grouped['KS_%s' % target] = abs(grouped['PctBad_1_%s' % target]-grouped['PctGood_1_%s' % target])
                grouped['gain_%s' % target] = grouped['KS_%s' % target]
        grouped['Badrate_1'] = grouped[['Badrate_1_%s' % target for target in target_list]].apply('mean',axis=1)
        grouped['Badrate_2'] = grouped[['Badrate_2_%s' % target for target in target_list]].apply('mean',axis=1)
        grouped['gain'] = grouped[['gain_%s' % target for target in target_list]].apply('max',axis=1)
        grouped = grouped[(grouped['gain'] >= min_gain) & (grouped['gain'] < np.inf)]
        if ascending == True:
            for target in target_list:
                grouped = grouped[grouped['Badrate_1_%s' % target] < grouped['Badrate_2_%s' % target]]
        elif ascending == False:
            for target in target_list:
                grouped = grouped[grouped['Badrate_1_%s' % target] > grouped['Badrate_2_%s' % target]]
        grouped[['cnt','pct']] = grouped[['cnt_1','pct_1']]
        if reverse == True:
            grouped.loc[grouped['Badrate_1'] > grouped['Badrate_2'], ['cnt','pct']] = grouped[['cnt_2','pct_2']]
        else:
            grouped.loc[grouped['Badrate_1'] < grouped['Badrate_2'], ['cnt','pct']] = grouped[['cnt_1','pct_1']]
        grouped = grouped[(grouped['cnt'] >= min_cnt) & (grouped['pct'] >= min_pct)]
        if not grouped.empty:
            opt = grouped.sort_values(by='gain',ascending=False).iloc[0]
            if reverse == (opt['Badrate_1'] <= opt['Badrate_2']):
                direction = '<'
                result.append([var,direction,opt['cutoff'],opt['gain'],opt['cnt'],opt['pct']]+list(['Badrate_1_%s' % target for target in target_list])+list(['Total_1_%s' % target for target in target_list]))
            else:
                direction = '>'
                result.append([var,direction,opt['cutoff'],opt['gain'],opt['cnt'],opt['pct']]+list(['Badrate_2_%s' % target for target in target_list])+list(['Total_2_%s' % target for target in target_list]))
    columns = ['var','direction','cutoff','gain','cnt','pct'] + ['Badrate_%s' % target for target in target_list] + ['Total_%s' % target for target in target_list]
    result = pd.DataFrame(columns=columns, data=result).sort_values(by='gain',ascending=False).reset_index(drop=True)
    return result

def rules_mining(data, var_list, target_list, benchmark, target_lift, counter, min_cnt=100, min_pct=0.05, min_gain=0.001, ascending=None, reverse=False, method='min_Gini', aggfunc='mean', initial_point=[], max_depth=3, n_pro=30):
    def subtask(q_in, q_out, data, var_list, target_list, benchmark, target_lift, counter, min_cnt, min_pct, min_gain, ascending, reverse, method, aggfunc):
        while 1:
            try:
                where_str = q_in.get(timeout=1)
            except:
                continue
            result = single_cutting(data.query(where_str) if where_str else data, var_list, target_list, counter, min_cnt=min_cnt, min_pct=min_pct, min_gain=min_gain, ascending=ascending, reverse=reverse, method=method)
            if where_str:
                result['rule'] = where_str + ' and ' + result['var'] + result['direction'] + result['cutoff'].astype('str')
            else:
                result['rule'] = result['var'] + result['direction'] + result['cutoff'].astype('str')
            for i,target in enumerate(target_list):
                result['lift_%s' % target] = result['Badrate_%s' % target] / benchmark[i] / target_lift[i]
            result['lift'] = result[['lift_%s' % target for target in target_list]].apply(aggfunc,axis=1)
            if reverse == True:
                result['lift'] = 1 / result['lift']
            q_out.put(result)
    input_list = initial_point if len(initial_point) > 0 else [None]
    con = Concurrent(n_pro, subtask, data, var_list, target_list, benchmark, target_lift, counter, min_cnt, min_pct, min_gain, ascending, reverse, method, aggfunc)
    columns = ['rule','lift'] + ['Badrate_%s' % target for target in target_list] + ['Total_%s' % target for target in target_list]
    rule_detail = pd.DataFrame(columns=columns)
    cur_depth = 0
    while cur_depth < max_depth:
        cur_depth += 1
        con.put(input_list)
        result = pd.DataFrame()
        for i in tqdm(input_list):
            output = con.get()
            result = result.append(output,ignore_index=True)
        if result.empty:
            break
        input_list = list(result['rule'])
        rule_detail = rule_detail.append(result.query('lift > 1')[columns],ignore_index=True)
    con.exit()
    rule_detail = rule_detail.sort_values(by='lift',ascending=False).reset_index(drop=True)
    rule_set = list(rule_detail['rule'])
    return rule_set

def rules_filter(data, rule_set, target_list, benchmark, target_lift, counter, min_cnt=100, min_pct=0.05, reverse=False, method='risk', aggfunc='mean', n_pro=30):
    def subtask(q_in, q_out, data, index_list, target_list, benchmark, target_lift, counter, min_cnt, min_pct, reverse, method, aggfunc):
        while 1:
            try:
                rule = q_in.get(timeout=1)
            except:
                continue
            values = data.query(rule)[index_list].sum()
            total_list = [values['Total_%s' % target] for target in target_list]
            if min(total_list) > 0 and values['cnt'] >= min_cnt and values['cnt']/cnt_tol >= min_pct:
                lift_list = [values['Bad_%s' % target]/values['Total_%s' % target]/benchmark[i]/target_lift[i] for i,target in enumerate(target_list)]
                lift = pd.DataFrame(columns='target',data=lift_list).agg(aggfunc)
                if reverse == True:
                    lift = (1/lift) if lift > 0 else np.inf
                if lift >= 1 and method == 'pct':
                    lift = values['cnt'] / min_cnt
            else:
                lift = 0
            q_out.put([rule,lift])
    data['cnt'] = (data[counter] >= 0) * 1
    index_list = ['cnt']
    for target in target_list:
        data['Total_%s' % target] = (data[target] >= 0) * 1
        data['Bad_%s' % target] = (data[target] == 1) * 1
        data['Good_%s' % target] = data['Total_%s' % target] - data['Bad_%s' % target]
        index_list += ['Total_%s' % target,'Bad_%s' % target,'Good_%s' % target]
    cnt_tol = data['cnt'].sum()
    def calculate(data, rule_set):
        con = Concurrent(n_pro, subtask, data, index_list, target_list, benchmark, target_lift, counter, min_cnt, min_pct, reverse, method, aggfunc)
        con.put(rule_set)
        result = []
        for i in tqdm(rule_set):
            output = con.get()
            result.append(output)
        con.exit()
        result = pd.DataFrame(columns=['rule','lift'], data=result)
        return result
    columns = ['cnt'] + ['Badrate_%s' % target for target in target_list] + ['Total_%s' % target for target in target_list]
    rule_detail = []
    rule_select = []
    rule_remain = rule_set.copy()
    data_select = pd.DataFrame(columns=data.columns)
    data_remain = data.copy()
    while len(rule_remain) > 0:
        result = calculate(data_remain, rule_set)
        if result.empty:
            break
        rule_best = result.sort_values(by='lift',ascending=False).iloc[0]
        rule_select.append(rule_best)
        rule_remain = list(result[result['lift'] >= 1]['rule'])
        data_select = data_select.append(data_remain.query(rule_best))
        data_remain = data_remain.loc[~data_remain.index.isin(data_remain.query(rule_best).index)]
        info_self = data.query(rule_best)[index_list].sum()
        info_gain = data_remain(rule_best)[index_list].sum()
        info_cum = data_select[index_list].sum()
        rule_detail.append([rule_best]+list(info_self[columns])+list(info_gain[columns])+list(info_cum[columns]))
    columns_all = ['rule']
    for index in ['self','gain','cum']:
        columns_all += ['%s_%s' % (index,column) for column in columns]
    rule_detail = pd.DataFrame(columns=columns_all, data=rule_detail)
    return rule_select, rule_detail


def spliting(data, var_list, target_list, counter, min_cnt=100, min_pct=0.05, min_gain=0.001, ascending=None, method='min_Gini', max_depth=3, n_pro=30):
    def subtask(q_in, q_out, data):
        while 1:
            try:
                where_str = q_in.get(timeout=1)
            except:
                continue
            result = single_cutting(data.query(where_str) if where_str else data, var_list, target_list, counter, min_cnt=100, min_pct=0.05, min_gain=0.001, ascending=None, reverse=False, method='min_Gini', if_both=True)
            q_out.put(result)
    con = Concurrent(n_pro, subtask, data)
    def calculate(input_list):
        con.put(input_list)
        result = pd.DataFrame()
        for i in tqdm(input_list):
            output = con.get()
            result = result.append(output,ignore_index=True)
        return result
    con.exit()
    input_list = [None]
    result = calculate(input_list)
    return result

def assigning():
    return








