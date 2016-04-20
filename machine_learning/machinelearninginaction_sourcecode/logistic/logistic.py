#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random

def load_dataset():
    data_mat = []
    label_mat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        line_arr = line.strip().split()
        data_mat.append([1.0, float(line_arr[0]), float(line_arr[1])])
        label_mat.append(int(line_arr[2]))
    return data_mat, label_mat

def sigmoid(inX):
    return 1.0/(1+np.exp(-inX))

def grad_ascent(data_mat, class_labels):
    data_matrix = np.mat(data_mat)
    label_mat = np.mat(class_labels).transpose()
    m, n = np.shape(data_matrix)
    alpha = 0.001
    max_cycles = 500
    weights = np.ones((n,1))
    for k in range(max_cycles):
        h = sigmoid(data_matrix*weights)
        error = (label_mat - h)
        weights = weights + alpha*data_matrix.transpose()*error
    return weights

def test0():
    data_arr, label_mat = load_dataset()
    weights = grad_ascent(data_arr, label_mat)
    print weights.getA()

def plot_best_fit(wei):
    import matplotlib.pyplot as plt
    if type(wei).__name__ != 'ndarray':
        weights = wei.getA()
    else:
        weights = wei
    data_mat, label_mat = load_dataset()
    data_arr = np.array(data_mat)
    n = np.shape(data_arr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(label_mat[i]) == 1:
            xcord1.append(data_arr[i,1])
            ycord1.append(data_arr[i,2])
        else:
            xcord2.append(data_arr[i,1])
            ycord2.append(data_arr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = np.arange(-3.0, 3.0, 0.1)
    # 依据0=w0x0+w1x1+w2x2解出X2和X1
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()

def test1():
    data_arr, label_mat = load_dataset()
    weights = grad_ascent(data_arr, label_mat)
    plot_best_fit(weights)

# 一次仅用一个样本点来更新回归系数
def stoc_grad_ascent0(data_matrix, class_labels):
    m, n = np.shape(data_matrix)
    alpha = 0.01
    weights = np.ones(n)
    for i in range(m):
        h = sigmoid(sum(data_matrix[i]*weights))
        error = class_labels[i] - h
        weights = weights + alpha*error*data_matrix[i]
    return weights

def test2():
    data_arr, label_mat = load_dataset()
    weights = stoc_grad_ascent0(np.array(data_arr), label_mat)
    plot_best_fit(weights)

# 防止在收敛值附近波动
# 随机选取用本来更新回归系数
def stoc_grad_ascent1(data_matrix, class_labels, num_iter=150):
    m, n = np.shape(data_matrix)
    weights = np.ones(n)
    for j in range(num_iter):
        data_index = range(m)
        for i in range(m):
            alpha = 4/(1.0+j+i) + 0.01
            rand_index = int(random.uniform(0, len(data_index)))
            h = sigmoid(sum(data_matrix[rand_index]*weights))
            error = class_labels[rand_index] - h
            weights = weights + alpha*error*data_matrix[rand_index]
            del(data_index[rand_index])
    return weights

def test3():
    data_arr, label_mat = load_dataset()
    weights = stoc_grad_ascent1(np.array(data_arr), label_mat)
    plot_best_fit(weights)

def classify_vector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5:
        return 1.0
    else:
        return 0.0

def colic_test():
    fr_train = open('horseColicTraining.txt')
    fr_test = open('horseColicTest.txt')
    training_set = []
    training_labels = []
    for line in fr_train.readlines():
        curr_line = line.strip().split('\t')
        line_arr = []
        for i in range(21):
            line_arr.append(float(curr_line[i]))
        training_set.append(line_arr)
        training_labels.append(float(curr_line[21]))
    training_weights = stoc_grad_ascent1(np.array(training_set), training_labels, 500)
    error_count = 0
    num_test_vec = 0.0
    for line in fr_test.readlines():
        num_test_vec += 1.0
        curr_line = line.strip().split('\t')
        line_arr = []
        for i in range(21):
            line_arr.append(float(curr_line[i]))
        if int(classify_vector(np.array(line_arr), training_weights)) != int(curr_line[21]):
            error_count += 1
    error_rate = float(error_count) / num_test_vec
    print 'error rate is: %f' % error_rate
    return error_rate

def multi_test():
    num_tests = 10
    error_sum = 0.0
    for k in range(num_tests):
        error_sum += colic_test()
    print 'after %d iteration the average error rate is: %f' % (num_tests, error_sum/float(num_tests))

def test4():
    multi_test()

test4()