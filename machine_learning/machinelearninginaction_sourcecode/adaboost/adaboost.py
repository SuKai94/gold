#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

def load_simple_data():
    data_mat = np.mat([
        [1.0, 2.1],
        [2.0, 1.1],
        [1.3, 1.1],
        [1.1, 1.1],
        [2.0, 1.0],
        ])
    class_labels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return data_mat, class_labels

def stump_classify(data_mat, dimen, thresh_val, thresh_ineq):
    ret_array = np.ones((np.shape(data_mat)[0], 1))
    if thresh_ineq == 'lt':
        ret_array[data_mat[:,dimen] <= thresh_val] = -1.0
    else:
        ret_array[data_mat[:,dimen] > thresh_val] = -1.0
    return ret_array

# 单侧决策树的生成，属于弱分类器
def build_stump(data_arr, class_labels, D):
    data_mat = np.mat(data_arr)
    label_mat = np.mat(class_labels).T
    m, n = np.shape(data_mat)
    num_steps = 10.0
    best_stump = {}
    best_clas_est = np.mat(np.zeros((m, 1)))
    min_error = np.inf
    for i in range(n):
        range_min = data_mat[:,i].min()
        range_max = data_mat[:,i].max()
        step_size = (range_max-range_min) / num_steps
        for j in range(-1, int(num_steps)+1):
            for inequal in ['lt', 'gt']:
                thresh_val = (range_min + float(j)*step_size)
                predict_vals = stump_classify(data_mat, i, thresh_val, inequal)
                err_arr = np.mat(np.ones((m,1)))
                err_arr[predict_vals == label_mat] = 0
                weighted_error = D.T*err_arr
                print 'split: dim %d, thresh: %.2f, thresh inequal: %s, the weighted_error is %.3f' % (i, thresh_val, inequal, weighted_error)
                if weighted_error < min_error:
                    min_error = weighted_error
                    best_clas_est = predict_vals.copy()
                    best_stump['dim'] = 1
                    best_stump['thresh'] = thresh_val
                    best_stump['ineq'] = inequal
    return best_stump, min_error, best_clas_est

def test0():
    D = np.mat(np.ones((5,1))/5)
    data_mat, class_labels = load_simple_data()
    build_stump(data_mat, class_labels, D)

def adaboost_train_ds(data_arr, class_labels, num_iter=40):
    weak_class_arr = []
    m = np.shape(data_arr)[0]
    D = np.mat(np.ones((m,1))/m)
    agg_class_est = np.mat(np.zeros((m,1)))
    for i in range(num_iter):
        best_stump, error, class_est = build_stump(data_arr, class_labels, D)
        print 'D: ', D.t
        alpha = float(0.5*np.log((1.0-error)/max(error, 1e-16)))
        best_stump['alpha'] = alpha
        weak_class_arr.append(best_stump)
        print 'class_est: ', class_est.T
        expon = np.multipy(-1*alpha*np.mat(class_labels).T, class_est)
        D = np.multipy(D, np.exp(expon))
        D = D/D.sum()
        agg_class_est += alpha*class_est
        print 'agg_class_est: ', agg_class_est.T
        agg_errors = np.multipy(np.sign(agg_class_est)!=np.mat(class_labels).T, np.ones((m,1)))
        error_rate = agg_errors.sum()/m
        print 'total error: ', error_rate, '\n'
        if error_rate == 0.0:
            break
    return weak_class_arr

def ada_classify(dat_to_class, classifier_arr):
    data_mat = np.mat(dat_to_class)
    m = np.shape(data_mat)[0]
    agg_class_est = np.mat(np.zeros((m,1)))
    for i in range(len(classifier_arr)):
        class_est = stump_classify(data_mat, classifier_arr[i]['dim'], classifier_arr[i]['thresh'], classifier_arr[i]['ineq'])
        agg_class_est += classifier_arr[i]['alpha']*class_est
        print agg_class_est
    return np.sign(agg_class_est)

test0()