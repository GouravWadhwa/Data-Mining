import numpy as np
import collections

from sklearn.model_selection import train_test_split

def get_average (data, column) :
    sum = collections.defaultdict (int)
    for i in range (len (data)) :
        if data[i][column] != ' ?' :
            sum[data[i][column]] += 1

    return max (sum, key=lambda x:sum[x])

if __name__ == '__main__' :
    file_name = "Dataset/adult.csv"
    file = open (file_name, "r")

    data = []
    unique_colums = None

    for i, line in enumerate (file.readlines ()) :
        if i == 0 :
            unique_colums = [[] for _ in range (len (line.split(',')))]
            continue
        line = line.split (',')
        line[-1] = line[-1][:-1]

        for i in range (len (line)) :
            try :
                line[i] = int (line[i])
            except :
                if line[i] not in unique_colums[i] and line[i] != ' ?' :
                    unique_colums[i].append (line[i])
                    line[i] = len (unique_colums[i]) - 1
                elif line[i] != ' ?' :
                    line[i] = unique_colums[i].index (line[i])
        
        data.append (line)

    sorted_data = sorted (data, key=lambda x: x[-1])
    poitive_data = None
    negative_data = None

    for i in range (len (sorted_data)) :
        if sorted_data[i][-1] != sorted_data[i+1][-1] :
            positive_data = sorted_data[0:i+1][:]
            negative_data = sorted_data[i+1:][:]
            break

    for i in range (len (positive_data)) :
        for j in range (len (positive_data[i])) :
            if positive_data[i][j] == ' ?' :
                positive_data[i][j] = get_average (positive_data, j)
        if len (positive_data[i]) != 15 :
            print (i)

    for i in range (len (negative_data)) :
        for j in range (len (negative_data[i])) :
            if negative_data[i][j] == ' ?' :
                negative_data[i][j] = get_average (negative_data, j)

    data = np.concatenate ((np.array (positive_data).astype(int), np.array (negative_data).astype(int)), axis=0)

    write_file = open ("Dataset/processed_adults.txt", "w+")
    write_file2 = open ("Dataset/adults_metadata.txt", "w+")
    
    for i in range (data.shape[0]) :
        for j in range (data.shape[1]) :
            write_file.write (str (data[i][j]) + " ")
        write_file.write ("\n")

    for column in unique_colums :
        for i in column :
            write_file2.write (str (i) + " ")
        write_file2.write ("\n")