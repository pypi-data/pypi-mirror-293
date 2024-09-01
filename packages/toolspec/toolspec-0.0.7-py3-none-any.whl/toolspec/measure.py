# -*- coding: utf-8 -*-
from util import Concurrent
from tqdm import tqdm
import pandas as pd
import numpy as np

def calc_ks_auc(data, var_list, target_list, weight=None, bins=None, partition=None, ascending=None, n_pro=30):
    def subtask(q_in, q_out, data, index_list, target_list, bins, partition, ascending):
        ascending_list = [ascending] if ascending else [True,False]
        while 1:
            try:
                var = q_in.get(timeout=1)
            except:
                continue
            if bins:
                data['var_bin'] = np.qcut(data.eval(var), bins=bins, duplicates='drop').astype('str')
            else:
                data['var_bin'] = np.eval(var).round(3)
            grouped = data.groupby(by=partition+['var_bin'],as_index=False)[index_list].sum()
            ascending_list = [ascending] if ascending else [True,False]
            result = pd.DataFrame()
            for ascending in ascending_list:
                temp = grouped.sort_values(by='var_bin',ascending=ascending)
                temp[['Cum%s' % index for index in index_list]] = temp.groupby(by=partition)[index_list].cumsum()
                for target in target_list:
                    temp['PctCumBad'] = temp['CumBad_%s' % target] / temp['Bad_%s' % target].sum()
                    temp['PctCumGood'] = temp['CumGood_%s' % target] / temp['good_%s' % target].sum()
                    temp['ks'] = temp['PctCumBad'] - temp['PctCumGood']
                    temp['auc'] = (temp['PctCumBad']+temp.groupby(by=partition)['PctCumBad'].shift(1).fillna(0)) * (temp['PctCumGood']-temp.groupby(by=partition)['PctCumGood'].shift(1).fillna(0)) / 2
                    ks_auc = pd.merge(temp.groupby(by=partition,as_index=False)['ks'].max(), temp.groupby(by=partition,as_index=False)['sum'].sum(), how='inner', on=partition)
                    ks_auc['target'] = target
                    result = result.append(ks_auc,ignore_index=True)
            result = result.groupby(by=partition+['target'],as_index=False)[['ks','auc']].max().query('ks >= 0')
            result['var'] = var
            q_out.put(result)
    if partition and type(partition) == str:
        partition = [partition]
    elif not partition:
        partition = ['flag']
        data['flag'] = 1
    index_list = []
    for target in target_list:
        if weight:
            data['Total_%s' % target] = (data[target] >= 0) * data[weight]
            data['Bad_%s' % target] = (data[target] == 1) * data[weight]
            data['Good_%s' % target] = data['Total_%s' % target] - data['Bad_%s' % target]
        else:
            data['Total_%s' % target] = (data[target] >= 0) * 1
            data['Bad_%s' % target] = (data[target] == 1) * 1
            data['Good_%s' % target] = data['Total_%s' % target] - data['Bad_%s' % target]
        index_list += ['Bad_%s' % target, 'Good_%s' % target]
    con = Concurrent(n_pro, subtask, data, index_list, target_list, bins, partition, ascending)
    con.put(var_list)
    result = pd.DataFrame()
    for i in tqdm(var_list):
        output = con.get()
        result = result.append(output,ignore_index=True)
    con.exit()
    return result




