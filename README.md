# Python Database

Connects to SQL Server and prints every row from `student_details`.

## Setup

Install [Microsoft ODBC Driver 18 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server), then:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with the server, database, login, and password. On Windows, if the legacy driver is the one installed, set `DB_DRIVER=SQL Server`.

```bash
python main.py
```

The script uses SQL authentication. If the server cannot be reached, it prints the reason and exits with status 1.

## Environment variables

- `DB_SERVER` — SQL Server host. Defaults to `localhost`.
- `DB_DATABASE` — database name. Defaults to `students`.
- `DB_USER` — SQL login. Required.
- `DB_PASSWORD` — password for that login. Required.
- `DB_DRIVER` — ODBC driver name. Defaults to `ODBC Driver 18 for SQL Server`.
