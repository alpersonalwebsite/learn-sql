# SQL Constraints & Schema Definitions

These are used when creating or altering tables to define the **structure**, **rules**, and **integrity constraints** for your data.

---

## 🗂️ Table & Column Definitions

Used within `CREATE TABLE` or `ALTER TABLE` statements.

```sql
CREATE TABLE Users (
    ID INT,
    Name VARCHAR(100),
    Email VARCHAR(255),
    CreatedAt DATETIME
);
```

---

## 🔐 Primary Key Constraint

- Ensures that a column (or combination) uniquely identifies each row.
- Automatically creates a unique index.

```sql
ID INT PRIMARY KEY

PRIMARY KEY (ID, SiteID)
```

---

## 🧷 Foreign Key Constraint

- Enforces a relationship between two tables.
- Prevents invalid data entry in the child table.

```sql
FOREIGN KEY (UserID) REFERENCES Users(ID)
```

Optional behaviors:

```sql
ON DELETE CASCADE
ON UPDATE SET NULL
```

---

## 🔁 Unique Constraint

Ensures all values in a column or set of columns are distinct.

```sql
Email VARCHAR(255) UNIQUE
```

```sql
UNIQUE (SiteID, Email)
```

---

## ✅ Check Constraint

Restricts the values that can be inserted.

```sql
CHECK (Age >= 18)
```

```sql
CHECK (Status IN ('Active', 'Inactive'))
```

---

## 📌 Default Constraint

Provides a default value when none is supplied.

```sql
CreatedAt DATETIME DEFAULT GETDATE()
```

```sql
IsActive BIT DEFAULT 1
```

---

## 🧍 Not Null Constraint

Ensures that a column cannot have NULL values.

```sql
Name VARCHAR(100) NOT NULL
```

---


## 📄 Identity / Auto-increment (SQL Server & MySQL)

Automatically generates incrementing numbers.

```sql
ID INT IDENTITY(1,1) PRIMARY KEY  -- SQL Server
```

```sql
ID INT AUTO_INCREMENT PRIMARY KEY  -- MySQL
```

---

## 💡 Notes:

* Constraints help enforce data integrity, reduce errors, and document business rules.
* They are defined as part of the schema (i.e., table structure), not during query execution.