#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

def loaddataset(filename):
    data_mat = []
    fr = open(filename)
    for line in fr.readlines():
        cur_line = line.strip().split('\t')
        flt_line = map(float, cur_line)
        data_mat.append(flt_line)
    return data_mat

def dist_eclud(vecA, vecB):
    return np.sqrt(np.sum(np.power(vecA-vecB, 2)))

def rand_cent(dataset, k):
    n = np.shape(dataset)[1]
    centroids = np.mat(np.zeros((k,n)))
    for j in range(n):
        min_j = np.min(dataset[:,j])
        range_j = float(np.max(dataset[:,j]) - min_j)
        centroids[:,j] = min_j + range_j * np.random.rand(k,1)
    return centroids

def test0():
    data_mat = np.mat(loaddataset('testSet.txt'))
    print np.min(data_mat[:,0])
    print np.max(data_mat[:,0])
    print np.min(data_mat[:,1])
    print np.max(data_mat[:,1])
    print rand_cent(data_mat, 2)

def kmeans(dataset, k, distmeas=dist_eclud, create_cnt=rand_cent):
    m = np.shape(dataset)[0]
    cluster_assment = np.mat(np.zeros((m,2)))
    centroids = create_cnt(dataset, k)
    cluster_changed = True
    while cluster_changed:
        cluster_changed = False
        # 对于每个数据点，对于每个质点，计算质点与数据点之间的距离，将数据点分配给距其最近的簇
        for i in range(m):
            min_dist = np.inf
            min_index = -1
            for j in range(k):
                dist_ji = distmeas(centroids[j,:], dataset[i,:])
                if dist_ji < min_dist:
                    min_dist = dist_ji
                    min_index = j
            if cluster_assment[i,0] != min_index:
                cluster_changed = True
            cluster_assment[i,:] = min_index, min_dist**2
        # 对于每一个簇，计算簇中所有点的均值并将均值作为质心
        for cent in range(k):
            pts_in_clust = dataset[np.nonzero(cluster_assment[:,0].A==cent)[0]]
            centroids[cent,:] = np.mean(pts_in_clust, axis=0)
    return centroids, cluster_assment

def test1():
    data_mat = np.mat(loaddataset('testSet.txt'))
    my_centroids, cluster_assing = kmeans(data_mat, 4)
    print my_centroids
    print cluster_assing

'''
下面讨论kmeans可能出现的问题：k-means会收敛于局部最小值，而非全局最小值
一个用于度量聚类效果的指标是SSE(Sum of Squared Error，误差平方和)，对用着cluster_assment矩阵的第一列之和
降低SSE的一种方法是：将具有最大SSE值得簇分成两个簇，即将最大簇包含的点过滤出来，并在这些点上运行k=2的k-means算法；但为了保证簇总数不变，可以将两个簇进行合并，
当维度低时，可以通过可视化发现应该合并的两个簇，维度多时，合并有两种量化的方法：合并最近的质心，或者合并两个使得SSE增幅最小的质心
'''
# 二分k-均值算法
'''
先将所有点看成一个簇，
当簇数目小于k：
  对于每个簇
    计算总误差
    在给定的簇上进行k=2的kmeans算法
    计算将该簇一分为二之后的总误差
  选择使得误差最小的那个簇进行划分
'''
def bitkmeans(dataset, k, distmeas=dist_eclud):
    m = np.shape(dataset)[0]
    cluster_assment = np.mat(np.zeros(m,2))
    centroids0 = np.mean(dataset, axis=0).tolist()[0]
    cenlist = [centroids0]
    for j in range(m):
        cluster_assment[j,1] = distmeas(np.mat(centroids0), dataset[j,:])**2
    while len(cenlist) < k:
        lowest_sse = np.inf
        for i in range(len(cenlist)):
            pts_in_curr_cluster = dataset[np.nonzero(cluster_assment[:,0].A==i)[0],:]
            centroid_mat, split_clust_ass = kmeans(pts_in_curr_cluster, 2, distmeas)
            sse_split = np.sum(split_clust_ass[:,1])
            sse_not_split = np.sum(cluster_assment[np.nonzero(cluster_assment[:,0].A!=i)[0],1])
            print 'sse_split, and not_split: ', sse_split, sse_not_split
            # 划分误差与剩余未划分数据集误差之和罪恶本次划分的误差
            if sse_split + sse_not_split < lowest_sse:
                best_cent_to_split = i
                best_new_cents = split_clust_ass.copy()
                lowest_sse = sse_split + sse_not_split
        # 使用k=2的kmeans得到编号为0和1的两个结果簇，需要将这些编号修改为划分簇以及新加簇的编号
        best_clust_ass[np.nonzero(best_clust_ass[:,0].A==1)[0],0] = len(cenlist)
        best_clust_ass[np.nonzero(best_clust_ass[:,0].A==0)[0],0] = best_cent_to_split
        print 'the best_cent_to_split is: ', best_cent_to_split
        print 'the len of best_clust_ass is: ', len(best_clust_ass)
        cenlist[best_cent_to_split] = best_new_cents[0,:]
        cenlist.append(best_new_cents[1,:])
        cluster_assment[np.nonzero(cluster_assment[:,0].A == best_cent_to_split)[0],:] = best_clust_ass
    return np.mat(cenlist), cluster_assment

test1()