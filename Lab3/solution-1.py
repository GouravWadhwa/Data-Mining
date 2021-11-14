import numpy as np

from k_nearest_neighbour import knn
from naive_bayes_classifier import naive_bayes_classifier
from bayes_classifier import bayes_classifier

import random
import os
import time

if __name__ == '__main__' :
    select_file = int (input ("Choose a valid option \n1. Credits Card Dataset \n2. Other Dataset\n"))
    if select_file == 1 :
        file_name = "Dataset/creditcard.csv"
        file = open (file_name, "r")
    elif select_file == 2 :
        file_name = input ("Enter a valid file : ")
        if not os.path.isfile (file_name) :
            print ("No File Exists !")
            exit(0)

        file = open (file_name, "r")
    else :
        print ("Please enter a valid choice !")
        exit(0)

    data = []

    for i, line in enumerate (file.readlines ()) :
        if i == 0 :
            continue
        arr = line.split (",")
        arr[-1] = arr[-1][1]

        data.append (arr)

    algo = int (input ("Enter a valid option \n1. Bayes Algorithm \n2. Naive Bayes Algorithm \n3. K Nearest neighbour Algorithm\n"))

    if algo == 1 or algo == 2 :
        test_ratio_negative = 0.001
        test_ratio_positive = 0.05
    elif algo == 3 :
        test_ratio_negative = 0.001
        test_ratio_positive = 0.05
    else :
        print ("Invalid Choice !")
        exit (0)
    
    data = sorted (data, key=lambda x: x[-1])

    positive_class = 0
    negative_class = 0
    for i in range (len (data)) :
        if data[i][-1] == '0' :
            negative_class += 1
        else :
            positive_class += 1

    test_index = random.sample (range (negative_class), int (negative_class * test_ratio_negative))
    test_index.extend (random.sample (range (negative_class, len(data)), int (test_ratio_positive * positive_class)))

    print ("Training Dataset size - ", len (data) - int (test_ratio_positive * positive_class) + int (test_ratio_negative * negative_class))
    print ("Testing Dataset size - ", int (test_ratio_positive * positive_class) + int (test_ratio_negative * negative_class)) 
    print ("Testing Dataset Positive examples - ", int (test_ratio_positive * positive_class))
    print ("Testing Dataset Negative examples - ", int (test_ratio_negative * negative_class))

    test_index = sorted (test_index)

    train_inputs = []
    train_y = []

    test_inputs = []
    test_y = []

    current = 0

    for i in range (len (data)) :
        if current < len (test_index) and test_index[current] == i :
            test_inputs.append (list (map (float, data[i][1:-1])))
            test_y.append (data[i][-1])
            current += 1
        else :
            train_inputs.append (list (map (float, data[i][1:-1])))
            train_y.append (data[i][-1])

    if algo == 1 :
        prediction = bayes_classifier (train_inputs, train_y, test_inputs)
    elif algo == 2 :
        prediction = naive_bayes_classifier (train_inputs, train_y, test_inputs)
    elif algo == 3 :
        prediction = knn (train_inputs, train_y, test_inputs, 10)

    tp, tn, fp, fn = (0, 0, 0, 0)
    for i in range (len (test_inputs)) :
        if test_y[i] == prediction[i] and test_y[i] == "1" :
            tp += 1
        elif test_y[i] == prediction[i] and test_y[i] == "0" :
            tn += 1
        elif test_y[i] != prediction[i] and test_y[i] == "1" :
            fn += 1
        elif test_y[i] != prediction[i] and test_y[i] == "0" :
            fp += 1

    print ("TP =", tp, "TN =", tn, "FP =", fp, "FN =", fn)
    print ("Precision =", tp / (fp + tp))
    print ("Recall =", tp / (fn + tp))
    print ("F1 Score =", 2 * tp/ (2 * tp + fp + fn))
    print ("Accuracy =", (tp + tn)/(tp+tn+fp+fn))
    print ("jaccard =", tp / (tp + fp + fn))