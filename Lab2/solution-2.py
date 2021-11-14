import numpy as np
import os

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from em_clustering import expected_maximization_function
from em_clustering import expected_maximization
from denclue import denclue_density_function

from sklearn.decomposition import PCA
from tqdm import tqdm

if __name__ == "__main__" :
    print ("Choose one of the folowing datasets \n1. Iris Dataset \n2. Spiral Dataset\n3. Different Dataset")
    n = int (input ())
    k = None

    file_name = None
    if n == 1 :
        file_name = "Datasets/iris.txt"
        k = 3
    elif n == 2 :
        file_name = "Datasets/2Dspiral.txt"
        k = 2
    elif n == 3 :
        file_name = input ("Enter the name of the file : ")
        if not os.path.isfile (file_name) :
            print ("No file exists!\n")
            exit (0)
        k = int (input ("Please enter the value of k"))
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

    pca = PCA (n_components=2)
    pca.fit (dataset_x)
    dataset_x = pca.transform (dataset_x)

    print ("Choose the algorithm for which you want to plot the PDF \n1. Expected Maximization \n2. Denclue")
    algo = int (input ())

    x = np.linspace (-5, 5, 100)
    y = np.linspace (-5, 5, 100)

    X, Y = np.meshgrid (x, y)

    if algo == 1 :
        means, sigma, pp = expected_maximization (dataset_x, k, epsilon=1e-2)
        z = np.array ([expected_maximization_function (means, sigma, pp, [a, b]) for a, b in tqdm (zip (np.ravel (X), np.ravel (Y)))])
    elif algo == 2 :
        z = np.array ([denclue_density_function (dataset_x, [a, b], 0.2) for a, b in tqdm (zip (np.ravel (X), np.ravel (Y)))])
    Z = z.reshape (X.shape)

    fig = plt.figure (figsize=(20, 10))
    ax = fig.add_subplot (111, projection='3d')

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='b', alpha=0.2)
    plt.savefig ("em_iris.jpg")
    plt.show ()