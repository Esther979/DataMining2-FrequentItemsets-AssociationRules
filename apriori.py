from collections import defaultdict
import argparse
import time
import csv


# 得到 1-项候选集

def get_frequent_1_itemsets(transactions, min_support):
   
    counts = defaultdict(int)
    for t in transactions:
        for item in t:
            counts[frozenset([item])] += 1

    L1 = {itemset: count for itemset, count in counts.items()
          if count >= min_support}
    return L1



# 生成候选 k-项集

def generate_candidates(prev_frequents, k):
    
    prev_itemsets = list(prev_frequents)
    candidates = set()
    n = len(prev_itemsets)

    for i in range(n):
        for j in range(i + 1, n):
            l1 = sorted(list(prev_itemsets[i]))
            l2 = sorted(list(prev_itemsets[j]))

            # Join 条件：前 k-2 项相同
            if l1[:k - 2] == l2[:k - 2]:
                new_itemset = frozenset(prev_itemsets[i] | prev_itemsets[j])

                if len(new_itemset) == k:
                    # prune：检查所有子集是否都频繁
                    all_subsets_frequent = True
                    for item in new_itemset:
                        subset = new_itemset - {item}
                        if subset not in prev_frequents:
                            all_subsets_frequent = False
                            break
                    if all_subsets_frequent:
                        candidates.add(new_itemset)

    return candidates



# 统计候选项集支持度

def count_support(candidates, transactions, min_support):
    
    counts = defaultdict(int)

    for t in transactions:
        for c in candidates:
            if c.issubset(t):
                counts[c] += 1

    Lk = {itemset: count for itemset, count in counts.items()
          if count >= min_support}
    return Lk



# Apriori 

def apriori(transactions, min_support):
    
    frequent_itemsets = {}

    # 计算 L1
    Lk = get_frequent_1_itemsets(transactions, min_support)
    k = 1

    while Lk:
        frequent_itemsets.update(Lk)
        k += 1

        # 由 L(k-1) 生成 C(k)
        Ck = generate_candidates(set(Lk.keys()), k)
        if not Ck:
            break

        # 统计 C(k) 支持度得到 L(k)
        Lk = count_support(Ck, transactions, min_support)

    return frequent_itemsets


