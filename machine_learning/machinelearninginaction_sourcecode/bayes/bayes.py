#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random

'''
朴素贝叶斯中朴素是指每个特征在统计意义上是独立的，即一个特征或者单词出现的可能性与它和其他单词相邻没有关系；而且每个特征同等重要
'''

def load_dataset():
    posting_list = [
    ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
    ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
    ['my', 'dalmation', 'is', 'so', 'cute', 'i', 'love', 'him'],
    ['stop', 'posting',' stupid', 'worthless', 'garbage'],
    ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
    ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
    ]
    # 1代表侮辱性文字，0代表正常言论
    class_vec = [0,1,0,1,0,1]
    return posting_list, class_vec

def create_vocab_list(dataset):
    vacab_set = set([])
    for ducument in dataset:
        vacab_set = vacab_set | set(ducument)
    return list(vacab_set)

# 词集模型
def set_of_words2vec(vocab_list, input_set):
    return_vec = [0]*len(vocab_list)
    for word in input_set:
        if word in vocab_list:
            return_vec[vocab_list.index(word)] = 1
        else:
            print 'the word: %s is not in my vocabulary!' % word
    return return_vec

def test0():
    posting_list, class_vec = load_dataset()
    my_vocab_list = create_vocab_list(posting_list)
    print my_vocab_list
    print posting_list[0]
    print set_of_words2vec(my_vocab_list, posting_list[0])

def train_naive_bayes(train_matrix, train_category):
    num_train_docs = len(train_matrix)
    num_words = len(train_matrix[0])
    p_abusive = sum(train_category)/float(num_train_docs)
    # 利用贝叶斯分类器对文档进行分类时，计算多个概率的乘积以获得文档属于某个类别的概率
    # 即计算p(w0|1)p(w1|1)p(w2|1)...
    # 防止其中一个概率值为0，导致最后乘积为0，我们将所有词出现数初始化为1，分母初始化为2
    # p_0num = np.zeros(num_words)
    # p_1num = np.zeros(num_words)
    # p_0denom = 0.0
    # p_1denom = 0.0
    p_0num = np.ones(num_words)
    p_1num = np.ones(num_words)
    p_0denom = 2.0
    p_1denom = 2.0
    # 计算：在给定文档类别条件下，词汇表中的单词出现的概率
    for i in range(num_train_docs):
        if train_category[i] == 1:
            p_1num += train_matrix[i]
            p_1denom += sum(train_matrix[i])
        else:
            p_0num += train_matrix[i]
            p_0denom += sum(train_matrix[i])
    # 防止过多很小的数相乘造成下溢出，我们解决方法是对乘积取自然对数   
    # p_1vect = p_1num / p_1denom
    # p_0vect = p_0num / p_0denom
    p_1vect = np.log(p_1num / p_1denom)
    p_0vect = np.log(p_0num / p_0denom)
    return p_0vect, p_1vect, p_abusive

def test1():
    posting_list, class_vec = load_dataset()
    my_vocab_list = create_vocab_list(posting_list)
    train_mat = []
    for posting_doc in posting_list:
        train_mat.append(set_of_words2vec(my_vocab_list, posting_doc))
    # print train_mat
    p0v, p1v, pab = train_naive_bayes(train_mat, class_vec)
    print p0v
    print p1v
    print pab

def classify_navie_bayes(vec2classify, p_0vect, p_1vect, p_class1):
    p1 = np.sum(vec2classify*p_1vect) + np.log(p_class1)
    p0 = np.sum(vec2classify*p_0vect) + np.log(1.0-p_class1)
    if p1 > p0:
        return 1
    else:
        return 0

def test_navie_bayes():
    posting_list, class_vec = load_dataset()
    my_vocab_list = create_vocab_list(posting_list)
    train_mat = []
    for posting_doc in posting_list:
        train_mat.append(set_of_words2vec(my_vocab_list, posting_doc))
    p0v, p1v, pab = train_naive_bayes(np.array(train_mat), np.array(class_vec))
    test_entry = ['love', 'my', 'dalmation']
    this_doc = np.array(set_of_words2vec(my_vocab_list, test_entry))
    print test_entry, ' classified as: ', classify_navie_bayes(this_doc, p0v, p1v, pab)
    test_entry = ['stupid', 'garbage']
    this_doc = np.array(set_of_words2vec(my_vocab_list, test_entry))
    print test_entry, ' classified as: ', classify_navie_bayes(this_doc, p0v, p1v, pab)

# 词袋模型
def bag_of_words2vec(vocab_list, input_set):
    return_vec = [0]*len(vocab_list)
    for word in input_set:
        if word in vocab_list:
            return_vec[vocab_list.index(word)] += 1
    return return_vec

# 使用朴素贝叶斯过滤垃圾邮件
def text_parse(big_string):
    import re
    list_of_tokens = re.split(r'\W*', big_string)
    return [tok.lower() for tok in list_of_tokens if len(tok)>2]

def spam_test():
    doc_list = []
    class_list = []
    full_text = []
    for i in range(1, 26):
        word_list = text_parse(open('email/spam/%d.txt' % i).read())
        doc_list.append(word_list)
        full_text.extend(word_list)
        class_list.append(1)
        word_list = text_parse(open('email/ham/%d.txt' % i).read())
        doc_list.append(word_list)
        full_text.extend(word_list)
        class_list.append(0)
    vocab_list = create_vocab_list(doc_list)
    training_set = range(50)
    test_set = []
    # 随机选取10个测试集
    for i in range(10):
        rand_index = int(random.uniform(0, len(training_set)))
        test_set.append(training_set[rand_index])
        del(training_set[rand_index])
    train_mat = []
    train_classes = []
    for doc_index in training_set:
        train_mat.append(set_of_words2vec(vocab_list, doc_list[doc_index]))
        train_classes.append(class_list[doc_index])
    p0v, p1v, pspam = train_naive_bayes(np.array(train_mat), np.array(train_classes))
    error_count = 0
    for doc_index in test_set:
        word_vector = set_of_words2vec(vocab_list, doc_list[doc_index])
        if classify_navie_bayes(np.array(word_vector), p0v, p1v, pspam) != class_list[doc_index]:
            error_count += 1
    print 'the error rate is: ', float(error_count)/len(test_set)

def test2():
    spam_test()

test2()