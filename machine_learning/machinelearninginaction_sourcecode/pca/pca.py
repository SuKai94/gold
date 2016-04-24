#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

'''
PCA：将数据转换成前N个主成分的伪代码大致如下：
去除平均值
计算协方差矩阵
计算协方差矩阵的特征值和特征向量
将特征值从大到小排序
保留最上面的N个特征向量
将数据转换到上述N个特征向量构建的新空间中
'''

def loaddataset(filename, delim='\t'):
    fr = open(filename)
    string_arr = [line.strip().split(delim) for line in fr.readlines()]
    data_arr = [map(float, line) for line in string_arr]
    return np.mat(data_arr)

def pca(datamat, top_n_feat=9999999):
    mean_vals = np.mean(datamat, axis=0)
    mean_removed = datamat - mean_vals
    cov_mat = np.cov(mean_removed, rowvar=0)
    eig_vals, eig_vects = np.linalg.eig(np.mat(cov_mat))
    eig_val_ind = np.argsort(eig_vals)
    eig_val_ind = eig_val_ind[:-(top_n_feat+1):-1]
    red_eigvects = eig_vects[:,eig_val_ind]
    lowd_data_mat = mean_removed*red_eigvects
    recon_mat = (lowd_data_mat*red_eigvects.T) + mean_vals
    # 原始数据被重构之后返回用于调试，同时降维之后的数据集也被返回
    return lowd_data_mat, recon_mat

def test0():
    datamat = loaddataset('testSet.txt')
    lowDMat, reconMat = pca(datamat, 1)
    print np.shape(lowDMat)
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datamat[:,0].flatten().A[0], datamat[:,1].flatten().A[0], marker='^', s=90)
    ax.scatter(reconMat[:,0].flatten().A[0], reconMat[:,1].flatten().A[0], marker='o', s=50, c='red')
    plt.show()

test0()