/* Expert SQL: Extracting Transactional Data for Market Basket Analysis 
This script prepares the raw Online Retail data by filtering out 
cancellations and focusing on the France region for pattern stability.
*/

WITH CleanedTransactions AS (
    SELECT 
        InvoiceNo,
        Description,
        Quantity,
        Country
    FROM online_retail_db.transactions
    WHERE Description IS NOT NULL
      AND InvoiceNo NOT LIKE 'C%'  -- Exclude cancellations
      AND Quantity > 0             -- Ensure positive purchase magnitude
)
SELECT 
    InvoiceNo,
    Description,
    SUM(Quantity) as TotalQuantity
FROM CleanedTransactions
WHERE Country = 'France'
GROUP BY InvoiceNo, Description
ORDER BY InvoiceNo;