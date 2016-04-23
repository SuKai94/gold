#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

'''
CART: Classification And Regression Trees
分类与回归树
'''

class TreeNode():
    def __init__(self, feat, val, right, left):
        feature_to_split_on = feat
        value_of_split = val
        right_branch = right
        left_branch = left

def load_dataset(filename):
    data_mat = []
    fr = open(filename)
    for line in fr.readlines():
        cur_line =  line.strip().split('\t')
        flt_line = map(float, cur_line)
        data_mat.append(flt_line)
    return data_mat

def reg_leaf(dataset):
    # 负责生成叶节点，在回归树中即目标变量的均值
    return np.mean(dataset[:,-1])

def reg_err(dataset):
    # 误差估计函数
    # 总方差：均方差*样本数量
    return np.var(dataset[:,-1]) * np.shape(dataset)[0]

def bin_split_dataset(dataset, feature, value):
    mat0 = dataset[np.nonzero(dataset[:,feature] > value)[0], :][0]
    mat1 = dataset[np.nonzero(dataset[:,feature] <= value)[0], :][0]
    return mat0, mat1
    
# 用最佳方式切分数据集和生成相应的叶节点
# 目的是找到最佳的二元切分方式
def choose_best_split(dataset, leaftype=reg_leaf, errtype=reg_err, ops=(1,4)):
    # tol_s表示容许的误差下降值
    # tol_n表示切分的最少样本数
    tol_s = ops[0]
    tol_n = ops[1]
    # 所有值相等，则退出
    if len(set(dataset[:,-1].T.tolist()[0])) == 1:
        return None, leaftype(dataset)
    m, n = np.shape(dataset)
    s = errtype(dataset)
    best_s = np.inf
    best_index = 0
    best_value = 0
    for feat_index in range(n-1):
        for split_val in set(dataset[:,feat_index]):
            mat0, mat1 = bin_split_dataset(dataset, feat_index, split_val)
            if np.shape(mat0)[0] < tol_n or np.shape(mat1)[0] < tol_n:
                continue
            new_s = errtype(mat0) + errtype(mat1)
            if new_s < best_s:
                best_index = feat_index
                best_value = split_val
                best_s = new_s
    if (s-best_s) < tol_s:
        return None, leaftype(dataset)
    mat0, mat1 = bin_split_dataset(dataset, best_index, best_value)
    if (np.shape(mat0)[0] < tol_n) or (np.shape(mat1)[0] < tol_n):
        return None, leaftype(dataset)
    return best_index, best_value

def create_tree(dataset, leaftype=reg_leaf, errtype=reg_err, ops=(1,4)):
    feat, val = choose_best_split(dataset, leaftype, errtype, ops)
    if feat == None:
        return val
    ret_tree = {}
    ret_tree['spInd'] = feat
    ret_tree['spVal'] = val
    l_set, r_set = bin_split_dataset(dataset, feat, val)
    ret_tree['left'] = create_tree(l_set, leaftype, errtype, ops)
    ret_tree['right'] = create_tree(r_set, leaftype, errtype, ops)
    return ret_tree

def test0():
    test_mat = np.mat(np.eye(4))
    mat0, mat1 = bin_split_dataset(test_mat, 1, 0.5)
    print mat0
    print mat1s

def test1():
    my_dat = load_dataset('ex0.txt')
    my_mat = np.mat(my_dat)
    print create_tree(my_mat)

'''
树剪枝
tol_s, tol_n算是预剪枝，树构建算法对tol_s和tol_n非常敏感
后剪枝
'''
# 判断当前节点是够为叶节点
def is_tree(obj):
    return type(obj).__name__ == 'dict'


def get_mean(tree):
    if is_tree(tree['right']):
        tree['right'] = get_mean(tree['right'])
    if is_tree(tree['left']):
        tree['left'] = get_mean(tree['left'])
    return (tree['left']+tree['right'])/2.0

# 参数：待剪枝的树以及剪枝所需的测试集
'''
基于已有的树切分测试数据：
    如果存在任一个子集是一棵树，则在该子集递归剪枝过程
    计算当前两个叶节点合并后的误差
    计算不合并的误差
    如果合并误差会降低的话，选择将叶节点合并
'''
def prune(tree, testdata):
    if np.shape(testdata)[0] == 0:
        return get_mean(tree)
    if is_tree(tree['left']) or is_tree(tree['right']):
        l_set, r_set = bin_split_dataset(testdata, tree['spInd'], tree['spVal'])
    if is_tree(tree['left']):
        tree['left'] = prune(tree['left'], l_set)
    if is_tree(tree['right']):
        tree['right'] = prune(tree['right'], r_set)
    if not is_tree(tree['left']) and not is_tree(tree['right']):
        l_set, r_set = bin_split_dataset(testdata, tree['spInd'], tree['spVal'])
        error_no_merge = np.sum(np.power(l_set[:,-1]-tree['left'],2)) + np.sum(np.power(r_set[:,-1]-tree['right'],2))
        tree_mean = (tree['left']+tree['right'])/2.0
        error_merge = np.sum(np.power(testdata[:,-1]-tree_mean,2))
        if error_merge < error_no_merge:
            print 'merging'
            return tree_mean
        else:
            return tree
    else:
        return tree

def test2():
    my_dat = load_dataset('ex0.txt')
    my_mat = np.mat(my_dat)
    my_tree = create_tree(my_mat)
    my_data_test = load_dataset('ex2test.txt')
    my_mat_test = np.mat(my_data_test)
    print prune(my_tree, my_mat_test)

'''
模型树
'''
# 暂时搁置于此

test2()