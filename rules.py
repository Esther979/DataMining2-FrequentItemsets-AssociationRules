from itertools import combinations

# BONUS: Generate Association Rules (X → Y)

def generate_association_rules(frequent_itemsets, min_confidence):
    rules = [] # Save (X, Y, support_xy, confidence)

    for itemset, support_xy in frequent_itemsets.items():
        if len(itemset) < 2:
            continue  # need at least 2 items to form rule

        items = list(itemset) # # convert the itemset to a list

        # Generate all non-empty proper subsets
        # X∪Y=itemset; X∩Y=∅
        for i in range(1, len(items)): # i = size of subset, from 1 to len(items)-1
            for X in combinations(items, i):
                X = frozenset(X)
                Y = itemset - X # Y = I - X

                support_X = frequent_itemsets.get(X, 0) # Get support of X from the frequent itemsets dictionary
                if support_X == 0: # # if X is not frequent or missing
                    continue

                confidence = support_xy / support_X # compute confidence(X -> Y) = support(X ∪ Y) / support(X)

                if confidence >= min_confidence:
                    rules.append((X, Y, support_xy, confidence)) # keep if confidence > threshold

    return rules
