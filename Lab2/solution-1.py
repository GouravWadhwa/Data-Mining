import numpy as np
import os
import time

import matplotlib.pyplot as plt

from k_means import apply_k_means
from db_scan import apply_db_scan

from sklearn.decomposition import PCA

def plot_dataset (x, y, y_cap) :
    _, (ax1, ax2) = plt.subplots (1, 2)
    colors = ["red", "blue", "black", "green", "purple", "orange", "pink", "yellow", "brown", "silver"]
    for i in range (x.shape[0]) :
        color = colors [y[i]]
        ax1.scatter (x[i][0], x[i][1], c=color)
        color = colors [y_cap[i]]
        ax2.scatter (x[i][0], x[i][1], c=color)
    ax1.set_title ("Original Clusters")
    ax2.set_title ("Predicted Clusters")

    plt.savefig ("db_scan_spiral.png")
    plt.show ()

if __name__ == '__main__' :
    k_default = None
    epsilon_default = None 
    min_points_default = None

    print ("Choose one of the folowing datasets \n1. Iris Dataset \n2. Spiral Dataset\n3. Different Dataset")
    n = int (input ())

    file_name = None
    if n == 1 :
        file_name = "Datasets/iris.txt"
        k_default = 3
        epsilon_default = 0.2
        min_points_default = 5
    elif n == 2 :
        file_name = "Datasets/2Dspiral.txt"
        k_default = 10
        epsilon_default = 0.2
        min_points_default = 5
    elif n == 3 :
        file_name = input ("Enter the name of the file : ")
        if not os.path.isfile (file_name) :
            print ("No file exists!\n")
            exit (0)
    else :
        print ("Wrong Choice !!\n")
        exit (0)

    file = open (file_name, "r")
    dataset_x = []
    dataset_y = []
    for line in file.readlines () :
        dataset_x.append (list (map (float, line.split(",")[:-1])))
        dataset_y.append (int (line.split(",")[-1].strip()))

    dataset_x = np.array (dataset_x)
    dataset_y = np.array (dataset_y)

    print ("Choose the algorithm you want to apply -\n1. K-Means \n2. DB-Scan")
    algo = int (input ())

    

    if algo == 1 :
        k = int (input ("Enter the value of K (If want to use the default value enter -1, Don't enter -1 in case of new datasets) - "))
        if k == -1 :
            if k_default is None :
                print ("Cannot use default K for new dataset !!")
                exit (0)
            k = k_default
            
        start_time = time.time ()
        labels, sse = apply_k_means (dataset_x, dataset_y, k)
    elif algo == 2 :
        epsilon = float (input ("Enter the value of epsilon (Enter -1 for using default value) - "))
        min_points = int (input ("Enter minimum points for being core point (Enter -1 for using default value) - "))

        if epsilon == -1 :
            if epsilon_default is None :
                print ("Don't use -1 for new datasets !!")
                exit (0)
            epsilon = epsilon_default
        if min_points == -1 :
            if min_points_default is None :
                print ("Don't use -1 for new datasets !!")
                exit (0)
            min_points = min_points_default

        start_time = time.time ()
        labels = apply_db_scan (dataset_x, dataset_y, epsilon, min_points)
    else :
        print ("Wrong Choice !!")
        exit (0)

    print ("Totol Time taken - ", time.time() - start_time)

    # For Making the SSE loss graph for K-means un comment the following code --
    '''
    sse_loss = []
    for k in range (1, 50) :
        labels, sse = apply_k_means (dataset_x, dataset_y, k)
        sse_loss.append (sse)

    plt.plot (sse_loss)
    plt.savefig ("k-means_spiral.jpg")
    plt.show ()
    '''

    if n == 1 :
        pca = PCA (n_components=2)
        dataset_x = pca.fit_transform (dataset_x)
    plot_dataset (dataset_x, dataset_y, labels)