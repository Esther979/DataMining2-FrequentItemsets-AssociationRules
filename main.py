import argparse
import time
import csv
from collections import defaultdict

from apriori import apriori
from rules import generate_association_rules


# Load Dataset

'''
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
# CSV format
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

# main

def main():
    parser = argparse.ArgumentParser(description="Apriori Frequent Itemset Mining")
    parser.add_argument("--input", required=True,
                        help="Path to the dataset file, e.g., Groceries_dataset.csv")
    parser.add_argument("--min_support", type=int, required=True,
                        help="Minimum support threshold (absolute number)")
    parser.add_argument("--min_confidence", type=float, default=0.2)

    args = parser.parse_args()

    print("Loading dataset...")
    start_time = time.time()

    transactions = load_transactions(args.input)
    print(f"Dataset loaded successfully. Total transactions: {len(transactions)}")

    print(f"Running Apriori with min_support = {args.min_support} ...")
    frequent_itemsets = apriori(transactions, args.min_support)

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

    # ---------------------------------------------------------
    # Generate Association Rules X → Y
    # ---------------------------------------------------------
    print(f"\nGenerating Association Rules (min_confidence = {args.min_confidence})...")
    rules = generate_association_rules(frequent_itemsets, args.min_confidence)
    print(f"Total rules generated: {len(rules)}\n")

    rules_sorted = sorted(rules, key=lambda x: (-x[3], -x[2]))

    print("===== TOP 50 RULES =====")
    for X, Y, supp, conf in rules_sorted[:50]:
        print(f"{set(X)} → {set(Y)} | support={supp}, confidence={conf:.3f}")

    end_time = time.time()
    print(f"\nExecution time: {end_time - start_time:.2f}s")



if __name__ == "__main__":
    main()

