from collections import defaultdict
import argparse
import time
import csv


# 读取数据集

def load_transactions(file_path):
   
    transactions = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items = line.split()
            transactions.append(set(items))
    return transactions
'''
def load_transactions(file_path):
    
    baskets = defaultdict(set)

    with open(file_path, "r") as f:
        reader = csv.DictReader(f)   # 按列名读
        for row in reader:
            member = row["Member_number"]
            date = row["Date"]
            item = row["itemDescription"].strip()

            # 用 (member, date) 作为一个购物 session 的唯一标识
            tid = (member, date)
            baskets[tid].add(item)

    return list(baskets.values())

'''
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



# main

def main():
    parser = argparse.ArgumentParser(description="Apriori Frequent Itemset Mining")
    parser.add_argument("--input", required=True,
                        help="Path to the dataset file, e.g., T10I4D100K.dat")
    parser.add_argument("--min_support", type=int, required=True,
                        help="Minimum support threshold (absolute number)")

    args = parser.parse_args()

    print("Loading dataset...")
    start_time = time.time()

    transactions = load_transactions(args.input)
    print(f"Dataset loaded successfully. Total transactions: {len(transactions)}")

    print(f"Running Apriori with min_support = {args.min_support} ...")
    frequent_itemsets = apriori(transactions, args.min_support)

    end_time = time.time()
    elapsed = end_time - start_time

    print("\n===== Results =====")
    print(f"Number of frequent itemsets: {len(frequent_itemsets)}\n")

    # 按项集大小和字典序排序输出前 50 个
    sorted_itemsets = sorted(
        frequent_itemsets.items(),
        key=lambda x: (len(x[0]), sorted(list(x[0])))
    )

    print("Showing first 50 frequent itemsets:")
    for itemset, support in sorted_itemsets[:50]:
        items = ", ".join(sorted(itemset))
        print(f"{{{items}}}: {support}")

    # ===== 显示 2-itemsets =====
    print("\n===== Frequent 2-itemsets =====")
    for itemset, support in sorted_itemsets:
        if len(itemset) == 2:
            items = ", ".join(sorted(itemset))
            print(f"{{{items}}}: {support}")

# ===== 显示 3-itemsets =====
    print("\n===== Frequent 3-itemsets =====")
    for itemset, support in sorted_itemsets:
        if len(itemset) == 3:
            items = ", ".join(sorted(itemset))
            print(f"{{{items}}}: {support}")


    print(f"\nExecution time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
