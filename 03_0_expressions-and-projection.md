# Common SQL Expressions and projections

## 🧮 SQL Expressions & Projection Elements

These are used primarily in the `SELECT` clause to transform, calculate, or rename data.

---

### 🔢 Arithmetic Expressions

Used to perform math operations between numeric columns or values.

- `price * quantity`  
- `salary + bonus`  
- `score / attempts`  

---

### 🔤 String Expressions

Used to manipulate or combine text.

- `FirstName + ' ' + LastName AS FullName`  
- `CONCAT(city, ', ', state) AS Location`  
- `SUBSTRING(name, 1, 3)`  
- `UPPER(email)`  

---

### 🗓️ Date & Time Expressions

Used to extract or manipulate date/time values.

- `YEAR(BirthDate) AS BirthYear`  
- `DATEDIFF(DAY, CreatedAt, GETDATE()) AS DaysSinceCreation`  
- `GETDATE()`  
- `DATEADD(DAY, 7, OrderDate) AS DeliveryEstimate`  

---

### 🧠 Conditional Expressions

Return different values based on conditions.

- `CASE WHEN age >= 18 THEN 'Adult' ELSE 'Minor' END AS AgeGroup`  
- `IIF(IsActive = 1, 'Yes', 'No') AS ActiveStatus` (SQL Server)

---

### 🔍 Aliases (Renaming Output)

Used to give a readable or meaningful name to an expression or column.

- `salary + bonus AS TotalCompensation`  
- `COUNT(*) AS TotalUsers`  

---

### 🆕 Derived Columns

Expressions used in the `SELECT` clause that **don’t exist in the base table** but are **calculated on the fly**.

Examples:
- `price * quantity AS TotalPrice`  
- `CONCAT(FirstName, ' ', LastName) AS FullName`  
- `YEAR(GETDATE()) - YEAR(BirthDate) AS Age`  

---

### 🧮 Aggregate Functions (often used with GROUP BY)

Operate on a set of rows and return a single value.

- `COUNT(*)`  
- `SUM(sales)`  
- `AVG(score)`  
- `MAX(price)`  
- `MIN(birthdate)`

---

### 📐 Scalar Functions (Apply to a single value)

- `ABS(-5)`  
- `ROUND(price, 2)`  
- `LEN(name)`  
- `ISNULL(comment, 'N/A')`

---

### 🧠 Notes:

- These elements are **not statements or clauses** — they are expressions or parts of expressions.
- Derived columns, aliases, and calculated fields fall into this group.
- They are typically part of the **projection logic** in a `SELECT` query.