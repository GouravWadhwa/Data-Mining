def calculate_item_transactions (transactions, min_sup) :
    i_tran = {}
    for i, transaction in enumerate (transactions) :
        for item in transaction :
            item = (item,)
            if item in i_tran.keys() :
                i_tran[item][1] += 1
                i_tran[item][0].append (i)
            else :
                i_tran[item] = [[i], 1] 

    i_tran_list = list (i_tran.keys())

    for item in i_tran_list :
        if i_tran[item][1] < TOTAL_TRANSACTIONS * min_sup :
            del i_tran[item]
    

    i_tran_list = list (i_tran.keys())

    i_tran_diff = {}
    for item in i_tran_list :
        i_tran_diff[item] = [[], i_tran[item][1]]

        point = 0
        for i in range (TOTAL_TRANSACTIONS) :
            
            if point < len (i_tran[item][0]) and i_tran[item][0][point] == i :
                point += 1
            else :
                i_tran_diff[item][0].append (i)

    return i_tran_diff

def prefix_equal (item_1, item_2) :
    if not isinstance (item_1, list) :
        return True
    length = len (item_1) - 1
    for i in range (length) :
        if not item_1[i] == item_2[i] :
            return False

    return True  

def eclat (items_tran, min_sup) :
    frequent_itemsets = []

    items_tran_list = list (items_tran.keys())

    for i, itemA in enumerate (items_tran_list) :
        frequent_itemsets.append ([itemA, items_tran[itemA][1]])
    
        new_items_tran = {}

        for j, itemB in enumerate (items_tran_list) :
            if j <= i :
                continue
            if not prefix_equal (itemA, itemB) :
                continue

            final_item = tuple (itemA[:] + itemB[-1:])
            ct = list (set (items_tran[itemB][0]).difference (set (items_tran[itemA][0])))
            sup = items_tran[itemA][1] - len (ct)

            if sup > TOTAL_TRANSACTIONS * min_sup :
                new_items_tran[final_item] = [ct, sup]
        if len (new_items_tran) != 0 :
            fi = eclat (new_items_tran, min_sup)
            frequent_itemsets.extend (fi)

    return frequent_itemsets

def apply_eclat (transactions, min_sup_) :
    global TOTAL_TRANSACTIONS, min_sup
    TOTAL_TRANSACTIONS = len (transactions)
    min_sup = min_sup_

    items_tran = calculate_item_transactions (transactions, min_sup_)
    return eclat (items_tran, min_sup)

TOTAL_TRANSACTIONS = 0
min_sup = 0