-- Impala SQL: Sales Analysis with Analytic Functions
-- Demonstrates window functions, partitioning, and ranking in Apache Impala

SELECT
  store_id,
  product_category,
  sales_month,
  total_sales,
  SUM(total_sales) OVER (
    PARTITION BY store_id, product_category
    ORDER BY sales_month
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total,
  RANK() OVER (
    PARTITION BY store_id
    ORDER BY total_sales DESC
  ) AS sales_rank,
  ROUND(
    total_sales / SUM(total_sales) OVER (PARTITION BY store_id) * 100,
    2
  ) AS pct_of_store_total
FROM monthly_sales
WHERE sales_year = 2023
  AND total_sales > 0
ORDER BY store_id, product_category, sales_month;
