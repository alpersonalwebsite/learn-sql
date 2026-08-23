# Learn SQL

Notes on SQL: what the statements and clauses are, how expressions and operators behave, how
constraints shape a schema, and a long walk through joins with worked examples.

The joins document is the one to read if you only read one. Every join type has the same two sample
tables, the query, and the rows it returns, and those rows are **checked by running the query** rather
than typed from memory. That matters more than it sounds: when this was written the sample data said one
thing and three result tables said another, and nothing could have caught it by reading.

## Checking the SQL

```bash
make check          # both
make check-sql      # run every SQL sample against the sample data and diff the results
make check-links    # every relative link and #anchor resolves
```

`scripts/check_sql.py` parses the sample tables out of the markdown into an in-memory sqlite database,
runs each ```sql block, and compares what comes back against the result table the document claims. It
found, on the version before this:

- two queries that **did not run at all** against the schema defined a few lines above them
  (`USING (customer_id)` on a schema whose key is `id`, and a semi-join written against table and
  column names this repository never defines);
- three result tables and one prose sentence describing a product the sample data had been
  renamed away from;
- a sample table that was never named, so nothing said which table the query above it referred to.

Blocks that cannot be executed say so on their first line, and the categories are kept apart because
they are different claims: `fragment` for a clause or column definition that is valid SQL in context,
`notation` for a block that is not SQL at all, `dialect <name>` for valid SQL that sqlite cannot run,
and `fails <text>` for a query that is *supposed* to fail, where the error must contain that text. That
last one is the useful one: a query demonstrating an error is otherwise indistinguishable from a query
that is simply broken.

sqlite is not every dialect, and these notes cover MySQL, Postgres and SQL Server too, so a green run
means the samples are consistent with each other and with sqlite. It does not mean every sample is
portable.

No dependencies: `sqlite3` ships with Python.

## Contents

- [Databases](./00_0_databases.md)
    - [🔢 Relational Databases (SQL)](./00_0_databases.md#-relational-databases-sql)
    - [📦 NoSQL Databases (Non-Relational)](./00_0_databases.md#-nosql-databases-non-relational)
    - [🌐 Search & Analytics Engines](./00_0_databases.md#-search--analytics-engines)
    - [🧠 Graph Databases](./00_0_databases.md#-graph-databases)
    - [⏱️ Time-Series Databases](./00_0_databases.md#️-time-series-databases)
    - [🧰 Multi-Model Databases](./00_0_databases.md#-multi-model-databases)
- [Entity Relationship Diagrams](./01_0_erd.md)
- [SQL Statements](./02_0_statements.md)
    - [🗄️ Data Query Language (DQL)](./02_0_statements.md#️-data-query-language-dql)
    - [✏️ Data Manipulation Language (DML)](./02_0_statements.md#️-data-manipulation-language-dml)
    - [🧱 Data Definition Language (DDL)](./02_0_statements.md#-data-definition-language-ddl)
    - [🔐 Data Control Language (DCL)](./02_0_statements.md#-data-control-language-dcl)
    - [🔁 Transaction Control Language (TCL)](./02_0_statements.md#-transaction-control-language-tcl)
- [Clauses](./03_0_clauses.md)
    - [🔍 Clauses Used in SELECT Statements](./03_0_clauses.md#-clauses-used-in-select-statements)
    - [🔗 Clauses for Joining Tables](./03_0_clauses.md#-clauses-for-joining-tables)
    - [📄 Clauses for Subqueries and Set Operations](./03_0_clauses.md#-clauses-for-subqueries-and-set-operations)
    - [🧠 Other Common Clauses](./03_0_clauses.md#-other-common-clauses)
- [Expressions, Projections and Operators](./04_0_expressions-projections-operators.md)
    - [SQL Expressions, Operators and Projection Elements](./04_0_expressions-projections-operators.md#sql-expressions-operators-and-projection-elements)
        - [Arithmetic Expressions](./04_0_expressions-projections-operators.md#arithmetic-expressions)
        - [String Expressions](./04_0_expressions-projections-operators.md#string-expressions)
        - [Date & Time Expressions](./04_0_expressions-projections-operators.md#date--time-expressions)
        - [Conditional Expressions](./04_0_expressions-projections-operators.md#conditional-expressions)
        - [Aliases (Renaming Output)](./04_0_expressions-projections-operators.md#aliases-renaming-output)
        - [Derived Columns](./04_0_expressions-projections-operators.md#derived-columns)
        - [Aggregate Functions (often used with GROUP BY)](./04_0_expressions-projections-operators.md#aggregate-functions-often-used-with-group-by)
        - [Scalar Functions (Apply to a single value)](./04_0_expressions-projections-operators.md#scalar-functions-apply-to-a-single-value)
        - [Type Conversion Expressions](./04_0_expressions-projections-operators.md#type-conversion-expressions)
        - [Notes](./04_0_expressions-projections-operators.md#notes)
    - [SQL Operators](./04_0_expressions-projections-operators.md#sql-operators)
        - [➕ Arithmetic Operators](./04_0_expressions-projections-operators.md#-arithmetic-operators)
        - [Comparison Operators](./04_0_expressions-projections-operators.md#comparison-operators)
        - [Logical Operators](./04_0_expressions-projections-operators.md#logical-operators)
        - [Set Operators](./04_0_expressions-projections-operators.md#set-operators)
        - [Pattern Matching Operators](./04_0_expressions-projections-operators.md#pattern-matching-operators)
        - [Null Comparison](./04_0_expressions-projections-operators.md#null-comparison)
        - [Bitwise Operators (SQL Server, PostgreSQL, etc.)](./04_0_expressions-projections-operators.md#bitwise-operators-sql-server-postgresql-etc)
- [Constraints and Schema Definitions](./05_0_constraints-and-schema-definitions.md)
    - [🗂️ Table & Column Definitions](./05_0_constraints-and-schema-definitions.md#️-table--column-definitions)
    - [🔐 Primary Key Constraint](./05_0_constraints-and-schema-definitions.md#-primary-key-constraint)
    - [🧷 Foreign Key Constraint](./05_0_constraints-and-schema-definitions.md#-foreign-key-constraint)
    - [🔁 Unique Constraint](./05_0_constraints-and-schema-definitions.md#-unique-constraint)
    - [✅ Check Constraint](./05_0_constraints-and-schema-definitions.md#-check-constraint)
    - [📌 Default Constraint](./05_0_constraints-and-schema-definitions.md#-default-constraint)
    - [🧍 Not Null Constraint](./05_0_constraints-and-schema-definitions.md#-not-null-constraint)
    - [📄 Identity / Auto-increment (SQL Server & MySQL)](./05_0_constraints-and-schema-definitions.md#-identity--auto-increment-sql-server--mysql)
    - [💡 Notes:](./05_0_constraints-and-schema-definitions.md#-notes)
- [Joins and Table Relationships](./06_0_joins-and-relationships.md)
    - [Joins](./06_0_joins-and-relationships.md#joins)
    - [Common SQL Join Types](./06_0_joins-and-relationships.md#common-sql-join-types)
        - [INNER JOIN](./06_0_joins-and-relationships.md#inner-join)
        - [LEFT JOIN (LEFT OUTER JOIN)](./06_0_joins-and-relationships.md#left-join-left-outer-join)
        - [RIGHT JOIN (RIGHT OUTER JOIN)](./06_0_joins-and-relationships.md#right-join-right-outer-join)
        - [FULL OUTER JOIN](./06_0_joins-and-relationships.md#full-outer-join)
        - [CROSS JOIN](./06_0_joins-and-relationships.md#cross-join)
        - [SELF JOIN](./06_0_joins-and-relationships.md#self-join)
        - [USING Clause (Alternative to ON)](./06_0_joins-and-relationships.md#using-clause-alternative-to-on)
        - [NATURAL JOIN (⚠️ Use with caution)](./06_0_joins-and-relationships.md#natural-join-️-use-with-caution)
        - [ANTI JOIN](./06_0_joins-and-relationships.md#anti-join)
        - [✅ SEMI JOIN (Exists-style Filter)](./06_0_joins-and-relationships.md#-semi-join-exists-style-filter)
    - [🧬 Table Relationships in SQL](./06_0_joins-and-relationships.md#-table-relationships-in-sql)
        - [🔑 One-to-Many (Most common)](./06_0_joins-and-relationships.md#-one-to-many-most-common)
        - [🔗 Many-to-Many](./06_0_joins-and-relationships.md#-many-to-many)
        - [📄 One-to-One](./06_0_joins-and-relationships.md#-one-to-one)

## Note on the emoji headings

Several headings begin with an emoji, and a few of those emoji are a symbol followed by U+FE0F
(variation selector-16). GitHub's anchor generator deletes the symbol and **keeps** the selector, so
those anchors start with an invisible character. The index above is generated with the same rule
`scripts/check_links.py` verifies against GitHub's renderer, which is why the links work. Writing them
by hand would not have.
