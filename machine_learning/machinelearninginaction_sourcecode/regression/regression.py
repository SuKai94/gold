#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def load_dataset(filename):
    num_feat = len(open(filename).readline().split('\t')) - 1
    data_mat = []
    label_mat = []
    fr = open(filename)
    for line in fr.readlines():
        line_arr = []
        cur_line = line.strip().split('\t')
        for i in range(num_feat):
            line_arr.append(float(cur_line[i]))
        data_mat.append(line_arr)
        label_mat.append(float(cur_line[-1]))
    return data_mat, label_mat

# 最小二乘法
def stand_regres(x_arr, y_arr):
    x_mat = np.mat(x_arr)
    y_mat = np.mat(y_arr).T
    xTx = x_mat.T*x_mat
    # 计算行列式是否为0
    if np.linalg.det(xTx) == 0.0:
        print 'This matrix is singular, cannot do inverse'
        return
    ws = xTx.I * (x_mat.T * y_mat)
    return ws

def test_stand_regres():
    x_arr, y_arr = load_dataset('ex0.txt')
    ws = stand_regres(x_arr, y_arr)
    x_mat = np.mat(x_arr)
    y_mat = np.mat(y_arr)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x_mat[:,1].flatten().A[0], y_mat.T[:,0].flatten().A[0])
    x_copy = x_mat.copy()
    x_copy.sort(0)
    y_hat = x_copy*ws
    ax.plot(x_copy[:,1], y_hat)
    plt.show()

# 局部加权线性回归函数
def lwlr(test_point ,x_arr, y_arr, k=1.0):
    x_mat = np.mat(x_arr)
    y_mat = np.mat(y_arr).T
    m = np.shape(x_mat)[0]
    weights = np.mat(np.eye((m)))
    for j in range(m):
        diff_mat = test_point - x_mat[j,:]
        weights[j,j] = np.exp(diff_mat*diff_mat.T/(-2.0*k**2))
    xTx = x_mat.T * (weights*x_mat)
    if np.linalg.det(xTx) == 0.0:
        print 'This matrix is singular, cannot do inverse'
        return
    ws = xTx.I * (x_mat.T * (weights*y_mat))
    return test_point*ws

def lwlr_test(test_arr, x_arr, y_arr, k=1.0):
    m = np.shape(test_arr)[0]
    y_hat = np.zeros(m)
    for i in range(m):
        y_hat[i] = lwlr(test_arr[i], x_arr, y_arr, k)
    return y_hat

def test0():
    x_arr, y_arr = load_dataset('ex0.txt')
    print y_arr[0]
    ws0 = lwlr(x_arr[0], x_arr, y_arr, 1.0)
    print ws0
    ws1 = lwlr(x_arr[0], x_arr, y_arr, 0.001)
    print ws1
    y_hat = lwlr_test(x_arr, x_arr, y_arr, 1.0)
    x_mat = np.mat(x_arr)
    srt_ind = x_mat[:,1].argsort(0)
    x_sort = x_mat[srt_ind][:,0,:]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x_sort[:,1], y_hat[srt_ind])
    ax.scatter(x_mat[:,1].flatten().A[0], np.mat(y_arr).T.flatten().A[0], s=2, c='red')
    plt.show()

# 岭回归
def ridge_regres(x_mat, y_mat, lam=0.2):
    xTx = x_mat.T*x_mat
    denom = xTx + np.eye(np.shape(x_mat)[1])*lam
    if np.linalg.det(denom) == 0.0:
        print 'This matrix is singular, cannot do inverse'
        return
    ws = denom.I * (x_mat.T*y_mat)
    return ws

def ridge_test(x_arr, y_arr):
    x_mat = np.mat(x_arr)
    y_mat = np.mat(y_arr).T
    # 对特征进行标准化
    # 所有特征都减去各自的均值，并除以方差
    y_mean = np.mean(y_mat, 0)
    x_mean = np.mean(x_mat, 0)
    x_var = np.var(x_mat, 0)
    x_mat = (x_mat - x_mean) / x_var
    num_test_pts = 30
    w_mat = np.zeros((num_test_pts, np.shape(x_mat)[1]))
    for i in range(num_test_pts):
        ws = ridge_regres(x_mat, y_mat, np.exp(i-10))
        w_mat[i,:] = ws.T
    return w_mat

def test1():
    abx, aby = load_dataset('abalone.txt')
    ridge_weights = ridge_test(abx, aby)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(ridge_weights)
    plt.show()

def rss_error(y_arr, y_hat_arr):
    return ((y_arr - y_hat_arr)**2).sum()

def stage_wise(x_arr, y_arr, eps=0.01, num_it=100):
    x_mat = np.mat(x_arr)
    y_mat = np.mat(y_arr).T
    y_mean = np.mean(y_mat, 0)
    y_mat = y_mat - y_mean
    # 将特征按照均值为0，方差为1进行标准化处理
    x_mat = np.regularize(x_mat)
    m, n = np.shape(x_mat)
    return_mat = np.zeros((num_it, n))
    ws = np.zeros((n, 1))
    ws_test = ws.copy()
    ws_max = ws.copy()
    for i in range(num_it):
        print ws.T
        lowest_error = inf;
        for j in range(n):
            # 分别计算增加或者减少该特征对误差的影响
            for sign in [-1, 1]:
                ws_test = ws.copy()
                ws_test[j] += eps*ws_test
                y_test = x_mat*ws_test
                # 使用平方误差
                rsse = rss_error(y_mat.A, y_test.A)
                if rsse < lowest_error:
                    lowest_error = rsse
                    ws_max = ws_test
        ws = ws_max.copy()
        return_mat[i,:] = ws.T
    return return_mat

test1()