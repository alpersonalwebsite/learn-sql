# SQL Joins & Table Relationships

Joins are used to **combine rows from two or more tables** based on related columns, typically via **foreign key relationships**.

---

## Joins

Most joins rely on **relational integrity**, where a **foreign key** in one table points to a **primary key** in another.

```sql
SELECT ...
FROM Orders
JOIN Customers ON Orders.CustomerID = Customers.ID
```

---

## 🧱 Common SQL Join Types

Example tables

🧾 Customers

| CustomerID | Name     |
|------------|----------|
| 1          | Alice    |
| 2          | Bob      |
| 3          | Charlie  |


📦 Orders

| OrderID | CustomerID | Product     |
|---------|------------|-------------|
| 101     | 1          | Coffee      |
| 102     | 2          | Tea         |
| 103     | NULL       | Sandwich    |


### 🔄 INNER JOIN

- Returns rows where matching values exist in both tables.
- Most common join type.

```sql
SELECT Customers.Name, Orders.Product
FROM Customers
INNER JOIN Orders ON Customers.CustomerID = Orders.CustomerID;
```

✅ Returns only matching rows from both tables.

| Name  | Product |
| ----- | ------- |
| Alice | Coffee  |
| Bob   | Tea     |


---

### 🧩 LEFT JOIN (LEFT OUTER JOIN)

- Returns all rows from the left table, and matching rows from the right.
- If no match, right-side columns are NULL.

```sql
SELECT Customers.Name, Orders.Product
FROM Customers
LEFT JOIN Orders ON Customers.CustomerID = Orders.CustomerID;
```

✅ Returns all customers, with orders if they exist.

| Name    | Product |
| ------- | ------- |
| Alice   | Coffee  |
| Bob     | Tea     |
| Charlie | NULL    |

---

### 🧩 RIGHT JOIN (RIGHT OUTER JOIN)

- Returns all rows from the right table, and matching rows from the left.
- Less commonly used than LEFT JOIN.

```sql
SELECT Customers.Name, Orders.Product
FROM Customers
RIGHT JOIN Orders ON Customers.CustomerID = Orders.CustomerID;
```

✅ Returns all orders, including ones with no matching customer.

| Name  | Product  |
| ----- | -------- |
| Alice | Coffee   |
| Bob   | Tea      |
| NULL  | Sandwich |

--- 

### 🧲 FULL OUTER JOIN

- Returns all rows from both tables.
- Fills in NULL when there is no match on one side.

```sql
SELECT Customers.Name, Orders.Product
FROM Customers
FULL OUTER JOIN Orders ON Customers.CustomerID = Orders.CustomerID;
```

✅ Returns all records from both tables.

| Name    | Product  |
| ------- | -------- |
| Alice   | Coffee   |
| Bob     | Tea      |
| Charlie | NULL     |
| NULL    | Sandwich |


---

### 🧮 CROSS JOIN

- Returns the Cartesian product of both tables.
- Every row from table A is paired with every row from table B.
- Rarely used without a WHERE filter.

```sql
SELECT Customers.Name, Orders.Product
FROM Customers
CROSS JOIN Orders;
```

✅ Returns every combination of rows between both tables (Cartesian product).

| Name    | Product  |
| ------- | -------- |
| Alice   | Coffee   |
| Alice   | Tea      |
| Alice   | Sandwich |
| Bob     | Coffee   |
| Bob     | Tea      |
| Bob     | Sandwich |
| Charlie | Coffee   |
| Charlie | Tea      |
| Charlie | Sandwich |

---

### 🔍 SELF JOIN

A table joined to itself, useful for hierarchies.

```sql
SELECT e1.Name AS Employee, e2.Name AS Manager
FROM Employees e1
LEFT JOIN Employees e2 ON e1.ManagerID = e2.ID;
```

Example:

| EmployeeID | Name    | ManagerID |
| ---------- | ------- | --------- |
| 1          | Alice   | NULL      |
| 2          | Bob     | 1         |
| 3          | Charlie | 1         |

```sql
SELECT e1.Name AS Employee, e2.Name AS Manager
FROM Employees e1
LEFT JOIN Employees e2 ON e1.ManagerID = e2.EmployeeID;

```

Result:

| Employee | Manager |
| -------- | ------- |
| Alice    | NULL    |
| Bob      | Alice   |
| Charlie  | Alice   |

---

### 🛠 USING Clause (Alternative to ON)

Used when joining on a column with the same name in both tables.

```sql
SELECT *
FROM Orders
JOIN Customers USING (CustomerID);
```

---

### 🛠 NATURAL JOIN (⚠️ Use with caution)

- Automatically joins tables based on columns with the same name.
- Can be unpredictable and should be avoided in complex schemas.

```sql
SELECT *
FROM Orders
NATURAL JOIN Customers;
```

💡 Notes

* INNER JOIN is safest when you're sure both sides will match.
* Use LEFT JOIN when you want everything from the left (e.g., all customers).
* FULL OUTER JOIN is useful for data reconciliation.
* CROSS JOIN is rare; use with care — it multiplies row counts.
* Always use proper JOIN conditions to avoid accidental Cartesian joins.

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