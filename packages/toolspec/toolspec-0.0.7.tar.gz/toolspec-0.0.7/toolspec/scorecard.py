# -*- coding: utf-8 -*-
from util import Concurrent
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import numpy as np

def fwd_select(data, var_list, target, var_initial=[], tol=0.05, var_max=20):
    current_formula = '%s ~ %s + 1' % (target, ' + '.join(var_initial))
    current_score = smf.logit(current_formula, data).fit().aic
    var_choice = var_initial
    var_remain = [var for var in var_list if var not in var_choice]
    while len(var_remain) > 0:
        score_list = []
        for var in var_remain:
            formula = '%s ~ %s + 1' % (target, ' + '.join(var_choice+[var]))
            try:
                lr_res = smf.logit(formula, data).fit(method='newton', maxiter=100, disp=0, tol=tol)
            except Exception as error:
                print('Skipped %s due to %s' % (var, error))
                continue
            score = lr_res.aic 
            converged = lr_res.mle_retvals['converged']
            if converged:
                score_list.append((var,score))
            else: 
                print('Skipped %s due to not converged' % var)
                continue
        if len(score_list) > 0:
            score_list.sort(ascending=True)
            best_var, best_score = score_list[0]
        else:
            break
        if best_score < current_score:
            var_choice.append(best_var)
            var_remain.remove(best_var)
            current_formula = '%s ~ %s + 1' % (target, ' + '.join(var_choice))
            current_score = best_score
            print('Added %s' % best_var)
            lr_res = smf.logit(current_formula, data).fit(method='newton', maxiter=100, disp=0, tol=tol)
            p_values = lr_res.pvalues
            p_over = p_values[p_values > tol]
            if p_over.shape[0] > 0:
                for name in p_over.index:
                    try:
                        var_choice.remove(name)
                        print('Removed %s due to PValue=%s' % (name, p_over[name]))
                    except ValueError:
                        continue
            model_params = lr_res.params
            negative = model_params[model_params < 0]
        else:
            break
        if len(var_choice) >= var_max:
            break
    formula = '%s ~ %s + 1' % (target, ' + '.join(var_choice))
    lr_res = smf.logit(formula, data).fit(method='newton', maxiter=100, disp=0, tol=tol)
    return lr_res

def bkwd_select(data, var_list, target, threshold=5):
    var_choice = var_list.copy()
    while 1:
        vif = [variance_inflation_factor(data[var_choice].values,i) for i in range(len(var_choice))]
        if max(vif) > threshold:
            var_drop = [var_choice[i] for i,value in enumerate(vif) if value == max(vif)][0]
            print('Removed %s' % var_drop)
            var_choice.drop(var_drop)
        else:
            break
    formula = '%s ~ %s + 1' % (target, ' + '.join(var_choice))
    lr_res = smf.logit(formula, data).fit()
    return lr_res

def raw2woe(raw_data, var_list, bin_tbl):
    woe_data = raw_data[var_list].copy()
    for var in tqdm(var_list):
        bin_var = bin_tbl[bin_tbl['var'] == var].copy()
        woe_data[var] = 0
        for i in range(bin_var.shape[0]):
            value = bin_var.iloc[i]
            woe_data[var] += (raw_data[var] > value['lbound']) * (raw_data[var] <= value['ubound']) * value['WOE']
    return woe_data

def createcard(lr_res, bin_tbl, score0=660, odds0=1/15, pdo=15, ascending=False):
    B = pdo / np.log(2) * (-1 if ascending == True else 1)
    A = score0 + B * np.log(odds0)
    model_params = lr_res.params
    model_vars = [var for var in model_params.index if var != 'Intercept']
    scorecard = pd.DataFrame()
    for var in model_vars:
        bin_var = bin_tbl[bin_tbl['var'] == var].copy()
        bin_var['score'] = - B * model_params[var] * bin_var['WOE']
        scorecard = scorecard.append(bin_var,ignore_index=True)
    min_score = scorecard.groupby(by='var',as_index=False)['score'].min()
    score_basic = A - B * model_params['Intercept']
    score_amort = (score_basic + min_score['score'].sum()) / min_score.shape[0]
    scorecard = scorecard.merge(min_score, how='inner', on='var', suffixes=('_org','_min'))
    scorecard['score'] = scorecard.eval('score_org - score_min + %f' % score_amort).round(0)
    return scorecard

def raw2score(raw_data, scorecard):
    raw_data['score'] = 0
    for i in range(scorecard.shape[0]):
        value = scorecard.iloc[i]
        raw_data['score'] += (raw_data[value['var']] > value['lbound']) * (raw_data[value['var']] <= value['ubound']) * value['score']
    return raw_data['score']

def scorebucket(X, y, lr_res, bins=20):
    model_params = lr_res.params
    ln_odds = (X * model_params).sum(axis=1)
    prob = 1 / (np.exp(-ln_odds)+1)
    prob.name = 'Prob'
    prob = pd.DataFrame(prob)
    prob['Target'] = y 
    prob.sort_values(by='Prob', ascending=False, inplace=True)
    prob['Rank'] = 1
    prob.Rank = prob.Rank.cumsum()
    prob['Bucket'] = pd.qcut(prob.Rank, bins)
    return prob

def ksdistance(prob):
    bucket = prob.groupby('Bucket',as_index=False)['Target'].agg({'Total':'count','Bad':'sum','BadRate':'mean'})
    bucket.drop('Bucket', axis=1, inplace=True)
    bucket.eval('Good = Total - Bad', inplace=True)
    bucket['CumTotal'] =bucket['Total'].cumsum()
    bucket['CumBad'] = bucket['Bad'].cumsum()
    bucket['CumGood'] = bucket['Good'].cumsum()
    bucket['PctCumTotal'] = bucket['CumTotal'] / bucket['CumTotal'].max()
    bucket['PctCumBad'] = bucket['CumBad'] / bucket['CumBad'].max()
    bucket['PctCumGood'] = bucket['CumGood'] / bucket['CumGood'].max()
    bucket['KS'] = bucket['PctCumBad'] - bucket['PctCumGood']
    bucket.eval('Lift = PctCumBad/PctCumTotal', inplace=True)
    metric_ks = bucket['KS'].max()
    bucket[['PctCumBad','PctCumGood','KS','Lift']].plot(style=['r','b','g','y'], xlim=[0,bucket.shape[0]], ylim=[0,1], title='KS Distance = %.4f' % metric_ks)
    plt.xlabel('Score Buckets')
    plt.ylabel('Pct Distribution')
    plt.show() 
    return metric_ks, bucket




