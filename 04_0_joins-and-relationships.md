# SQL Joins & Table Relationships

Joins are used to **combine rows from two or more tables** based on related columns, typically via **foreign key relationships**.

---

## Joins

Most joins rely on **relational integrity**, where a **foreign key** in one table points to a **primary key** in another.


## Common SQL Join Types

🧾 customers

| id | name  | lastname | birth_date | hobbies             |
|----|-------|----------|------------|---------------------|
| 1  | Alice | Smith    | 1990-04-15 | reading, hiking     |
| 2  | Bob   | Johnson  | 1985-12-02 | cooking, chess      |
| 3  | Carol | Davis    | 1992-07-23 | yoga, painting      |
| 4  | David | Lee      | 1988-09-10 | cycling, photography|
| 5  | Eve   | Martinez | 1995-03-30 | gaming, running     |

📦 orders

| id | customer_id | Product             | Price  |
|----|-------------|---------------------|--------|
| 1  | 1           | Wireless Mouse      | 25.99  |
| 2  | 2           | Bluetooth Headphones| 59.49  |
| 3  | 3           | Laptop Stand        | 32.00  |
| 4  | 1           | Notebook            | 5.25   |
| 5  | 4           | USB-C Hub           | 45.75  |
| 6  | 999         | Portable Charger    | 29.99  |


### INNER JOIN

- Returns rows where matching values exist in both tables.
- Most common join type.

```sql
SELECT c.name AS Customer, 
       o.product AS Product
FROM customers c 
JOIN orders o ON c.id = o.customer_id;
```

Note: `... JOIN orders ...` or `... INNER JOIN orders ...` is the same.

✅ Returns only matching rows from both tables.

| Customer | Product             |
|----------|---------------------|
| Alice    | Wireless Mouse      |
| Bob      | Bluetooth Headphones|
| Carol    | Laptop Stand        |
| Alice    | Notebook            |
| David    | USB-C Hub           |

•	INNER JOIN returns only the rows where there is a match between the two tables.
•	It returns only the customers who have at least one order, showing each matching pair of customer name and product.
•	If a customer has multiple orders (e.g., Alice), each one appears as a separate row.

---

### LEFT JOIN (LEFT OUTER JOIN)

- Returns all rows from the left table, and matching rows from the right.
- If no match, right-side columns are NULL.

```sql
SELECT c.name AS Customer, 
       o.product AS Product
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;
```

✅ Returns all customers, with orders if they exist.

| Name   | Product             |
|--------|---------------------|
| Alice  | Wireless Mouse      |
| Alice  | Notebook            |
| Bob    | Bluetooth Headphones|
| Carol  | Laptop Stand        |
| David  | USB-C Hub           |
| Eve    | NULL                |


•	A LEFT JOIN includes all rows from the customers table.
•	If a customer has no matching orders, like Eve, you’ll see NULL in the Product column.

---

### RIGHT JOIN (RIGHT OUTER JOIN)

- Returns all rows from the right table, and matching rows from the left.
- Less commonly used than LEFT JOIN.

```sql
SELECT c.name AS Customer, 
       o.product AS Product
FROM customers c
RIGHT JOIN orders o ON c.id = o.customer_id;
```

✅ Returns all orders, including ones with no matching customer.

| Name   | Product             |
|--------|---------------------|
| Alice  | Wireless Mouse      |
| Bob    | Bluetooth Headphones|
| Carol  | Laptop Stand        |
| Alice  | Notebook            |
| David  | USB-C Hub           |
| NULL   | Gaming Chair        |

•	It returns all rows from the orders table, and the matching rows from the customers table.
•	If there’s a customer for each order (which there is in this data), it works just like an INNER JOIN.
•	If there were any orders with no matching customer (e.g., bad customer_id), the Customer column would be NULL for that row.



--- 

### FULL OUTER JOIN

- Returns all rows from both tables.
- Fills in NULL when there is no match on one side.

```sql
SELECT c.name AS Customer, 
       o.product AS Product
FROM customers c 
FULL OUTER JOIN orders o ON c.id = o.customer_id;
```

✅ Returns all records from both tables.

| Customer | Product             |
|----------|---------------------|
| Alice    | Wireless Mouse      |
| Bob      | Bluetooth Headphones|
| Carol    | Laptop Stand        |
| Alice    | Notebook            |
| David    | USB-C Hub           |
| Eve      | NULL                |
| NULL     | Gaming Chair        |


•	All matching rows from both customers and orders (like an INNER JOIN),
•	Plus unmatched rows from both sides:
  •	Eve (customer) has no order → Product = NULL
  •	The order Gaming Chair has customer_id = 999 (no matching customer) → Customer = NULL


---

### CROSS JOIN

- Returns the Cartesian product of both tables.
- Every row from table A is paired with every row from table B.
- Rarely used without a WHERE filter.

```sql
SELECT c.name AS Customer, 
       o.product AS Product
FROM customers c 
CROSS JOIN orders o;
```

✅ Returns every combination of rows between both tables (Cartesian product).

| Customer | Product             |
|----------|---------------------|
| Alice    | Wireless Mouse      |
| Alice    | Bluetooth Headphones|
| Alice    | Laptop Stand        |
| Alice    | Notebook            |
| Alice    | USB-C Hub           |
| Alice    | Gaming Chair        |
| Bob      | Wireless Mouse      |
| Bob      | Bluetooth Headphones|
| Bob      | Laptop Stand        |
| Bob      | Notebook            |
| Bob      | USB-C Hub           |
| Bob      | Gaming Chair        |
| Carol    | Wireless Mouse      |
| Carol    | Bluetooth Headphones|
| Carol    | Laptop Stand        |
| ...      | ...                 |

•	A CROSS JOIN returns the Cartesian product of both tables.
•	That means it combines every row from customers with every row from orders, regardless of any relationship.

---

### SELF JOIN

A table joined to itself, useful for hierarchies.

```sql
SELECT e1.name AS Employee, e2.name AS Manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.id;
```

Example:

+----+--------+------------+
| id | name   | manager_id |
+----+--------+------------+
|  1 | Alice  | NULL       |
|  2 | Bob    | 1          |
|  3 | Carol  | 1          |
|  4 | David  | 2          |
|  5 | Eve    | 2          |
|  6 | Frank  | 3          |
+----+--------+------------+

Result:

+----------+---------+
| Employee | Manager |
+----------+---------+
| Alice    | NULL    |
| Bob      | Alice   |
| Carol    | Alice   |
| David    | Bob     |
| Eve      | Bob     |
| Frank    | Carol   |
+----------+---------+
---

### USING Clause (Alternative to ON)

Used when joining on a column with the **same name and compatible type** in both tables. 
It simplifies syntax, but only works when this condition is met.

For our example, both tables `customers` and `orders` should have the column `customer_id` 


```sql
SELECT c.name, o.product
FROM customers c
JOIN orders o USING (customer_id);
```

This is equivalent to:

```sql
SELECT c.name, o.product
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;
```

---

### NATURAL JOIN (⚠️ Use with caution)

- Automatically joins tables using all columns with matching names. 
- ⚠️ Can be **unpredictable**, especially when table structures change or contain unexpected overlapping column names.

Example:

employees

| id | name    | department_id |
|----|---------|----------------|
| 1  | Alice   | 101            |
| 2  | Bob     | 102            |
| 3  | Charlie | 101            |

departments

| department_id | department_name |
|---------------|-----------------|
| 101           | Sales           |
| 102           | Engineering     |
| 103           | HR              |

```sql
SELECT * 
FROM employees
NATURAL JOIN departments;
```

Result:

| id | name    | department_id | department_name  |
|----|---------|----------------|-----------------|
| 1  | Alice   | 101            | Sales           |
| 2  | Bob     | 102            | Engineering     |
| 3  | Charlie | 101            | Sales           |

💡 Notes

* INNER JOIN is safest when you're sure both sides will match.
* Use LEFT JOIN when you want everything from the left (e.g., all customers).
* FULL OUTER JOIN is useful for data reconciliation.
* CROSS JOIN is rare; use with care — it multiplies row counts.
* Always use proper JOIN conditions to avoid accidental Cartesian joins.

---

### ANTI JOIN

An ANTI JOIN is a concept (not a SQL keyword) used to find rows in one table that do not have matching rows in another table.

* Left Anti Join: `LEFT JOIN ... WHERE right IS NULL`
* Right Anti Join: `RIGHT JOIN ... WHERE left IS NULL`
* Both Sides Missing: `FULL OUTER JOIN ... WHERE left.key IS NULL OR right.key IS NULL`


```sql
SELECT c.name AS Customer, 
       o.product AS Product
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.product IS NULL;
```

✅ Returns customers **with no orders**.

| Customer | Product |
|----------|---------|
| Eve      | NULL    |


✅ Returns order with matching customers.

```sql
SELECT c.name AS Customer, 
       o.product AS Product
FROM customers c
RIGHT JOIN orders o ON c.id = o.customer_id
WHERE c.name IS NOT NULL;
```

It doesn't include...
1. Order with `customer_id 999` because there is no customer with that customer id.
2. `Eve`, because she has no orders.


---

### ✅ SEMI JOIN (Exists-style Filter)

- Returns rows from the left table **where at least one match exists** in the right table.
- Common in subqueries using `EXISTS`.

```sql
SELECT Customers.Name
FROM Customers
WHERE EXISTS (
  SELECT 1
  FROM Orders
  WHERE Orders.CustomerID = Customers.CustomerID
);
```

✅ Returns customers **who placed at least one order**.

---

## 🧬 Table Relationships in SQL

### 🔑 One-to-Many (Most common)

One record in table A relates to many in table B.

```sql
Customers (ID) ➝ Orders (CustomerID)
```
---

### 🔗 Many-to-Many

Requires a junction table (bridge table).

```sql
Students
Courses
StudentCourses (StudentID, CourseID)
```

---

### 📄 One-to-One

One record in A relates to one in B (rare).

```sql
Users (ID) ➝ UserProfiles (UserID)
```

💡 Notes
- Always index join keys for performance (FOREIGN KEY, PRIMARY KEY).
- Be cautious with OUTER JOINs and NULL-handling in filters.
- Use aliases to improve readability when joining many tables.