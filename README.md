# DataMining2-FrequentItemsets-AssociationRules
The problem of discovering association rules between itemsets in a sales transaction database:  
1. Implement the A-Priori algorithm for finding frequent itemsets with support at least s in a dataset of sales transactions.  
2. Develop and implement an algorithm for generating association rules between frequent itemsets discovered using the A-Priori algorithm in a dataset of sales transactions.  

## Dataset
`Groceries_dataset.csv`  
Data source from: https://www.kaggle.com/datasets/heeraldedhia/groceries-dataset   
The experiments were performed on the Groceries Dataset, containing:  
    - 14,963 transactions  
    - Each transaction is combined by (Member_number, Date)  
    - Average basket size is small (≈4 items), which makes the dataset sparse  
    - The dataset contains 169 unique product categories  

## Running
`python3 main.py --input Groceries_dataset.csv --min_support 10 --min_confidence 0.2`  

## Struction
project/  
│── apriori.py      # Frequent itemsets  
│── rules.py        # Association rule generation (bonus)  
│── main.py         # Main：read dataset and run  
│── Groceries_dataset.csv       # Dataset  

## Input
1. Apriori:   
   1. dataset:`Groceries_dataset.csv`  
   2. Minimum support: `min_support 20`  
2. Rules:   
   1. dataset:`Groceries_dataset.csv`  
   2. Minimum support: `min_support 10`  
   3. Minimum confidence: `min_confidence 0.2`  

## Output
1. Number of frequent itemsets  
2. Frequent 2-itemsets  
3. Frequent 3-itemsets  
4. Association Rules within minimum confidence  

# Evaluation
- Association rule mining generated 8 meaningful rules with confidence ≥0.2.  
- Whole milk appears in almost all rules because:  
    It has very high global support  
    Many smaller itemsets overlap with it by chance  
    But this does not imply causality — only co-occurrence.   
- Using min_support = 10 was essential:  
    If support ≥20, most 3-itemsets disappear  
    If support ≥50, almost no 2-itemsets remain  
- Due to the sparsity and diversity of the dataset, confidences remain moderate (0.2–0.34), which is consistent with known results of the Groceries dataset.  
