#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np

def load_dataset(filename):
    data_mat = []
    label_mat = []
    fr = open(filename)
    for line in fr.readlines():
        line_arr = line.strip().split('\t')
        data_mat.append([float(line_arr[0]), float(line_arr[1])])
        label_mat.append(float(line_arr[2]))
    return data_mat, label_mat

# i是第一个alpha的下标，m是所有alpha的数目
def select_jrand(i, m):
    j = i
    while j == i:
        j = int(random.uniform(0,m))
    return j

def clip_alpha(aj, h, l):
    if aj > h:
        aj = h
    if l > aj:
        aj = l
    return aj

def svm_simple(data_mat_in, class_labels, c, toler, max_iter):
    data_matrix = np.mat(data_mat_in)
    label_mat = np.mat(class_labels).transpose()
    b = 0
    m, n = np.shape(data_matrix)
    alphas = np.mat(np.zeros((m,1)))
    iter = 0
    while iter < max_iter:
        alpha_pairs_changed = 0
        for i in range(m):
            fxi = float((np.multiply(alphas, label_mat).T) * (data_matrix*data_matrix[i,:].T)) + b
            # print fxi
            ei = fxi - float(label_mat[i])
            # print ei
            if ((label_mat[i]*ei < -toler) and (alphas[i] < c)) or ((label_mat[i]*ei > toler) and (alphas[i] > 0)):
                # 选取第二个alpha值
                j = select_jrand(i, m)
                fxj = float((np.multiply(alphas, label_mat).T) * (data_matrix*data_matrix[j,:].T)) + b
                ej = fxj - float(label_mat[j])
                alpha_iold = alphas[i].copy()
                alpha_jold = alphas[j].copy()
                if label_mat[i] != label_mat[j]:
                    l = max(0, alphas[j]-alphas[i])
                    h = min(c, c+alphas[j]-alphas[i])
                else:
                    l = max(0, alphas[j]+alphas[i]-c)
                    h = min(c, alphas[j]+alphas[i])
                if l == h:
                    print 'l == h'
                    continue
                eta = 2.0*data_matrix[i,:]*data_matrix[j,:].T - data_matrix[i,:]*data_matrix[i,:].T - data_matrix[j,:]*data_matrix[j,:].T
                if eta >= 0:
                    print 'eta >= 0'
                    continue
                alphas[j] -= label_mat[j]*(ei-ej)/eta
                alphas[j] = clip_alpha(alphas[j], h, l)
                if abs(alphas[j] - alpha_jold) < 0.00001:
                    print 'j not moving enough'
                    continue
                alphas[i] += label_mat[j]*label_mat[i]*(alpha_jold-alphas[j])
                b1 = b - ei - label_mat[i]*(alphas[i]-alpha_iold)*data_matrix[i,:]*data_matrix[i,:].T - label_mat[j]*(alphas[j]-alpha_jold)*data_matrix[i,:]*data_matrix[j,:].T
                b2 = b - ej - label_mat[i]*(alphas[i]-alpha_iold)*data_matrix[i,:]*data_matrix[j,:].T - label_mat[j]*(alphas[j]-alpha_jold)*data_matrix[j,:]*data_matrix[j,:].T
                if (0 < alphas[i]) and (c > alphas[i]):
                    b = b1
                elif (0 < alphas[j]) and (c > alphas[j]):
                    b = b2
                else:
                    b = (b1+b2)/2.0
                alpha_pairs_changed += 1
                print 'iter %d i: %d, pairs changed %d' % (iter, i, alpha_pairs_changed)
        if alpha_pairs_changed == 0:
            iter += 1
        else:
            iter = 0
        print 'iteration number: %d' % (iter)
    return b, alphas

def test0():
    data_arr, label_arr = load_dataset('testSet.txt')
    b, alphas = svm_simple(data_arr, label_arr, 0.6, 0.001, 40)
    print b
    print alphas[alphas>0]


class OptStruct:
    def __init__(self, data_mat_in, class_labels, C, toler):
        self.X = data_mat_in
        self.label_mat = class_labels
        self.C = C
        self.tol = toler
        self.m = np.shape(data_mat_in)[0]
        self.alphas = np.mat(np.zeros((self.m, 1)))
        self.b = 0
        # 误差缓存，第一列表示给出的e_cache是否有效的标志位，第二列给出的是实际的e值
        self.e_cache = np.mat(np.zeros((self.m, 2)))

def cal_c_ek(oS, k):
    fxk = float((np.multiply(oS.alphas, oS.label_mat)).T*(oS.X*oS.X[k,:].T)) + oS.b
    ek = fxk - float(oS.label_mat[k])
    return ek

# 选择合适的第二个alpha值，保证每次优化中采用最大步长，即ei-ej最大的alpha值
def select_j(i, oS, ei):
    max_k = -1
    max_delta_e = 0
    ej = 0
    oS.e_cache[i] = [1, ei]
    # 非零e值速所代表的alpha值
    valid_ecache_list = np.nonzero(oS.e_cache[:,0].A)[0]
    if len(valid_ecache_list) > 1:
        for k in valid_ecache_list:
            if k == i:
                continue
            ek = cal_c_ek(oS, k)
            delta_e = abs(ei - ek)
            if delta_e > max_delta_e:
                max_k = k
                max_delta_e = delta_e
                ej = ek
        return max_k, ej
    # 如果这是第一次循环的话，随机选择第二个alpha值即可
    else:
        j = select_jrand(i, oS.m)
        ej = cal_c_ek(oS, j)
    return j, ej

def update_ek(oS, k):
    ek = cal_c_ek(oS, k)
    oS.e_cache[k] = [1, ek]

def innerL(i, oS):
    ei = cal_c_ek(oS, i)
    if ((oS.label_mat[i]*ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.label_mat[i]*ei > oS.tol) and (oS.alphas[i] > 0)):
        j, ej = select_j(i, oS, ei)
        alpha_iold = oS.alphas[i].copy()
        alpha_jold = oS.alphas[j].copy()
        if oS.label_mat[i] != oS.alphas[j]:
            l = max(0, oS.alphas[j]-oS.alphas[i])
            h = min(oS.C, oS.C+oS.alphas[j]-oS.alphas[i])
        else:
            l = max(0, oS.alphas[j]+oS.alphas[i]-oS.C)
            h = min(oS.C, oS.alphas[j]+oS.alphas[i])
        if l == h:
            print 'l==h'
            return 0
        eta = 2.0*oS.X[i,:]*oS.X[j,:].T - oS.X[i,:]*oS.X[i,:].T - oS.X[j,:]*oS.X[j,:].T
        if eta >= 0:
            print 'eta >= 0'
            return 0
        oS.alphas[j] -= oS.label_mat[j]*(ei-ej)/eta
        oS.alphas[j] = clip_alpha(oS.alphas[j], h, l)
        update_ek(oS, j)
        if abs(oS.alphas[j] - alpha_jold) < 0.00001:
            print 'j not moving enough'
            return 0
        oS.alphas[i] += oS.label_mat[j]*oS.label_mat[i]*(alpha_jold-oS.alphas[j])
        update_ek(oS, i)
        b1 = oS.b - ei - oS.label_mat[i]*(oS.alphas[i]-alpha_iold)*oS.X[i,:]*oS.X[i,:].T - oS.label_mat[j]*(oS.alphas[j]-alpha_jold)*oS.X[i,:]*oS.X[j,:].T
        b2 = oS.b - ej - oS.label_mat[i]*(oS.alphas[i]-alpha_iold)*oS.X[i,:]*oS.X[j,:].T - oS.label_mat[j]*(oS.alphas[j]-alpha_jold)*oS.X[j,:]*oS.X[j,:].T
        if 0 < oS.alphas[i] and oS.C > oS.alphas[i]:
            oS.b = b1
        elif 0 < oS.alphas[j] and oS.C > oS.alphas[j]:
            oS.b = b2
        else:
            oS.b = (b1+b2) / 2
        return 1
    else:
        return 0

def smo_p(data_mat_in, class_labels, C, toler, max_iter, ktup=('lin', 0)):
    oS = OptStruct(np.mat(data_mat_in), np.mat(class_labels).transpose(), C, toler)
    iter = 0
    entire_set = True
    alpha_pairs_changed = 0
    while (iter < max_iter) and ((alpha_pairs_changed > 0) or (entire_set)):
        alpha_pairs_changed = 0
        # 在数据集上遍历任意可能的alpha值
        if entire_set:
            for i in range(oS.m):
                alpha_pairs_changed += innerL(i, oS)
            print 'full_set, iter: %d i: %d, pairs changed %d' % (iter, i, alpha_pairs_changed)
            iter+= 1
        # 遍历所有非边界alpha值，也就是不在边界0或者1上的值
        else:
            non_bound_is = np.nonzero((oS.alphas.A > 0) * (oS.alphas.A < C))[0]
            for i in non_bound_is:
                alpha_pairs_changed += innerL(i, oS)
                print 'non-bound, iter %d i: %d, pairs changed %d' % (iter, i, alpha_pairs_changed)
                iter += 1
        if entire_set:
            entire_set = False
        elif alpha_pairs_changed == 0:
            entire_set = True
        print 'iteration number %d' % iter
    return oS.b, oS.alphas

def test1():
    data_arr, label_arr = load_dataset('testSet.txt')
    b, alphas = smo_p(data_arr, label_arr, 0.6, 0.001, 40)
    print b
    print alphas[alphas>0]

def cal_w(alphas, data_arr, class_labels):
    X = np.mat(data_arr)
    label_mat = np.mat(class_labels).transpose()
    m, n = np.shape(X)
    w = np.zeros((n, 1))
    for i in range(m):
        w += np.multiply(alphas[i]*label_mat[i], X[i,:].T)
    return w

def test2():
    data_arr, label_arr = load_dataset('testSet.txt')
    b, alphas = smo_p(data_arr, label_arr, 0.6, 0.001, 40)
    w = cal_w(alphas, data_arr, label_arr)
    print w
    data_mat = np.mat(data_arr)
    print data_mat[0]*np.mat(w) + b
    print label_arr[0]

def kernel_trans(X, A, k_tup):
    # X: m*n
    # A: 1*n
    m, n = np.shape(X)
    k = np.mat(np.zeros((m,1)))
    if k_tup[0] == 'lin':
        k = X * A.T
    elif k_tup[0] == 'rbf':
        for j in range(m):
            delta_row = X[j,:] - A # 1*n
            k[j] = delta_row*delta_row.T
        k = np.exp(k/(-1*k_tup[1]**2))
    else:
        raise NameError('That kernel is not recognized.')
    return k

class OptKernelStruct:
    def __init__(self, data_mat_in, class_labels, C, toler, k_tup):
        self.X = data_mat_in
        self.label_mat = class_labels
        self.C = C
        self.tol = toler
        self.m = np.shape(data_mat_in)[0]
        self.alphas = np.mat(np.zeros((self.m, 1)))
        self.b = 0
        # 误差缓存，第一列表示给出的e_cache是否有效的标志位，第二列给出的是实际的e值
        self.e_cache = np.mat(np.zeros((self.m, 2)))
        self.K = np.mat(np.zeros((self.m, self.m)))
        for i in range(self.m):
            self.K[:,i] = kernel_trans(self.X, slef.X[i,:], k_tup)

def innerL_kernel(i, oS):
    ei = cal_c_ek(oS, i)
    if ((oS.label_mat[i]*ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.label_mat[i]*ei > oS.tol) and (oS.alphas[i] > 0)):
        j, ej = select_j(i, oS, ei)
        alpha_iold = oS.alphas[i].copy()
        alpha_jold = oS.alphas[j].copy()
        if oS.label_mat[i] != oS.alphas[j]:
            l = max(0, oS.alphas[j]-oS.alphas[i])
            h = min(oS.C, oS.C+oS.alphas[j]-oS.alphas[i])
        else:
            l = max(0, oS.alphas[j]+oS.alphas[i]-oS.C)
            h = min(oS.C, oS.alphas[j]+oS.alphas[i])
        if l == h:
            print 'l==h'
            return 0
        # eta = 2.0*oS.X[i,:]*oS.X[j,:].T - oS.X[i,:]*oS.X[i,:].T - oS.X[j,:]*oS.X[j,:].T
        eta = 2.0*oS.K[i,j] - oS.K[i,i] - oS.K[j,j]
        if eta >= 0:
            print 'eta >= 0'
            return 0
        oS.alphas[j] -= oS.label_mat[j]*(ei-ej)/eta
        oS.alphas[j] = clip_alpha(oS.alphas[j], h, l)
        update_ek(oS, j)
        if abs(oS.alphas[j] - alpha_jold) < 0.00001:
            print 'j not moving enough'
            return 0
        oS.alphas[i] += oS.label_mat[j]*oS.label_mat[i]*(alpha_jold-oS.alphas[j])
        update_ek(oS, i)
        # b1 = oS.b - ei - oS.label_mat[i]*(oS.alphas[i]-alpha_iold)*oS.X[i,:]*oS.X[i,:].T - oS.label_mat[j]*(oS.alphas[j]-alpha_jold)*oS.X[i,:]*oS.X[j,:].T
        # b2 = oS.b - ej - oS.label_mat[i]*(oS.alphas[i]-alpha_iold)*oS.X[i,:]*oS.X[i,:].T - oS.label_mat[j]*(oS.alphas[j]-alpha_jold)*oS.X[j,:]*oS.X[j,:].T
        b1 = oS.b - ei - oS.label_mat[i]*(oS.alphas[i]-alpha_iold)*oS.K[i,i] - oS.label_mat[j]*(oS.alphas[j]-alpha_jold)*oS.K[i,j]
        b2 = oS.b - ej - oS.label_mat[i]*(oS.alphas[i]-alpha_iold)*oS.K[i,j] - oS.label_mat[j]*(oS.alphas[j]-alpha_jold)*oS.K[j,j]
        if 0 < oS.alphas[i] and oS.C > oS.alphas[i]:
            oS.b = b1
        elif 0 < oS.alphas[j] and oS.C > oS.alphas[j]:
            oS.b = b2
        else:
            oS.b = (b1+b2) / 2
        return 1
    else:
        return 0

def cal_c_ek_kernel(oS, k):
    # fxk = float((np.multiply(oS.alphas, oS.label_mat)).T*(oS.X*oS.X[k,:].T)) + oS.b
    fxk = float((np.multiply(oS.alphas, oS.label_mat)).T*oS.K[:,k]) + oS.b
    ek = fxk - float(oS.label_mat[k])
    return ek

def test_rbf(k1=1.3):
    data_arr, label_arr = load_dataset('testSetRBF.txt')
    b, alphas = smo_p(data_arr, label_arr, 200, 0.001, 10000, ('rbf', k1))
    data_mat = np.mat(data_arr)
    label_mat = np.mat(label_arr).transpose()
    sv_ind = np.nonzero(alphas.A>0)[0]
    svs = data_mat[sv_ind]
    label_sv = label_mat[sv_ind]
    print 'there are %d support vectors' % np.shape(svs)[0]
    m, n = np.shape(data_mat)
    error_count = 0
    for i in range(m):
        kernel = kernel_trans(svs, data_mat[i,:], ('rbf', k1))
        predict = kernel.T*np.multiply(label_sv, alphas[sv_ind]) + b
        if np.sign(predict) != np.sign(label_arr[i]):
            error_count += 1
    print 'the training error rate is: %f' % (float(error_count)/m)

    data_arr, label_arr = load_dataset('testSetRBF2.txt')
    error_count = 0
    data_mat = np.mat(data_arr)
    label_mat = np.mat(label_arr).transpose()
    m, n = np.shape(data_mat)
    for i in range(m):
        kernel = kernel_trans(svs, data_mat[i,:], ('rbf', k1))
        predict = kernel.T*np.multiply(label_sv, alphas[sv_ind]) + b
        if np.sign(predict) != np.sign(label_arr[i]):
            error_count += 1
    print 'the test error rate is: %f' % (float(error_count)/m)

test_rbf()