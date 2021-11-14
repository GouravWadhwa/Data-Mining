class FP_Node :
    def __init__ (self, item, count=0, parent=None, link=None) :
        self.item = item
        self.count = count
        self.parent = parent
        self.link = link
        self.children = {}

def make_fp_tree (transactions, min_sup) :
    root = FP_Node (item="Null", count=1, parent=None, link=None)
    items_table = []
    items_dic = {}

    for transaction in transactions :
        for item in transaction :
            if item in items_dic.keys() :
                items_dic[item] += 1
            else :
                items_dic[item] = 1

    items_list = list (items_dic.keys())

    for item in items_list :
        if items_dic[item] < min_sup * TOTAL_TRANSACTIONS :
            del items_dic[item]

    items_sorted = sorted (items_dic.items (), key=lambda x: (-x[1], x[0]))

    items_order = {}
    for i, (item, count) in enumerate (items_sorted) :
        items_order[item] = i
        node = FP_Node (item, count, None, None)
        items_table.append (node)

    for transaction in transactions :
        candidate_items = []
        
        for item in transaction :
            if item in items_dic.keys() :
                candidate_items.append (item)

        if len (candidate_items) == 0 :
            continue

        candidate_items_sorted = sorted (candidate_items, key=lambda x: items_order[x])
        node = root
        for item in candidate_items_sorted :
            if item in node.children.keys() :
                node.children[item].count += 1
                node = node.children[item]
            else :
                node.children[item] = FP_Node (item=item, count=1, parent=node, link=None)
                node = node.children[item]

                for n in items_table :
                    if n.item == node.item :
                        if n.link is None :
                            n.link = node
                        else :
                            node.link = n.link
                            n.link = node

    return root, items_table, items_dic, items_order

def condition_tree_transactions (node) :
    if node.parent == None :
        return None

    node_transactions = []

    while node is not None :
        line = []
        parent_node = node.parent
        while parent_node.parent is not None :
            line.append (parent_node.item)
            parent_node = parent_node.parent

        line = line[::-1]
        for i in range (node.count) :
            node_transactions.append (line)

        node = node.link

    return node_transactions


def find_frequent (root, table, min_sup, parent_node=None) :
    if len (list (root.children.keys())) == 0 :
        return None

    result = []
    reverse_table = table[::-1]


    for n in reverse_table :
        frequent_itemsets = [set (), 0]

        if parent_node == None :
            frequent_itemsets[0] = {n.item,}
        else :
            frequent_itemsets[0] = {n.item}.union (parent_node[0])

        frequent_itemsets[1] = n.count
        result.append (frequent_itemsets)
        ct_transactions = condition_tree_transactions (n.link)
        new_root, new_table, _, _ = make_fp_tree (ct_transactions, min_sup)
        frequent_itemsets = find_frequent (new_root, new_table, min_sup, frequent_itemsets)

        if frequent_itemsets is not None :
            result.extend (frequent_itemsets)

    return result

def fp_tree (transactions, min_sup) :
    global TOTAL_TRANSACTIONS
    TOTAL_TRANSACTIONS = len (transactions)

    root, table, items_dic, items_order = make_fp_tree (transactions, min_sup)

    frequent_itemsets = find_frequent (root, table, min_sup)
    return frequent_itemsets

TOTAL_TRANSACTIONS = 0
min_sup = 0