import collections
import time

import numpy as np

def normal_distribution (x, mu, sigma) :
    x_m = x - mu
    return (1 / np.sqrt (2 * np.pi * sigma)) * np.exp (- (x_m)**2 / (2 * sigma))

def train_classifier (inputs, y) :
    print ("Training the model ....")
    start = time.time ()

    n = len (inputs)
    m = len (inputs[0])

    subsets = collections.defaultdict (list)
    for i in range (n) :
        subsets[y[i]].append (inputs[i])

    k = len (list (subsets.keys ()))

    prior_probabilities = np.zeros ((k))
    mean = np.zeros ((k, m))
    variance = np.zeros ((k, m))

    subsets_keys = sorted (subsets.keys ())

    for i, key in enumerate (subsets_keys) :
        data = np.array (subsets[key])
        prior_probabilities[i] = data.shape[0] / n

        mean[i, :] = np.mean (data, axis=0)

        Z = data - mean[i, :]
        for j in range (m) :
            variance[i, j] = (1 / data.shape[0]) * np.dot (Z[:, j], Z[:, j])

    print ("Model Trained")
    print ("Total Time taken -", time.time() - start)
    return prior_probabilities, mean, variance, subsets_keys

def naive_bayes_classifier (train_inputs, train_y, test_inputs) :
    pp, mean, variance, classes = train_classifier (train_inputs, train_y)

    start = time.time ()
    print ("Predicting the label of the dataset")
    prediction = [None] * len (test_inputs)
    for i in range (len (test_inputs)) :
        max_prob = None
        for j in range (len (classes)) :
            prob = 1
            for k in range (len (test_inputs[i])) :
                prob = prob * normal_distribution (test_inputs[i][k], mean[j][k], variance[j, k])
            prob = prob * pp[j]
            
            if max_prob == None or max_prob < prob :
                max_prob = prob
                prediction[i] = classes[j]

    print ("Time taken to predict the label of the dataset -", time.time () - start)
    return prediction