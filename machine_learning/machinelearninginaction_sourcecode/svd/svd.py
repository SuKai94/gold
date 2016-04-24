#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

'''
svd：Singular Value Decomposition，奇异值分解
利用svd，我们能够使用小得多的数据集来表示原始数据，这样做，实际上是去除了噪声和冗余信息
svd的两个应用：信息检索和推荐系统
'''

def test0():
    u, sigma, vt = np.linalg.svd([[1,1], [7,7]])
    print u
    print sigma,
    print vt

'''
有很多应用可以通过svd来提升性能，比如推荐系统
'''

'''
相似度计算
'''
# 欧式距离
def eclud_sim(ina, inb):
    return 1.0/(1.0+np.linalg.norm(ina, inb))

# 皮尔逊相关系数
def pears_sim(ina, inb):
    if len(ina) < 3:
        return 1.0
    return 0.5+0.5*np.corrcoef(ina, inb, rowarr=0)[0][1]

# 余弦相似度
def cos_sim(ina, inb):
    num = float(ina.T*inb)
    denom = np.linalg.norm(ina)*np.linalg.norm(inb)
    return 0.5+0.5*(num/denom)

'''
暂时搁置
'''