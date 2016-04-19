#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir
import numpy as np
import operator
import matplotlib
import matplotlib.pyplot as plt

def create_dataset():
    group = np.array([[1.0,1.1], [1.0,1.0], [0,0], [0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def classfiy(inX, dataset, labels, k):
    dataset_size = dataset.shape[0]
    diff_mat = np.tile(inX, (dataset_size,1)) - dataset
    sq_diff_mat = diff_mat**2
    sq_distances =  sq_diff_mat.sum(axis=1)
    distances = sq_distances**0.5
    sorted_dist_indicies = distances.argsort()
    class_count = {}
    for i in range(k):
        vote_label = labels[sorted_dist_indicies[i]]
        class_count[vote_label] = class_count.get(vote_label, 0) + 1
    sorted_class_count = sorted(class_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    # print sorted_class_count
    return sorted_class_count[0][0]

def test0():
    group, labels = create_dataset()
    print classfiy([0,0], group, labels, 3)

def file2matrix(filename):
    fr = open(filename)
    array_lines = fr.readlines()
    number_of_lines = len(array_lines)
    return_mat = np.zeros((number_of_lines, 3))
    class_label_vector = []
    index = 0
    for line in array_lines:
        line = line.strip()
        list_from_line = line.split('\t')
        return_mat[index,:] = list_from_line[0:3]
        class_label_vector.append(int(list_from_line[-1]))
        index += 1
    return return_mat, class_label_vector

def draw_data_set(dating_data_mat, dating_labels):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    print 15.0*np.array(dating_labels)
    ax.scatter(dating_data_mat[:,0], dating_data_mat[:,1], 15.0*np.array(dating_labels), 15.0*np.array(dating_labels))
    plt.show()

def test1():
    dating_data_mat, dating_labels = file2matrix('datingTestSet2.txt')
    draw_data_set(dating_data_mat, dating_labels)

def auto_norm(dataset):
    min_val = dataset.min(0)
    max_val = dataset.max(0)
    ranges = max_val - min_val
    norm_dataset = np.zeros(np.shape(dataset))
    m = dataset.shape[0]
    norm_dataset = dataset - np.tile(min_val, (m,1))
    norm_dataset = norm_dataset / np.tile(ranges, (m,1))
    return norm_dataset, ranges, min_val

def dating_class_test():
    ho_ratio = 0.10
    dating_data_mat, dating_labels = file2matrix('datingTestSet2.txt')
    norm_mat, ranges, min_val = auto_norm(dating_data_mat)
    m = norm_mat.shape[0]
    num_test_vecs = int(m*ho_ratio)
    error_count = 0.0
    for i in range(num_test_vecs):
        classifier_result = classfiy(norm_mat[i,:], norm_mat[num_test_vecs:m,:], dating_labels[num_test_vecs:m], 3)
        print 'the classifier came back with: %d, the real answer is: %d' % (classifier_result, dating_labels[i])
        if classifier_result != dating_labels[i]:
            error_count += 1.0
    print 'the total error rate is %f' % (error_count/float(num_test_vecs))

def test2():
    dating_class_test()

def classify_person():
    result_list = ['not at all', 'in small doses', 'in large doses']
    percent_tats = float(raw_input("percent of time spent playing miles earned video games?"))
    ff_miles = float(raw_input("frequent flier miles earned per year?"))
    ice_cream = float(raw_input("liters of ice cream consumed per year?"))
    dating_data_mat, dating_labels = file2matrix('datingTestSet2.txt')
    norm_mat, ranges, min_val = auto_norm(dating_data_mat)
    in_arr = np.array([ff_miles, percent_tats, ice_cream])
    classifier_result = classfiy((in_arr-min_val)/ranges, norm_mat, dating_labels, 3)
    print 'You will like this person: ', result_list[classifier_result-1]

def test3():
    classify_person()

def img2vector(filename):
    return_vect = np.zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        line_str = fr.readline()
        for j in range(32):
            return_vect[0,32*i+j] = int(line_str[j])
    return return_vect

def test4():
    test_vect = img2vector('testDigits/0_13.txt')
    print test_vect[0,0:31]

def handle_writing_class_test():
    hw_labels = []
    training_file_list = listdir('trainingDigits')
    m = len(training_file_list)
    training_mat = np.zeros((m,1024))
    for i in range(m):
        file_name_str = training_file_list[i]
        file_str = file_name_str.split('.')[0]
        class_num_str = file_str.split('_')[0]
        hw_labels.append(class_num_str)
        training_mat[i,:] = img2vector('trainingDigits/%s' % file_name_str)
    test_file_str = listdir('testDigits')
    error_count = 0.0
    m_test = len(test_file_str)
    for i in range(m_test):
        file_name_str = test_file_str[i]
        file_str = file_name_str.split('.')[0]
        class_num_str = file_str.split('_')[0]
        vector_under_test = img2vector('trainingDigits/%s' % file_name_str)
        classifier_result = classfiy(vector_under_test, training_mat, hw_labels, 3)
        print 'the classifier came back with: %s, the real answer is: %s' % (classifier_result, class_num_str)
        if classifier_result != class_num_str:
            error_count += 1
    print 'the total number of errors is %f' % (error_count)
    print 'the total error rate is %f' % (error_count/float(m_test))

def test5():
    handle_writing_class_test()

test5()