def calculate_support (candidate_itemsets, transactions, min_sup) :
    ci_sup = {}

    for transaction in transactions :
        for i, candidate_item in enumerate (candidate_itemsets) :
            if set (candidate_item).issubset (transaction) :
                if tuple (candidate_item) in ci_sup.keys() :
                    ci_sup[tuple (candidate_item)] += 1
                else :
                    ci_sup[tuple (candidate_item)] = 1

    items = list (ci_sup.keys())

    for i in items :
        if ci_sup[i] < min_sup * TOTAL_TRANSACTIONS :
            del ci_sup[i]

    return ci_sup

def prefix_match (item1, item2) :
    for i in range (len (item1) - 1) :
        if item1[i] != item2[i] :
            return False

    return True

def not_redundant (item1, item2, items) :
    if not ((item1[:-1] + item2[-1:]) in items and (item2[:-1] + item1[-1:]) in items) :
        return True

    for i in range (len (item1) - 1) :
        current_item = item1[:i] + item1[i+1:] + item2[-1:]
        if not (current_item in items) :
            return False

    return True
    

def extend_prefix_tree (items) :
    candidate_itemsets = []
    for i, item1 in enumerate (items) :
        for j, item2 in enumerate (items) :
            if j <= i :
                continue

            if isinstance (item1, int) :
                item1 = [item1]
            elif isinstance (item1, tuple) :
                item1 = list (item1)

            if isinstance (item2, int) :
                item2 = [item2]
            elif isinstance (item2, tuple) :
                item2 = list (item2)
            
            
            if prefix_match (item1, item2) :
                if not_redundant (item1, item2, items) :

                    candidate_itemsets.append ((item1 + item2[-1:]))
                    candidate_itemsets[-1].sort ()

    return candidate_itemsets

def initialize_apriori (transactions) :
    candidate_itemsets = {}
    for transaction in transactions :
        for item in transaction :
            item = tuple ([item])
            if item in candidate_itemsets.keys() :
                candidate_itemsets[item] += 1
            else :
                candidate_itemsets[item] = 1

    ci_list = list (candidate_itemsets.keys())
    for item in ci_list :
        if candidate_itemsets[item] < min_sup * TOTAL_TRANSACTIONS :
            del candidate_itemsets[item]

    return candidate_itemsets

def apriori (transactions, min_sup_) :
    global TOTAL_TRANSACTIONS, min_sup
    TOTAL_TRANSACTIONS = len (transactions)
    min_sup = min_sup_

    frequent_itemsets = []
    
    candidate_itemsets = initialize_apriori (transactions)
    k = 1

    while len (candidate_itemsets) != 0 :

        frequent_itemsets.extend (list (candidate_itemsets.items()))

        candidate_itemsets = extend_prefix_tree (list (candidate_itemsets.keys()))
        candidate_itemsets = calculate_support (candidate_itemsets, transactions, min_sup_)
        k += 1

    return frequent_itemsets

TOTAL_TRANSACTIONS = 0
min_sup = 0