import numpy as np

import collections
import os

from sklearn.model_selection import train_test_split
from decision_tree import train_decision_tree, test_decision_tree, test_decision_tree_with_node

if __name__ == '__main__' :
    select_file = int (input ("Choose a valid option \n1. Adults Dataset \n2. Other Dataset (make sure you preprocessed the dataset)\n"))
    if select_file == 1 :
        file_name = "Dataset/processed_adults.txt"
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
        line = list (map (int, line.strip().split (' ')))
        
        data.append (line)

    print ("\nFollowing are the correlation among the output and input attributes - \n")
    x = np.array (data)
    for i in range (x.shape[1]-1) :
        attribute_1 = x[:, i]
        attribute_2 = x[:, -1]

        print ("Correlation between data at index", i, "and outputs =", np.corrcoef (attribute_1, attribute_2)[1, 0])
    print ("It is recommended to not to use data with correlation less that 0.01\n")

    train_inputs, test_inputs, train_y, test_y = train_test_split (np.array (data) [:, :-1], np.array (data) [:, -1], test_size=0.2)

    print ("Splitted the dataset into 80/20 ratio -")
    print ("Nmumber of training examples -", len (train_inputs), "\nNumber of testing examples -", len (test_y), "\n")

    choice = int (input ("Choose a valid option \n1. Train the model \n2. Test the best model \n3. Test for different number of nodes\n"))

    if choice == 1 :
        train_decision_tree (train_inputs, train_y)
        print ("The model is saved as model.pkl")
    elif choice == 2 :
        test_decision_tree_with_node (train_inputs, train_y, test_inputs, test_y)
    elif choice == 3 :
        test_decision_tree (train_inputs, train_y, test_inputs, test_y)
    else :
        print ("Wrong Choice !")
        exit(0)