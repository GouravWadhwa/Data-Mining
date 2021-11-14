import numpy as np

import collections
import copy
import pickle

import matplotlib.pyplot as plt

class Node () :
    def __init__ (self) :
        self.split = None
        self.index = None
        self.left = None
        self.right = None
        self.pos_prob = None
        self.neg_prob = None
        self.train_accuracy = None

def entropy (data) :
    n = data.shape[0]
    entropy = 0

    grouped_data = collections.defaultdict (int)
    for i in range (n) :
        grouped_data[data[i][-1]] += 1
    
    for key in grouped_data.keys() :
        if grouped_data[key] != 0 :
            entropy -= (grouped_data[key] / n) * np.log2 (grouped_data[key] / n)

    return entropy

def calculate_gain (data, column, split, index) :
    n = data.shape[0]
    gain = entropy (data)

    left_data = [[], []]
    right_data = [[], []]
    
    left_data[0] = data[:index+1, :-1].tolist()
    left_data[1] = data[:index+1, -1].tolist()

    right_data[0] = data[index+1:, :-1].tolist()
    right_data[1] = data[index+1:, -1].tolist()

    if len (left_data[0]) != 0 :
        gain = gain - (len (left_data[0]) / n) * entropy (np.hstack ((
            np.array (left_data[0]),
            np.expand_dims (np.array (left_data[1]), axis=-1)
        )))

    if len (right_data[0]) != 0 :
        gain = gain - (len (right_data[0]) / n) * entropy (np.hstack ((
            np.array (right_data[0]),
            np.expand_dims (np.array (right_data[1]), axis=-1)
        )))

    return gain, left_data, right_data


def split_data (data, column) :
    n = data.shape[0]

    max_gain = float ("-inf")

    considered_split = set ()
    for i in range (n-1) :
        split = (float (data[i][column] + float (data[i+1][column]))) / 2

        if split in considered_split :
            continue
        considered_split.add (split)

        gain, left_data, right_data = calculate_gain (data, column, split, i)
        if gain > max_gain :
            max_gain = gain
            info = (gain, split, left_data, right_data)
            
    return info


def generate_best_split (train_inputs, train_y) :
    max_gain = float ("-inf")
    split = None

    train_inputs = np.array (train_inputs)
    train_y = np.array (train_y)

    data = np.concatenate ((train_inputs, np.expand_dims (train_y, axis=-1)), axis=1).tolist ()

    n = train_inputs.shape[0]
    dim = train_inputs.shape[1]

    for j in range (dim) :
        data = sorted (data, key=lambda x: x[j])
        if j == 2 :
            continue
        gain, split_point, left_data, right_data = split_data (np.array (data), j)

        if gain > max_gain :
            max_gain = gain
            split = (split_point, j, left_data, right_data)

    # print ("Choosed Split -> Split Index :", split[1], "Split Point :", split[0])

    return split

def build_tree (train_inputs, train_y, previous="Root") :
    n = len (train_inputs)
    print (previous)

    grouped_data = collections.defaultdict (list)
    for i in range (n) :
        grouped_data[train_y[i]].append (train_inputs[i])

    group_count = len (grouped_data.keys())

    if group_count == 1 :
        return list(grouped_data.keys())[0]
    else :
        node = Node ()
        best_split, best_split_index, left_data, right_data = generate_best_split (train_inputs, train_y)
        
        node.split = best_split
        node.index = best_split_index

        sum_ = sum (train_y)

        node.pos_prob = sum_ / len (train_y)
        node.neg_prob = (len(train_y) - sum_) / len(train_y)

        print ("Left Data -", len (left_data[0]), "Right Data -", len (right_data[0]))

        node.left = build_tree (left_data[0], left_data[1], previous+"->Left")
        node.right = build_tree (right_data[0], right_data[1], previous+"->Right")

        return node

def train_decision_tree (train_inputs, train_y) :
    root = build_tree (train_inputs, train_y)
    
    decision_tree = copy.deepcopy (root)
    pickle.dump (decision_tree, open ('model.pkl', "wb"))

def get_total_nodes (root) :
    if root == None :
        return 0

    if type (root) == int or type (root) == float :
        return 0

    return get_total_nodes (root.left) + get_total_nodes (root.right) + 1

def classify_data_point (root, data, num_nodes) :
    if type (root) == int or type (root) == float :
        return root

    if num_nodes == 0 :
        if root.pos_prob > root.neg_prob :
            return 1
        else :
            return 0

    if data[root.index] < root.split :
        return classify_data_point (root.left, data, num_nodes-1)
    else :
        return classify_data_point (root.right, data, num_nodes-1)

def get_accuracy (root, inputs, y, max_nodes=1000, start=0) :
    accuracy = []
    for i in range (start, max_nodes+1) :
        correct = 0
        for j in range (len (inputs)) :
            pred = classify_data_point (root, inputs[j], i)
            
            if pred == y[j] :
                correct += 1
        print ("Allowed Nodes =", i, "Accuracy =", correct / len (y))
        accuracy.append (correct / len (y))

    return accuracy

def test_decision_tree (train_inputs, train_y, test_inputs, test_y) :
    model = pickle.load (open ('model.pkl', 'rb'))
    
    total_nodes = get_total_nodes (model)
    print ("Out model in total contains -", total_nodes, "nodes")

    print ("Following are the Train accuracies for different allowed nodes")

    train_accuracies = get_accuracy (model, train_inputs, train_y, max_nodes=50)
    plt.plot (train_accuracies)
    plt.savefig ("train_accuracy")
    plt.show ()

    print ("Following are the Test accuracies for different allowed nodes")
    test_accuracies = get_accuracy (model, test_inputs, test_y, max_nodes=100)
    plt.plot (test_accuracies)
    plt.savefig ("test_accuracy")
    plt.show ()

    return train_accuracies, test_accuracies

def test_decision_tree_with_node (train_inputs, train_y, test_inputs, test_y) :
    model = pickle.load (open ('model.pkl', 'rb'))
    
    total_nodes = get_total_nodes (model)
    print ("Out model in total contains -", total_nodes, "nodes")

    print ("Training Accuracy - ")
    get_accuracy (model, train_inputs, train_y, max_nodes=88, start=88)
    print ("Testing Accuracy - ")
    get_accuracy (model, test_inputs, test_y, max_nodes=88, start=88)