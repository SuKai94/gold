#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as numpy
from math import log
import operator

def cal_shannon_ent(dataset):
    num_entries = len(dataset)
    label_counts = {}
    for feat_vec in dataset:
        current_label = feat_vec[-1]
        if current_label not in label_counts.keys():
            label_counts[current_label] = 0
        label_counts[current_label] += 1
    shannon_ent = 0.0
    for key in label_counts:
        prob = float(label_counts[key]) / num_entries
        # print prob
        shannon_ent -= prob*log(prob,2)
    # print shannon_ent
    return shannon_ent

def create_dataset():
    dataset = [
    [1,1,'yes'],
    [1,1,'yes'],
    [1,0,'no'],
    [0,1,'no'],
    [0,1,'no']
    ]
    labels = ['no surfacing', 'flippers']
    return dataset, labels

def test0():
    my_dat, labels = create_dataset()
    print cal_shannon_ent(my_dat)

def split_dataset(dataset, axis, value):
    '''
    若dataset=[
    [1,1,'maybe'],
    [1,0,'no']
    ]
    则返回[[1,'maybe']]
    '''
    ret_dataset = []
    for feat_vec in dataset:
        if feat_vec[axis] == value:
            reduced_feat_vec = feat_vec[:axis]
            reduced_feat_vec.extend(feat_vec[axis+1:])
            ret_dataset.append(reduced_feat_vec)
    return ret_dataset

def test1():
    my_dat, labels = create_dataset()
    print my_dat
    print split_dataset(my_dat, 0, 1)

def choose_best_feature_to_split(dataset):
    num_features = len(dataset[0]) - 1
    base_entropy = cal_shannon_ent(dataset)
    best_info_gain = 0.0
    best_feature = -1
    for i in range(num_features):
        feat_list = [example[i] for example in dataset]
        unique_vals = set(feat_list)
        new_entropy = 0.0
        for value in unique_vals:
            sub_dataset = split_dataset(dataset, i ,value)
            prob = len(sub_dataset) / float(len(dataset))
            new_entropy += prob*cal_shannon_ent(sub_dataset)
        info_gain = base_entropy - new_entropy
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_feature = i
    return best_feature

def test2():
    my_dat, labels = create_dataset()
    print choose_best_feature_to_split(my_dat)

def majority_cnt(class_list):
    class_count = {}
    for vote in class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(class_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]

# 递归构建决策树
def create_tree(dataset, labels):
    class_list = [example[-1] for example in dataset]
    # 类别完全相同，则停止分类
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]
    # 遍历完所有特征时返回出现次数最多的
    if len(dataset[0]) == 1:
        return majority_cnt(class_list)
    best_feat = choose_best_feature_to_split(dataset)
    best_feat_label = labels[best_feat]
    my_tree = {best_feat_label:{}}
    del(labels[best_feat])
    feat_values = [example[best_feat] for example in dataset]
    unique_values = set(feat_values)
    # 在每个数据集划分上递归调用create_tree()
    for value in unique_values:
        sub_labels = labels[:]
        my_tree[best_feat_label][value] = create_tree(split_dataset(dataset, best_feat, value), sub_labels)
    return my_tree

def test3():
    my_dat, labels = create_dataset()
    print my_dat
    print labels
    print create_tree(my_dat, labels)

def get_num_leafs(my_tree):
    num_leafs = 0
    first_str = my_tree.keys()[0]
    second_dict = my_tree[first_str]
    for key in second_dict:
        if type(second_dict[key]).__name__ == 'dict':
            num_leafs += get_num_leafs(second_dict[key])
        else:
            num_leafs += 1
    return num_leafs

def get_tree_depth(my_tree):
    max_depth = 0
    first_str = my_tree.keys()[0]
    second_dict = my_tree[first_str]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            this_depth = 1+get_tree_depth(second_dict[key])
        else:
            this_depth = 1
        if this_depth > max_depth : max_depth=this_depth
    return max_depth

def test4():
    my_dat, labels = create_dataset()
    my_tree = create_tree(my_dat, labels)
    print get_num_leafs(my_tree)
    print get_tree_depth(my_tree)

def classify(input_tree, feat_labels, test_vec):
    first_str = input_tree.keys()[0]
    second_dict = input_tree[first_str]
    feat_index = feat_labels.index(first_str)
    for key in second_dict.keys():
        if test_vec[feat_index] == key:
            if type(second_dict[key]).__name__ == 'dict':
                class_label = classify(second_dict[key], feat_labels, test_vec)
            else:
                class_label = second_dict[key]
    return class_label

def retrieve_tree(i):
    list_of_trees = [
    {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
    {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
    ]
    return list_of_trees[i]

def test5():
    my_dat, labels = create_dataset()
    my_tree = retrieve_tree(0)
    print classify(my_tree, labels, [1,0])

def store_tree(input_tree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(input_tree, fw)
    fw.close()

def grab_tree():
    import pickle
    fr = open(filename)
    return pickle.load(fr)

test5()