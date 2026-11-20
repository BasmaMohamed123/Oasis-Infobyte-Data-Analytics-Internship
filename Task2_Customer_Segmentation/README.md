# Task 2: Customer Segmentation

## Project Overview
This project applies customer segmentation using RFM (Recency, Frequency, Monetary) analysis and K-Means clustering to identify customer groups based on purchasing behavior.

## Dataset
- **Source:** UCI Machine Learning Repository – Online Retail
- **Link:** https://archive.ics.uci.edu/dataset/352/online-retail
- **Original records:** 541,909 transactions
- **Cleaned records:** 397,884 transactions
- **Unique customers:** 4,338

The dataset contains transactions from a UK-based online retailer between December 2010 and December 2011.

## Methodology
1. Data loading and exploration.
2. Data cleaning: removed cancelled invoices, missing customer IDs, returns, and non-positive prices.
3. Calculated RFM metrics:
   - Recency: Days since the customer's last purchase.
   - Frequency: Number of unique invoices.
   - Monetary: Total customer spending.
4. Applied log transformation and StandardScaler.
5. Used the Elbow Method and Silhouette Score to evaluate the number of clusters.
6. Applied K-Means clustering with 2 clusters.
7. Profiled the resulting customer segments and developed business recommendations.

## Key Findings

| Metric | Cluster 0 | Cluster 1 |
|---|---:|---:|
| Customers | 2,671 | 1,667 |
| Customer Percentage | 61.57% | 38.43% |
| Average Recency (days) | 134.14 | 25.88 |
| Average Frequency | 1.67 | 8.44 |
| Average Spending | £497.74 | £4,548.26 |
| Revenue Contribution | 14.92% | 85.08% |

- Cluster 0 represents less-engaged customers with lower purchase frequency and spending.
- Cluster 1 represents active, high-value customers who purchase more frequently and contribute most of the revenue.
- 38.43% of customers generate 85.08% of total revenue.

## Business Recommendations
- **Cluster 1:** Focus on customer retention through loyalty programs, personalized rewards, and exclusive offers.
- **Cluster 0:** Use targeted re-engagement campaigns and promotions to encourage repeat purchases.

## Project Structure
- data/: Original dataset.
- 
otebooks/: Customer segmentation analysis notebook.
- outputs/: Exported customer segments, cluster summary, and visualizations.

## Tools & Libraries
Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, Jupyter Notebook.

## Dataset Attribution
Online Retail dataset by the UCI Machine Learning Repository, licensed under CC BY 4.0.
