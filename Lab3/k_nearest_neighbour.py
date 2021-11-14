import collections
import heapq

import numpy as np

import random
from tqdm import tqdm

def calculate_dist (a, b) :
    return np.mean ((a - b)**2)

def knn (train_inputs, train_y, test_inputs, k) :
    train_inputs = np.array (train_inputs)
    train_y = np.array (train_y)
    test_inputs = np.array (test_inputs)

    n_train = train_inputs.shape[0]
    n_test = test_inputs.shape[0]

    predictions = [None] * n_test
    for i in tqdm (range (n_test)) :
        min_dis = [(float ("inf"), None) for _ in range(k)]
        for j in range (n_train) :
            distance = calculate_dist (train_inputs[j], test_inputs[i])
            for l in range (k) :
                if min_dis[l][0] > distance :
                    min_dis[l] = (distance, train_y[j])
                    break
        
        classes = collections.defaultdict (int)
        for l in range (k) :
            classes[min_dis[l][1]] += 1
        
        predictions[i] = max (classes, key=lambda x: classes[x])
        
    return predictions