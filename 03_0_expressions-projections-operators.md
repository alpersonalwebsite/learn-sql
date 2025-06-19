# Common SQL Expressions and projections

## SQL Expressions, Operators and Projection Elements

These are used primarily in the `SELECT` clause to transform, calculate, or rename data.

---

### Arithmetic Expressions

Used to perform math operations between numeric columns or values.

- `price * quantity`  
- `salary + bonus`  
- `score / attempts`  

---

### String Expressions

Used to manipulate or combine text.

- `FirstName + ' ' + LastName AS FullName`  
- `CONCAT(city, ', ', state) AS Location`  
- `SUBSTRING(name, 1, 3)`  

---

### Date & Time Expressions

Used to extract or manipulate date/time values.

- `YEAR(BirthDate) AS BirthYear`  
- `DATEDIFF(DAY, CreatedAt, GETDATE()) AS DaysSinceCreation`  
- `GETDATE()`  
- `DATEADD(DAY, 7, OrderDate) AS DeliveryEstimate`  

---

### Conditional Expressions

Return different values based on conditions.

- `CASE WHEN age >= 18 THEN 'Adult' ELSE 'Minor' END AS AgeGroup`  
- `IIF(IsActive = 1, 'Yes', 'No') AS ActiveStatus` (SQL Server)

---

### Aliases (Renaming Output)

Used to give a readable or meaningful name to an expression or column.

- `salary + bonus AS TotalCompensation`  
- `COUNT(*) AS TotalUsers`  

---

### Derived Columns

Expressions used in the `SELECT` clause that **don’t exist in the base table** but are **calculated on the fly**.

Examples:
- `price * quantity AS TotalPrice`  
- `CONCAT(FirstName, ' ', LastName) AS FullName`  
- `YEAR(GETDATE()) - YEAR(BirthDate) AS Age`  

---

### Aggregate Functions (often used with GROUP BY)

Operate on a set of rows and return a single value.

- `COUNT(*)`  
- `SUM(sales)`  
- `AVG(score)`  
- `MAX(price)`  
- `MIN(birthdate)`

---

### Scalar Functions (Apply to a single value)

- `ABS(-5)`  
- `ROUND(price, 2)`  
- `LEN(name)`  
- `ISNULL(comment, 'N/A')`
- `UPPER(name)`
- `LOWER(name)`
- `GETDATE()`
- `COALESCE(column1, column2)`

---

### Type Conversion Expressions

Used to convert data from one type to another.

- CAST(salary AS VARCHAR(10))
- CONVERT(DATE, birthdate)

---

## SQL Operators

### ➕ Arithmetic Operators

Used in numeric expressions.

| Operator | Description        | Example              |
|----------|--------------------|----------------------|
| `+`      | Addition            | `salary + bonus`     |
| `-`      | Subtraction         | `price - discount`   |
| `*`      | Multiplication      | `price * quantity`   |
| `/`      | Division            | `total / count`      |
| `%`      | Modulo (remainder)  | `score % 5`          |

---

### Comparison Operators

Used to compare values.

| Operator | Description             | Example               |
|----------|-------------------------|-----------------------|
| `=`      | Equal to                | `age = 30`            |
| `!=` or `<>` | Not equal to         | `status != 'Closed'`  |
| `<`      | Less than               | `price < 100`         |
| `>`      | Greater than            | `score > 80`          |
| `<=`     | Less than or equal to   | `age <= 18`           |
| `>=`     | Greater than or equal to| `salary >= 50000`     |

---

### Logical Operators

Used to combine multiple conditions.

| Operator | Description | Example                      |
|----------|-------------|------------------------------|
| `AND`    | Both must be true | `age > 18 AND active = 1` |
| `OR`     | Either can be true | `city = 'SF' OR city = 'LA'` |
| `NOT`    | Negates a condition | `NOT deleted`           |

---

### Set Operators

Often used in `WHERE` or subqueries.

| Operator     | Description             | Example                        |
|--------------|-------------------------|--------------------------------|
| `IN`         | Matches any in a list   | `state IN ('CA', 'NY')`        |
| `NOT IN`     | Not in a list           | `role NOT IN ('Guest', 'Temp')`|
| `EXISTS`     | True if subquery returns rows | `EXISTS (SELECT 1 FROM ...)` |
| `NOT EXISTS` | True if subquery returns no rows | `NOT EXISTS (...)`       |

---

### Pattern Matching Operators

Use with strings.

| Operator     | Description                        | Example                      |
|--------------|------------------------------------|------------------------------|
| `LIKE`       | Pattern match                      | `name LIKE 'A%'`            |
| `NOT LIKE`   | Does not match pattern             | `email NOT LIKE '%.org'`    |
| `_`          | Single character wildcard in LIKE  | `code LIKE 'A_1'`           |
| `%`          | Multi-character wildcard in LIKE   | `title LIKE '%manager%'`    |

---

### Null Comparison

| Operator        | Description                   | Example                |
|------------------|-------------------------------|------------------------|
| `IS NULL`        | Value is null                 | `end_date IS NULL`     |
| `IS NOT NULL`    | Value is not null             | `phone IS NOT NULL`    |

---

### Bitwise Operators (SQL Server, PostgreSQL, etc.)

| Operator | Description         | Example         |
|----------|---------------------|-----------------|
| `&`      | Bitwise AND         | `flags & 1`     |
| `|`      | Bitwise OR          | `flags | 2`     |
| `^`      | Bitwise XOR         | `flags ^ 3`     |
| `~`      | Bitwise NOT         | `~flags`        |