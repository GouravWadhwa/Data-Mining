from apriori import apriori
from fp_tree import fp_tree
from eclat import apply_eclat

import time

def average_width (transactions) :
    width = 0
    for transaction in transactions :
        width += len (transaction)
    return width / len (transactions)

if __name__ == '__main__' :
    input_file = int (input ("Choose one of the following file : \n1. T10I4D100K\n2. T40I10D100K\n3. retail\n4. groceries\n5. Other files\n"))
    min_sup = float (input ("Enter the min_sup : "))

    transactions = []
    delimiter = " "

    if input_file == 1 :
        file = open ("data/T10I4D100K.txt", "r")
    elif input_file == 2 :
        file = open ("data/T40I10D100K.txt", "r")
    elif input_file == 3 :
        file = open ("data/retail.txt", "r")
    elif input_file == 4 :
        file = open ("data/groceries.csv", "r")
        delimiter = ","
    else :
        input_file = input("Enter the file name (with full or relative path) : ")
        file = open (input_file, "r")

    lines = file.readlines ()
    transactions = []

    for i, line in enumerate (lines) :
        transactions.append ([num for num in line.split (delimiter)[:-1]])

    TOTAL_TRANSACTIONS = len (transactions)
    print ("There are a total of %d transactions in this data" %(TOTAL_TRANSACTIONS))
    print ("Average Width of the Dataset is -", average_width (transactions))

    input_algo = int (input ("Enter the Algorithm choice you want to evaluate : \n1. Apriori Algorithm\n2. FP Tree Algorithm\n3. Eclat Algorithm\n"))
    start = time.time ()

    if input_algo == 1 :
        frequent_itemsets = apriori (transactions, min_sup)
    elif input_algo == 2 :
        frequent_itemsets = fp_tree (transactions, min_sup)
    elif input_algo == 3 :
        frequent_itemsets = apply_eclat (transactions, min_sup)
    else :
        print ("-"*10 + "NOT A VALID CHOICE" + "-"*10)
        exit (0)
    print ("Time Taken - ", time.time () - start, " seconds")
    
    if frequent_itemsets is None :
        frequent_itemsets = []

    size_mfi = 0
    for items in frequent_itemsets :
        name = items[0]
        count = items[1]
        if len (name) > size_mfi :
            size_mfi = len (name)

        print ("Frequent Item -", name, " -> ", "Count - ", count) 

    print ("Maximum size of Maximal Frequent Itemset - ", size_mfi)
