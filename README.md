# csvjoin

> SQL-style join of two CSV files on a shared key column, without a database.

## Why

Two CSV exports, one shared ID, and no appetite for spinning up SQLite.
`csvjoin` does the join in one stdlib-only file.
