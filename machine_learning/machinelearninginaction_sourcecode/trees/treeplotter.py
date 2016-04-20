#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from trees import *

decision_node = dict(boxstyle="sawtooth", fc="0.8")
leaf_node = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plot_node(nodetxt, centerpt, parentpt, nodetype):
    create_plot.ax1.annotate(nodetxt, xy=parentpt, xycoords='axes fraction',
        xytext=centerpt, textcoords='axes fraction',
        va="center", ha="center", bbox=nodetype, arrowprops=arrow_args)

def create_plot():
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    create_plot.ax1 = plt.subplot(111, frameon=False)
    plot_node('a decision_node', (0.5, 0.1), (0.1, 0.5), decision_node)
    plot_node('a leaf node', (0.8, 0.1), (0.3, 0.8), leaf_node)
    plt.show()

def test0():
    create_plot()

def retrieve_tree(i):
    list_of_trees = [
    {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
    {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
    ]
    return list_of_trees[i]

def plot_mid_text(cntrpt, parentpt, txtstring):
    xmid = (parentpt[0] - cntrpt[0]) / 2.0 + cntrpt[0]
    ymid = (parentpt[1] - cntrpt[1]) / 2.0 + cntrpt[1]
    create_plot.ax1.text(xmid, ymid, txtstring)

def plot_tree(my_tree, parentpt, nodetxt):
    num_leafs = get_num_leafs(my_tree)
    depth = get_tree_depth(my_tree)
    first_str = my_tree.keys()[0]
    cntrpt = (plot_tree.xOff + (1.0 + float(num_leafs))/2.0/plot_tree.totalW, plot_tree.yOff)
    plot_mid_text(cntrpt, parentpt, nodetxt)
    plot_node(first_str, cntrpt, parentpt, decision_node)
    second_dict = my_tree[first_str]
    plot_tree.yOff = plot_tree.yOff - 1.0/plot_tree.totalD
    for key in second_dict:
        if type(second_dict[key]).__name__ == 'dict':
            plot_tree(second_dict[key], cntrpt, str(key))
        else:
            plot_tree.xOff = plot_tree.xOff + 1.0/plot_tree.totalW
            plot_node(second_dict[key], (plot_tree.xOff, plot_tree.yOff), cntrpt, leaf_node)
            plot_mid_text((plot_tree.xOff, plot_tree.yOff), cntrpt, str(key))
    plot_tree.yOff = plot_tree.yOff + 1.0/plot_tree.totalD

def create_plot(in_tree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    create_plot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plot_tree.totalW = float(get_num_leafs(in_tree))
    plot_tree.totalD = float(get_tree_depth(in_tree))
    plot_tree.xOff = -0.5/plot_tree.totalW;
    plot_tree.yOff = 1.0
    plot_tree(in_tree, (0.5, 0.1), '')
    plt.show()

def test1():
    my_tree = retrieve_tree(0)
    # my_tree['no surfacing'][3] = 'maybe'
    create_plot(my_tree)

test1()
