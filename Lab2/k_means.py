import random
import numpy as np

def calculate_l2_distance (x1, x2) :
    return np.mean ((x1 - x2)**2)

def calculate_l1_distance (x1, x2) :
    return np.mean (np.abs (x1 - x2))

def k_means (data, k) :
    if data.shape[0] == 0 :
        return None

    n = data.shape[0]
    dim = data.shape[1]
    centroids = np.zeros ((k, dim))

    for i in range (k) :
        centroids[i] = np.array (data[i])

    while (True) :
        total_change = 0
        labels = [0 for _ in range (n)]
        clusters = [[] for _ in range (k)]
        for j in range (n) :
            min_distance = None
            index = None

            for i in range (k) :
                distance = calculate_l2_distance (data[j], centroids[i])
                if min_distance == None or min_distance > distance :
                    min_distance = distance
                    index = i
            
            labels[j] = index
            clusters[index].append (data[j])


        for i in range (k) :
            total_sum = np.zeros ((dim, )).astype (float)
            for j in range (len (clusters[i])) :
                for l in range (dim) :
                    total_sum[l] += clusters[i][j][l]
            if len (clusters[i]) != 0 :
                new_centroid = total_sum / len (clusters[i])
            else :
                new_centroid = total_sum
                
            total_change += calculate_l1_distance (centroids[i], new_centroid)
            centroids[i, :] = new_centroid

        if total_change < 1e-10 : 
            return labels, centroids

def apply_k_means (data_x, data_y, k) :
    labels, centroids = k_means (data_x, k)
    sse_loss = SSE_Loss (data_x, centroids, labels)

    return labels, sse_loss

def SSE_Loss (data_x, centroids, labels) :
    loss = 0
    for i in range (data_x.shape[0]) :
        loss += calculate_l1_distance (centroids[labels[i]], data_x[i])

    print ("SSE Loss - " + str (loss))
    return loss