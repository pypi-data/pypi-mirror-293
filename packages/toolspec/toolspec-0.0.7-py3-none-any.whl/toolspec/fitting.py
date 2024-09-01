# -*- coding: utf-8 -*-
from util import Concurrent
from tqdm import tqdm
import pandas as pd
import numpy as np

def define_index(data, counter, target_list, sample_weight):
    index_list = ['cnt']
    data['cnt'] = (data[counter] >= 0) * 1
    for target in target_list:
        index_list += ['cnt_%s' % target, 'sum_%s' % target]
        if target in sample_weight.keys():
            weight = sample_weight[target]
            if type(weight) == str:
                data['cnt_%s' % target] = (data[target] >= 0) * data[weight]
                data['sum_%s' % target] = (data[target] >= 0) * data[weight] * data[target]
            else:
                data['cnt_%s' % target] = (data[target] >= 0) * data[weight[0]]
                data['sum_%s' % target] = (data[target] >= 0) * data[weight[1]] * data[target]
        else:
            data['cnt_%s' % target] = (data[target] >= 0) * 1
            data['sum_%s' % target] = (data[target] >= 0) * data[target]
    return index_list

def evaluate_gap(data, target_list, target_min_dict, target_max_dict, target_weight, method):
    for target in target_list:
        data['avg_%s' % target] = data['sum_%s' % target] / data['cnt_%s' % target]
        data['gap_%s' % target] = 0
        if target in target_min_dict.keys():
            data['gap_%s' % target] += (data['avg_%s' % target] - target_min_dict[target]) * (data['avg_%s' % target] > target_min_dict[target])
        if target in target_max_dict.keys():
            data['gap_%s' % target] += (target_max_dict[target] - data['avg_%s' % target]) * (data['avg_%s' % target] < target_max_dict[target])
        data['gap_%s' % target] = data['gap_%s' % target] * (target_weight[target] if target in target_weight.keys() else 1)
    data['gap'] = data[['gap_%s' % target for target in target_list]].apply(method, axis=1)
    return data['gap']

def single_fitting(data, var, counter, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=None):
    target_list = list(target_min_dict.keys()) + [target for target in target_max_dict.keys() if target not in target_min_dict.keys()]
    index_list = define_index(data, counter, target_list, sample_weight)
    data['value'] = data.eval(var).round(3)
    grouped = data.groupby(by='value',as_index=False)[index_list].sum()
    ascending_list = [ascending] if ascending else [True, False]
    result = pd.DataFrame()
    for ascending in ascending_list:
        temp = grouped.sort_values(by='value',ascending=ascending)
        temp['cutoff'] = (temp['value'] + temp['value'].shift(-1)) / 2
        temp[index_list] = temp[index_list].cumsum()
        temp['gap'] = evaluate_gap(temp, target_list, target_min_dict, target_max_dict, target_weight, method)
        temp['direction'] = '<' if ascending == True else '>'
        result = result.append(temp,ignore_index=True)
    result = result[result['cnt'] >= cnt_req].sort_values(by='cnt',ascending=True).drop_duplicates(subset='direction',keep='first')
    result = result[-np.isnan(result['cutoff'])]
    cutoff = result.sort_values(by='gap',ascending=True).iloc[:1]
    cutoff['var'] = var
    return cutoff

def couple_fitting(data, var_couple, counter, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=None, pct_single=0):
    target_list = list(target_min_dict.keys()) + [target for target in target_max_dict.keys() if target not in target_min_dict.keys()]
    index_list = define_index(data, counter, target_list, sample_weight)
    var1, var2 = var_couple[1], var_couple[2]
    data['value1'] = data.eval(var1).round(3)
    data['value2'] = data.eval(var2).round(3)
    data['flag'] = 1
    mesh = pd.merge(data[['flag','value1']].drop_duplicates(), data[['flag','value2']].drop_duplicates(), how='inner', on=['flag'])[['value1','value2']]
    grouped = mesh.merge(data.groupby(by=['value1','value2'],as_index=False)[index_list].sum(), how='left', on=['value1','value2']).fillna(0)
    ascending_list = [(ascending,ascending)] if ascending else [(True,True),(True,False),(False,True),(False,False)]
    result = pd.DataFrame()
    for ascending in ascending_list:
        temp = grouped.sort_values(by='value1',ascending=ascending[0])
        temp['cutoff1'] = (temp['value1'] + temp.groupby(by='value2')['value1'].shift(-1)) / 2
        temp[index_list] = temp.groupby(by='value2')[index_list].cumsum()
        temp = temp.sort_values(by='value2',ascending=ascending[1])
        temp['cutoff2'] = (temp['value2'] + temp.groupby(by='value1')['value2'].shift(-1)) / 2
        temp[index_list] = temp.groupby(by='value1')[index_list].cumsum()
        temp1 = grouped.groupby(by='value1',as_index=False)['cnt'].sum()
        temp1.sort_values(by='value1',ascending=ascending[0],inplace=True)
        temp1['cnt'] = temp1['cnt'].cumsum()
        temp2 = grouped.groupby(by='value2',as_index=False)['cnt'].sum()
        temp2.sort_values(by='value2',ascending=ascending[1],inplace=True)
        temp2['cnt'] = temp2['cnt'].cumsum()
        temp = temp.merge(temp1, how='inner', on='value1', suffixes=('','_1')).merge(temp2, how='inner', on='value2', suffixes=('','_1'))
        temp['pct_1'] = (temp['cnt_2'] - temp['cnt']) / (grouped['cnt'].sum() - temp['cnt'])
        temp['pct_2'] = (temp['cnt_1'] - temp['cnt']) / (grouped['cnt'].sum() - temp['cnt'])
        temp['gap'] = evaluate_gap(temp, target_list, target_min_dict, target_max_dict, target_weight, method)
        temp['direction1'] = '<' if ascending[0] == True else '>'
        temp['direction2'] = '<' if ascending[1] == True else '>'
        result = result.append(temp,ignore_index=True)
    result = result[result['cnt'] >= cnt_req].sort_values(by='cnt',ascending=True).drop_duplicates(subset=['direction1','direction2','value1'],keep='first')
    result = result[(-np.isnan(result['cutoff1'])) & (-np.isnan(result['cutoff2']))]
    result = result[(result['pct_1'] >= pct_single) & (result['pct_2'] >= pct_single)]
    cutoff = result.sort_values(by='gap',ascending=True).iloc[:1]
    cutoff['var1'] = var1
    cutoff['var2'] = var2
    return cutoff

def multiple_fitting(data, var_list, counter, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=None, pct_single=0, var_min=5, var_max=10, min_gain=0, n_pro=30):
    def subtask(q_in, q_out, data, var_cutoff, counter, cnt_req, cnt_tol, target_min_dict, target_max_dict, sample_weight, target_weight, method, ascending, pct_single, var_min, var_max):
        while 1:
            try:
                input = q_in.get(timeout=1)
            except:
                continue
            data['flag'] = 1
            for var in var_cutoff.keys():
                if var not in input:
                    direciton, cutoff = var_cutoff[var]
                    data['flag'] = data['flag'] * ((data[var] < cutoff) if direction == '<' else (data[var] > cutoff))
            if len(input) == 1:
                var = input[0]
                cutoff = single_fitting(data.query('flag == 1'), var, counter, cnt_req, target_min_dict=target_min_dict, target_max_dict=target_max_dict, sample_weight=sample_weight, target_weight=target_weight, method=method, ascending=ascending)
            else:
                var_couple = (input[0],input[1])
                cutoff = couple_fitting(data.query('flag == 1'), var_couple, counter, cnt_req, target_min_dict=target_min_dict, target_max_dict=target_max_dict, sample_weight=sample_weight, target_weight=target_weight, method=method, ascending=ascending, pct_single=pct_single)
            var_num = len(set(list(var_cutoff.keys()+input)))
            cutoff['gap_adj'] = cutoff['gap'] + 10 * (cutoff['cnt'] - cnt_req) / cnt_tol + 100 * (var_min - var_num) * (var_num < var_min) + 100 * (var_num - var_max) * (var_num > var_max)
            q_out.put(cutoff)
    target_list = list(target_min_dict.keys()) + [target for target in target_max_dict.keys() if target not in target_min_dict.keys()]
    _ = define_index(data, counter, target_list, sample_weight)
    cnt_tol = data['cnt'].sum()
    var_cutoff = {}
    def calculate(input_list):
        con = Concurrent(n_pro, subtask, data, var_cutoff, counter, cnt_req, cnt_tol, target_min_dict, target_max_dict, sample_weight, target_weight, method, ascending, pct_single, var_min, var_max)
        con.put(input_list)
        result = pd.DataFrame()
        for i in tqdm(input_list):
            output = con.get()
            result = result.append(output,ignore_index=True)
        con.exit()
        return result
    gap_min = np.inf
    while 1:
        if len(var_cutoff) == 0:
            input_list = [(var,) for var in var_list]
        else:
            input_list = []
            var_list_1 = list(var_cutoff.keys())
            for i,var1 in enumerate(var_list_1):
                input_list += [(var1,var2) for j,var2 in enumerate(var_list_1) if j > i]
                input_list += [(var1,var2) for var2 in var_list if var2 not in var_list_1]
        result = calculate(input_list)
        if not result.empty:
            opt = result.sort_values(by='gap_adj',ascending=True).iloc[0]
            if opt['gap_adj'] > gap_min-min_gain:
                break
            gap_min = opt['gap_adj']
            if 'var' in opt.index:
                var_cutoff[opt['var']] = (opt['direction'],opt['cutoff'])
            else:
                var_cutoff[opt['var1']] = (opt['direction1'],opt['cutoff1'])
                var_cutoff[opt['var2']] = (opt['direction2'],opt['cutoff2'])
        else:
            break
    result = []
    for var in var_cutoff.keys():
        data['cnt1'] = data['cnt']
        for i in var_cutoff.keys():
            if i != var:
                direction, cutoff = var_cutoff[i]
                data['cnt1'] = data['cnt1'] * ((data[i] < cutoff) if direction == '<' else (data[i] > cutoff))
        direction, cutoff = var_cutoff[var]
        data['cnt2'] = data['cnt'] * (data[var] < cutoff) if direction == '<' else (data[var] > cutoff)
        pct_self = (data['cnt'].sum() - data['cnt2'].sum()) / (data['cnt'].sum() - data.eval('cnt1*cnt2').sum())
        pct_gain = (data['cnt1'].sum() - data.eval('cnt1*cnt2').sum()) / (data['cnt'].sum() - data.eval('cnt1*cnt2').sum())
        result.append([var,direction,cutoff,pct_self,pct_gain])
    var_cutoff = pd.DataFrame(columns=['var','direction','cutoff','pct_self','pct_gain'], data=result).sort_values(by='pct_gain',ascending=False).reset_index(drop=True)
    return var_cutoff

def merge_fitting(data, var_list, counter, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=None, var_min=5, var_max=10, min_gain=0, max_weight=1, step_list=[], n_pro=30):
    def subtask(q_in, q_out, data, var_list, counter, cnt_req, target_min_dict, target_max_dict, sample_weight, target_weight, method, ascending, var_min, var_max, max_weight):
        while 1:
            try:
                var_weight = q_in.get(timeout=1)
            except:
                continue
            formula = ' + '.join(['%s * %f' % (var_list[i],weight) for i,weight in enumerate(var_weight) if weight > 0])
            data['value'] = data.eval(formula).round(3)
            cutoff = single_fitting(data, 'value', counter, cnt_req, target_min_dict=target_min_dict, target_max_dict=target_max_dict, sample_weight=sample_weight, target_weight=target_weight, method=method, ascending=ascending)
            var_num = len([1 for weight in var_weight if weight > 0])
            gap_add = sum([(weight-max_weight) for weight in var_weight if weight > max_weight])
            cutoff['gap_adj'] = cutoff['gap'] + 10 * gap_add + 100 * (var_min - var_num) * (var_num < var_min) + 100 * (var_num - var_max) * (var_num > var_max)
            cutoff[var_list] = var_weight
            q_out.put(cutoff[['gap_adj']+var_list])
    con = Concurrent(n_pro, subtask, data, var_list, counter, cnt_req, target_min_dict, target_max_dict, sample_weight, target_weight, method, ascending, var_min, var_max, max_weight)
    def calculate(input_list):
        con.put(input_list)
        result = pd.DataFrame()
        for i in tqdm(input_list):
            output = con.get()
            result = result.append(output,ignore_index=True)
        return result
    input_list = [[(1 if i == var else 0) for i in var_list] for var in var_list]
    result_all = calculate(input_list)
    opt = result_all.sort_values(by='gap_adj',ascending=True).iloc[0]
    var_weight_best = list(opt[var_list])
    gap_min = opt['gap_adj']
    for step in step_list:
        while 1:
            var_sub_1 = [var_list[i] for i,weight in enumerate(var_weight_best) if weight > max_weight]
            var_sub_2 = [var_list[i] for i,weight in enumerate(var_weight_best) if weight >= step]
            var_sub = var_sub_1 if len(var_sub_1) > 0 else var_sub_2
            var_add = [var_list[i] for i,weight in enumerate(var_weight_best) if round(weight+step,2) <= max_weight]
            var_weight_cand = []
            for var1 in var_sub:
                for var2 in var_add:
                    if var1 != var2:
                        var_weight = var_weight_best.copy()
                        var_weight[var_list.index(var1)] = round(var_weight[var_list.index(var1)]-step,2)
                        var_weight[var_list.index(var2)] = round(var_weight[var_list.index(var2)]+step,2)
                        var_weight_cand.append(var_weight)
            var_weight_cand = list(pd.concat([result_all.eval('flag=1'), pd.DataFrame(columns=var_list, data=var_weight_cand).eval('flag=0')], axis=0).drop_duplicates(subset=var_list,keep='first').query('flag==0')[var_list])
            var_weight_cand = [list(var_weight) for var_weight in var_weight_cand]
            result = calculate(var_weight_cand)
            result_all = result_all.append(result,ignore_index=True)
            if result.empty:
                break
            opt = result.sort_values(by='gap_adj',ascending=True).iloc[0]
            if opt['gap_adj'] > gap_min-min_gain:
                break
            gap_min = opt['gap_adj']
            var_weight_best = list(opt[var_list])
    con.exit()
    var_choice = [var_list[i] for i,weight in enumerate(var_weight_best) if weight > 0]
    var_weight = [weight for weight in var_weight_best if weight > 0]
    return var_choice, var_weight

def grid_fitting(data, var_couple, counter, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=False, min_gain=0, only_gain=True):
    target_list = list(target_min_dict.keys()) + [target for target in target_max_dict.keys() if target not in target_min_dict.keys()]
    index_list = define_index(data, counter, target_list, sample_weight)
    var_x, var_y = var_couple[0], var_couple[1]
    data['bin_x'] = data[var_x].round(3)
    data['bin_y'] = data[var_y].round(3)
    bin_x = list(data['bin_x'].drop_duplicates().sort_values(ascending=ascending))
    bin_y = list(data['bin_y'].drop_duplicates().sort_values(ascending=ascending))
    mesh = pd.merge(pd.DataFrame({'bin_x':bin_x,'flag':1}), pd.DataFrame({'bin_y':bin_y,'flag':1}), how='inner', on='flag')[['bin_x','bin_y']]
    mesh = mesh.merge(data.groupby(by=['bin_x','bin_y'],as_index=False)[index_list].sum(), how='left', on=['bin_x','bin_y']).fillna(0)
    mesh.set_index(['bin_x','bin_y'])
    mesh['flag'] = 0
    choice = {}
    for index in index_list:
        choice[index] = 0
    border = []
    gap_min = np.inf
    while 1:
        if len(border) > 0:
            point_cand = []
            for i,j in enumerate(border):
                if i == 0 and j < len(var_y):
                    point_cand.append((i+1,j+1))
                elif i > 0 and j < border[i-1]:
                    point_cand.append((i+1,j+1))
            else:
                if i < len(bin_x) - 1:
                    point_cand.append((i+2,1))
        else:
            point_cand = [(1,1)]
        if len(point_cand) == 0:
            break
        cand = mesh.loc[[(bin_x[p[0]-1],bin_y[p[1]-1]) for p in point_cand]].reset_index()
        cand['gap_add'] = evaluate_gap(cand, target_list, target_min_dict, target_max_dict, target_weight, method)
        for index in index_list:
            cand[index] += choice[index]
        cand['gap_tol'] = evaluate_gap(cand, target_list, target_min_dict, target_max_dict, target_weight, method)
        if only_gain:
            opt = cand.sort_values(by='gap_add',ascending=True).iloc[0]
        else:
            opt = cand.sort_values(by='gap_tol',ascending=True).iloc[0]
        if min_gain >= 0 and opt['gap_tol'] > gap_min-min_gain:
            break
        gap_min = opt['gap_tol']
        point_x = bin_x.index(opt['bin_x']) + 1
        point_y = bin_y.index(opt['bin_y']) + 1
        if point_x <= len(border):
            border[point_x-1] = point_y
        else:
            border.append(point_y)
        for index in index_list:
            choice[index] = opt[index]
        mesh.loc[(opt['bin_x'],opt['bin_y']), 'flag'] = 1
        if min_gain < 0 and opt['cnt'] >= cnt_req:
            break
    cross_tab = pd.pivot_table(mesh, index='bin_x', columns='bin_y', values='flag')
    return cross_tab

def grid_grouping(data, var_couple, counter, tab_conf, sample_weight={}, target_weight={}, method='sum', ascending=False, reverse=False, min_gain=0, only_gain=True):
    target_min_list = [column.replace('min_','') for column in tab_conf.columns if 'min_' in column]
    target_max_list = [column.replace('max_','') for column in tab_conf.columns if 'max_' in column]
    target_list = target_min_list + [target for target in target_max_list if target not in target_min_list]
    tab_copy = tab_conf.sort_values(by='id',ascending=True)
    if reverse:
        index_list = [column for column in tab_copy.columns if 'min_' in column or 'max_' in column]
        for index in index_list:
            tab_copy[index] = tab_copy[index] * tab_copy['pct']
        tab_copy[index_list] = tab_copy[index_list].cumsum()
        tab_copy['pct'] = tab_copy['pct'].cumsum()
        for index in index_list:
            tab_copy[index] = tab_copy[index] / tab_copy['pct']
        tab_copy.sort_values(by='id',ascending=False,inplace=True)
    index_list = define_index(data, counter, target_list, sample_weight)
    cnt_tol = data['cnt'].sum()
    var_x, var_y = var_couple[0], var_couple[1]
    data['bin_x'] = data[var_x].round(3)
    data['bin_y'] = data[var_y].round(3)
    bin_x = list(data['bin_x'].drop_duplicates().sort_values(ascending=ascending))
    bin_y = list(data['bin_y'].drop_duplicates().sort_values(ascending=ascending))
    mesh = pd.merge(pd.DataFrame({'bin_x':bin_x,'flag':1}), pd.DataFrame({'bin_y':bin_y,'flag':1}), how='inner', on='flag')[['bin_x','bin_y']]
    mesh = mesh.merge(data.groupby(by=['bin_x','bin_y'],as_index=False)[index_list].sum(), how='left', on=['bin_x','bin_y']).fillna(0)
    mesh.set_index(['bin_x','bin_y'])
    mesh['id'] = 0
    border = []
    for i in range(tab_copy.shape[0]):
        value = tab_copy.iloc[i]
        id = value['id']
        cnt_req = int(cnt_tol*value['pct'])
        target_min_dict = {}
        for target in target_min_list:
            target_min_dict[target] = value['min_%s' % target]
        target_max_dict = {}
        for target in target_max_list:
            target_max_dict[target] = value['max_%s' % target]
        choice = {}
        for index in index_list:
            choice[index] = 0
        gap_min = np.inf
        while 1:
            if len(border) > 0:
                point_cand = []
                for i,j in enumerate(border):
                    if i == 0 and j < len(bin_y):
                        point_cand.append((i+1,j+1))
                    elif i > 0 and j < border[i-1]:
                        point_cand.append((i+1,j+1))
                else:
                    if i < len(bin_x) - 1:
                        point_cand.append((i+2,1))
            else:
                point_cand = [(1,1)]
            if len(point_cand) == 0:
                break
            cand = mesh.loc[[(bin_x[p[0]-1],bin_y[p[1]-1]) for p in point_cand]].reset_index()
            cand['gap_add'] = evaluate_gap(cand, target_list, target_min_dict, target_max_dict, target_weight, method)
            for index in index_list:
                cand[index] += choice[index]
            cand['gap_tol'] = evaluate_gap(cand, target_list, target_min_dict, target_max_dict, target_weight, method)
            if only_gain:
                opt = cand.sort_values(by='gap_add',ascending=True).iloc[0]
            else:
                opt = cand.sort_values(by='gap_tol',ascending=True).iloc[0]
            if min_gain >= 0 and opt['gap_tol'] > gap_min-min_gain:
                break
            gap_min = opt['gap_tol']
            point_x = bin_x.index(opt['bin_x']) + 1
            point_y = bin_y.index(opt['bin_y']) + 1
            if point_x <= len(border):
                border[point_x-1] = point_y
            else:
                border.append(point_y)
            for index in index_list:
                choice[index] = opt[index]
            mesh.loc[(opt['bin_x'],opt['bin_y']), 'id'] = id
            if min_gain < 0 and opt['cnt'] >= cnt_req:
                break
    cross_tab = pd.pivot_table(mesh, index='bin_x', columns='bin_y', values='id')
    grouped = mesh.groupby(by='id',as_index=False)[index_list].sum()
    grouped['pct_group'] = grouped['cnt'] / cnt_tol
    for target in target_list:
        grouped['avg_%s' % target] = grouped['sum_%s' % target] / grouped['cnt_%s' % target]
    grouped = tab_conf.merge(grouped[['id','pct_group']+['avg_%s' % target for target in target_list]], how='left', on='id')
    return grouped, cross_tab

def multiple_grouping(data, var_list, counter, tab_conf, sample_weight={}, target_weight={}, method='sum', ascending=False, pct_single=0, var_min=5, var_max=10, min_gain=0, reverse=False, n_pro=30):
    target_min_list = [column.replace('min_','') for column in tab_conf.columns if 'min_' in column]
    target_max_list = [column.replace('max_','') for column in tab_conf.columns if 'max_' in column]
    target_list = target_min_list + [target for target in target_max_list if target not in target_min_list]
    tab_copy = tab_conf.sort_values(by='id',ascending=True)
    if reverse == True:
        index_list = [column for column in tab_copy.columns if 'min_' in column or 'max_' in column]
        for index in index_list:
            tab_copy[index] = tab_copy[index] * tab_copy['pct']
        tab_copy[index_list] = tab_copy[index_list].cumsum()
        tab_copy['pct'] = tab_copy['pct'].cumsum()
        for index in index_list:
            tab_copy[index] = tab_copy[index] / tab_copy['pct']
        tab_copy.sort_values(by='id',ascending=False,inplace=True)
    index_list = define_index(data, counter, target_list, sample_weight)
    cnt_tol = data['cnt'].sum()
    data_remain = data.copy()
    result = pd.DataFrame()
    for i in range(tab_copy.shape[0]):
        value = tab_copy.iloc[i]
        cnt_req = int(cnt_tol*value['pct'])
        target_min_dict = {}
        for target in target_min_list:
            target_min_dict[target] = value['min_%s' % target]
        target_max_dict = {}
        for target in target_max_list:
            target_max_dict[target] = value['max_%s' % target]
        var_cutoff = multiple_fitting(data_remain, var_list, counter, cnt_req, target_min_dict=target_min_dict, target_max_dict=target_max_dict, sample_weight=sample_weight, target_weight=target_weight, method=method, ascending=ascending, pct_single=pct_single, var_min=var_min, var_max=var_max, min_gain=min_gain, n_pro=n_pro)
        data_remain['flag'] = 1
        for i in range(var_cutoff.shape[0]):
            value = var_cutoff.iloc[i]
            var, direction, cutoff = value['var'], value['direction'], value['cutoff']
            data_remain['flag'] = data_remain['flag'] * ((data_remain[var] < cutoff) if direction == '<' else (data_remain[var] > cutoff))
        if reverse == True:
            data_remain = data_remain.query('flag == 1')
        else:
            data_remain = data_remain.query('flag == 0')
        result = result.append(var_cutoff,ignore_index=True)
    cross_tab = pd.pivot_table(result, index='id', columns='var', values='cutoff')
    if reverse == True:
        cross_tab.sort_index(ascending=False,inplace=True)
        cross_tab = cross_tab.cummin() if ascending == True else cross_tab.cummax()
    cross_tab['region'] = cross_tab.apply(lambda x : ' and '.join(['%s %s %f' % (column,'<' if ascending == True else '>',x[column]) for column in cross_tab.columns if x[column] > 0]))
    cross_tab = cross_tab.reset_index().sort_values(by='id',ascending=True)
    data['id'] = 0
    for i in range(cross_tab.shape[0]):
        value = cross_tab.iloc[i]
        data.loc[(data['id'] == 0) & (data.index.isin(data.query(value['region']).index)), 'id'] = value['id']
    grouped = data.groupby(by='id',as_index=False)[index_list].sum()
    grouped['pct_group'] = grouped['cnt'] / cnt_tol
    for target in target_list:
        grouped['avg_%s' % target] = grouped['sum_%s' % target] / grouped['cnt_%s' % target]
    result = tab_conf.merge(grouped[['id','pct_group']+['avg_%s' % target for target in target_list]], how='left', on='id').merge(cross_tab, how='left', on='id')
    return result




