# SQL Statements

## 🗄️ Data Query Language (DQL)
Used to query data from tables.

- `SELECT` – Retrieve data from one or more tables  
  Example: `SELECT * FROM users;`

---

## ✏️ Data Manipulation Language (DML)
Used to insert, update, or delete data.

- `INSERT` – Add new rows  
  Example: `INSERT INTO users (name) VALUES ('Ana');`

- `UPDATE` – Modify existing rows  
  Example: `UPDATE users SET name = 'Eva' WHERE id = 1;`

- `DELETE` – Remove rows  
  Example: `DELETE FROM users WHERE id = 1;`

---

## 🧱 Data Definition Language (DDL)
Used to define and modify table and database structures.

- `CREATE` – Create new tables, databases, indexes, etc.  
  Example: `CREATE TABLE users (id INT, name TEXT);`

- `ALTER` – Change the structure of a table  
  Example: `ALTER TABLE users ADD email TEXT;`

- `DROP` – Delete a table or database  
  Example: `DROP TABLE users;`

- `TRUNCATE` – Delete all rows in a table (faster, no rollback)  
  Example: `TRUNCATE TABLE users;`

---

## 🔐 Data Control Language (DCL)
Used to control access to data.

- `GRANT` – Give permissions to users or roles  
  Example: `GRANT SELECT ON users TO analyst;`

- `REVOKE` – Remove previously granted permissions  
  Example: `REVOKE SELECT ON users FROM analyst;`

---

## 🔁 Transaction Control Language (TCL)
Used to manage transactions in SQL.

- `BEGIN` or `START TRANSACTION` – Start a transaction  
  Example: `BEGIN;`

- `COMMIT` – Save all changes made during the transaction  
  Example: `COMMIT;`

- `ROLLBACK` – Undo changes made since the last BEGIN  
  Example: `ROLLBACK;`

- `SAVEPOINT` – Set a point within a transaction to roll back to  
  Example: `SAVEPOINT before_update;`
