# URL to SQL Parser
We are working on REST API to enable generalized SQL access to various datasets.  One of the goals is to support URL parameters that enable us to select a subset of table rows and columns, and to sort and paginate the result set.

This project contains a sample Python code module, and a Jupyter notebook that demonstrates its functionality.  


## References

A good example of REST API query parameters can be found on US Treasury's FiscalData web site.  It specifies a basic means of selecting and filtering a subset of columns and rows from available datasets.
https://fiscaldata.treasury.gov/api-documentation/#parameters

**Psycopg 3** is a PostgreSQL (and Redshift) database JDBC adapter for the Python programming language.  PostgreSQL features a module that contains objects and functions useful to generate SQL dynamically, in a convenient and safe way.
https://www.psycopg.org/psycopg3/docs/api/sql.html

SQL Injection vulnerabilities are a concern whenever executing programmatically composed SQL.   The following link describes a simple approach that uses regular expressions (RegEx) to scan SQL for potential issues based upon a configurable list of patterns.
https://github.com/pixie-io/pixie/issues/357
