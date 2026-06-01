-- TOTAL CUSTOMERS & OVERALL CHURN 
SELECT  
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    ROUND(AVG(Exited) * 100,2) AS 
Churn_Rate_Percent
FROM customers;

-- GEOGRAPHY AND GENDER RISK ANALYSIS
SELECT 
    Geography,
    Gender,
    COUNT(*) AS Customers,
    ROUND(AVG(Exited) * 100,2) AS Churn_Rate
FROM customers
GROUP BY Geography, Gender
ORDER BY Churn_Rate DESC;

-- CHURN BY AGE GROUP
SELECT 
    CASE 
    	WHEN Age < 30 THEN 'Under 30'
    	WHEN Age BETWEEN 30 AND 39 THEN '30-39'
    	WHEN Age BETWEEN 40 AND 49 THEN '40-49'
    	ELSE '50+'
    END AS Age_Group,
    COUNT(*) AS Customers,
    ROUND(AVG(Exited) * 100,2) AS Churn_Rate
    FROM customers
    GROUP BY Age_Group
    ORDER BY Churn_Rate DESC;
    
-- CHURN BY CREDIT SCORE GROUP
SELECT    
    CASE 
    	WHEN CreditScore < 500 THEN 'Poor'
    	WHEN CreditScore < 650 THEN 'Fair'
    	WHEN CreditScore < 750 THEN 'Good'
    	ELSE 'Excellent'  
    END AS Credit_Group,
    COUNT(*) AS Customers,
    ROUND(AVG(Exited) * 100,2) AS Churn_Rate
FROM customers
GROUP BY Credit_Group 
ORDER BY Churn_Rate DESC;

-- AVERAGE BALANCE BY CHURN STATUS
SELECT 
    Exited,
    ROUND(AVG(Balance),2) AS Avg_Balance
FROM customers
GROUP BY Exited;

-- AVERAGE SALARY BY CHURN STATUS
SELECT  
    Exited,
    ROUND(AVG(EstimatedSalary),2) AS 
Avg_Salary
FROM customers
GROUP BY Exited;

-- CHURN RATE BY NUMBER OF PRODUCTS
SELECT  
    NumOfProducts,
    COUNT(*) as Customers,
    ROUND(AVG(Exited) * 100,2) AS Churn_Rate
FROM customers
GROUP BY NumOfProducts 
ORDER BY NumOfProducts;

-- CHURN BY ACTIVE MEMBER
SELECT 
   IsActiveMember,
   COUNT(*) as Customers,
   ROUND(AVG(Exited) * 100,2) AS 
Churn_Rate
FROM customers
GROUP BY IsActiveMember;

-- TOP 10 HIGHEST BALANCE CUSTOMERS
SELECT 
    CustomerId,
    Surname,
    Geography,
    Gender,
    Balance,
FROM customers
ORDER BY Balance DESC 
LIMIT 10; 

-- TENURE ANALYSIS
SELECT
    Tenure,
    COUNT(*) AS Customers,
    ROUND(AVG(Exited) * 100,2) AS Churn_Rate
FROM customers
GROUP BY Tenure 
ORDER BY Tenure;

-- HIGH RISK CUSTOMER SEGMENT
SELECT 
    Geography,
    IsActiveMember,
    ROUND(AVG(Exited) * 100,2) AS Churn_Rate
FROM customers
GROUP BY Geography,IsActiveMember
ORDER BY Churn_Rate DESC;
    

