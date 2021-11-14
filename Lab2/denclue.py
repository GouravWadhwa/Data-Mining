import random
import numpy as np

def distance_l1 (point1, point2) :
    return np.mean (np.abs (point1 - point2))

def gaussian_kernel (z) :
    d = z.shape[0]
    if len (z.shape) == 1 :
        z = np.expand_dims (z, -1)

    return (1 / np.sqrt (2 * np.pi)**d) * np.exp (-np.dot (np.transpose (z), z))

def threshold_density (data, x_center, h) :
    n = data.shape[0]
    d = data.shape[1]

    probability = 0

    for i in range (n) :
        z = (x_center - data[i]) / h
        probability += gaussian_kernel (z)

    return (probability / n) / (h**d)

def density_attractor (data, index, h, epsilon) :
    attractor = data[x]

    while (True) :
        new_attractor = 0
        num, den = 0, 0
        for i in range (data.shape[0]) :
            z = (attractor - data[i]) / h
            k_z = gaussian_kernel (z)
            num += k_z *attractor
            den += k_z

        new_attractor = num / den
        if distance_l1 (new_attractor, attractor) < epsilon :
            attractor = new_attractor
            break
        
        attractor = new_attractor

def denclue_density_function (data, x, h) :
    f_x = 0
    
    for i in range (data.shape[0]) :
        z = (x - data[i]) / h
        f_x += gaussian_kernel (z)

    return f_x

def denclue (data, h, xi, epsilon) :
    n = data.shape[0]
    dim = data.shape[1]

    attractors = []
    itmes = {}

    for i in range (n) :
        attractor = density_attractor (data, i, h, epsilon)
        if threshold_density (data, attractor, h) > xi :
            if attractor not in attractors :
                attractors.append (attractor)
                if tuple (attractor) not in items :
                    items [tuple (attractor)] = data[i] 

    return attractors, items