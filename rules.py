from itertools import combinations

# BONUS: Generate Association Rules (X → Y)

def generate_association_rules(frequent_itemsets, min_confidence):
    rules = []

    for itemset, support_xy in frequent_itemsets.items():
        if len(itemset) < 2:
            continue  # need at least 2 items to form rule

        items = list(itemset)

        # Generate all non-empty proper subsets
        for i in range(1, len(items)):
            for X in combinations(items, i):
                X = frozenset(X)
                Y = itemset - X

                support_X = frequent_itemsets.get(X, 0)
                if support_X == 0:
                    continue

                confidence = support_xy / support_X

                if confidence >= min_confidence:
                    rules.append((X, Y, support_xy, confidence))

    return rules
