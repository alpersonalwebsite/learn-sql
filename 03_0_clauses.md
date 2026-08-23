# Most Common SQL Clauses

Every example below refers to this table, so the queries in this file can be run rather than only
read. `scripts/check_sql.py` loads it and executes them.

users

| id | name  | age | city   |
|----|-------|-----|--------|
| 1  | Alice | 34  | Lisbon |
| 2  | Bob   | 17  | Porto  |
| 3  | Carol | 28  | Lisbon |
| 4  | David | 15  | Faro   |

## 🔍 Clauses Used in SELECT Statements

- `FROM` – Specifies the table(s) to retrieve data from  
  Example: `SELECT * FROM users;`

- `WHERE` – Filters rows based on conditions  
  Example: `SELECT * FROM users WHERE age > 30;`

- `GROUP BY` – Groups rows that have the same values in specified columns  
  Example: `SELECT department, COUNT(*) FROM employees GROUP BY department;`

- `HAVING` – Filters grouped records (used with `GROUP BY`)  
  Example: `SELECT department, COUNT(*) FROM employees GROUP BY department HAVING COUNT(*) > 5;`

- `ORDER BY` – Sorts the result set  
  Example: `SELECT name FROM users ORDER BY name ASC;`
  or: `SELECT  account_id, total_amt_usd FROM orders ORDER By total_amt_usd DESC, account_id`

- `LIMIT` – Limits the number of rows returned (MySQL, PostgreSQL)  
  Example: `SELECT * FROM users LIMIT 10;`

- `OFFSET` – Skips a number of rows (used with `LIMIT`)  
  Example: `SELECT * FROM users LIMIT 10 OFFSET 20;`

- `DISTINCT` – Removes duplicate values  
  Example: `SELECT DISTINCT country FROM users;`

---

## 🔗 Clauses for Joining Tables

- `JOIN` – Combines rows from two or more tables  
  Types: `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL JOIN`  
  Example: `SELECT * FROM users INNER JOIN orders ON users.id = orders.user_id;`

- `ON` – Specifies the condition for a `JOIN`  
  Example: `...JOIN orders ON users.id = orders.user_id;`

- `USING` – Shorthand for joining on a column with the same name in both tables  
  Example: `...JOIN orders USING (user_id);`

---

## 📄 Clauses for Subqueries and Set Operations

- `IN` – Checks if a value exists in a list or subquery  
  Example: `SELECT * FROM users WHERE id IN (1, 2, 3);`

- `EXISTS` – Tests for the existence of rows in a subquery  
  Example: `SELECT * FROM users WHERE EXISTS (SELECT 1 FROM orders WHERE users.id = orders.user_id);`

- `UNION` / `UNION ALL` – Combines result sets from multiple `SELECT` statements  
  Example: `SELECT name FROM table1 UNION SELECT name FROM table2;`

---

## 🧠 Other Common Clauses

- `AS` – Assigns an alias to a column or table  
  Example: `SELECT name AS full_name FROM users;`

- `CASE` – Conditional logic in queries (like IF/ELSE)  
  Example:
  ```sql
  SELECT name,
         CASE WHEN age >= 18 THEN 'Adult' ELSE 'Minor' END AS status
  FROM users;
  ```

  | name  | status |
  |-------|--------|
  | Alice | Adult  |
  | Bob   | Minor  |
  | Carol | Adult  |
  | David | Minor  |

- `BETWEEN` – Checks if a value is within a range
  Example: `SELECT * FROM users WHERE age BETWEEN 18 AND 30;`

- `LIKE` – Pattern matching (e.g., with % and _)
  Example: `SELECT * FROM users WHERE name LIKE 'A%';`
