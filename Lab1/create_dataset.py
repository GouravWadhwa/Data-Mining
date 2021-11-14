import random

variance = 5 

def make_dataset (total_transactions, size_mfi, width_transaction, total_items) :
    transaction_width = []
    
    for i in range (total_transactions) :
        a = random.randint (max (width_transaction - variance, 1), width_transaction + variance)
        transaction_width.append (a)

    mf_items = []
    while (len (mf_items) < size_mfi) :
        a = random.randint (0, total_items - 1)
        if not a in mf_items :
            mf_items.append (a)

    transactions = []
    for i, width in enumerate (transaction_width) :
        transaction = []

        if random.uniform (0, 1) < 0.2 :
            transaction.extend (mf_items)
            width -= size_mfi
        
        while (width > 0) :
            a = random.randint (0, total_items - 1)
            if not a in transaction :
                transaction.append (a)
                width -= 1

        transactions.append (transaction)

    return transactions

if __name__ == '__main__' :
    total_transactions = int (input ("Enter the total number of Transactions : "))
    size_mfi = int (input ("Enter the size of maximal frequent itemset : "))
    width_transaction = int (input ("Enter the average width of the transactions : "))
    total_items = int (input ("Enter the total number of Items : "))

    variance = int (0.2 * width_transaction)

    transactions = make_dataset (total_transactions, size_mfi, width_transaction, total_items)

    file = open ("%dT%dM%dW%dT.txt" %(total_transactions, size_mfi, width_transaction, total_items), "w+")
    for transaction in transactions :
        for item in transaction :
            file.write (str (item) + " ")
        file.write ("\n")

    file.close ()
        