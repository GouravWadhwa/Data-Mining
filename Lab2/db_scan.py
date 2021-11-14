import numpy as np
import random

def distance_l1 (point1, point2) :
    return np.mean (np.abs (point1 - point2))

def calculate_neigbours (data, epsilon, index) :
    neighbours = []
    for i in range (data.shape[0]) :
        if distance_l1 (data[index], data[i]) < epsilon :
            neighbours.append (i)

    return neighbours

def density_connected (n_points, visited, index, min_points) :
    connected_points = []
    connected_points.extend (n_points[index])
    visited[index] = True 
    for neighbour in n_points[index] :
        if visited[neighbour] == True :
            continue
        if len (n_points[neighbour]) >= min_points :
            connected_points.extend (density_connected (n_points, visited, neighbour, min_points))
    
    return connected_points

def db_scan (data, epsilon, min_points) :
    core_points = set ()
    ids = [0] * data.shape[0]
    neighbourhood_points = {}

    data = np.array (data)
    n = data.shape[0]
    dim = data.shape[1]

    for i in range (n) :
        neighbourhood_points[i] = calculate_neigbours (data, epsilon, i)
        if len (neighbourhood_points[i]) >= min_points :
            core_points.add (i)

        ids[i] = 0

    cludter_id = 0
    for core_pt in core_points :
        if ids[core_pt] != 0 :
            continue
        
        cludter_id += 1
        ids[core_pt] = cludter_id

        visited = [False] * n

        conncted_pts = density_connected (neighbourhood_points, visited, core_pt, min_points)
        for point in conncted_pts :
            ids[point] = cludter_id
    
    return ids

def apply_db_scan (data_x, data_y, epsilon, min_points) :
    ids = db_scan (data_x, epsilon, min_points)
    return np.array (ids) - 1
