import os
import re
import sys

import pyodbc
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SERVER = "localhost"
DEFAULT_DATABASE = "students"
DEFAULT_DRIVER = "ODBC Driver 18 for SQL Server"


def get_config():
    return {
        "server": _env("DB_SERVER", DEFAULT_SERVER),
        "database": _env("DB_DATABASE", DEFAULT_DATABASE),
        "user": _env("DB_USER"),
        "password": _env("DB_PASSWORD"),
        "driver": _env("DB_DRIVER", DEFAULT_DRIVER),
    }


def build_connection_string(config):
    parts = [
        f"DRIVER={_brace(config['driver'])};",
        f"SERVER={config['server']};",
        f"DATABASE={_brace(config['database'])};",
        f"UID={_brace(config['user'])};",
        f"PWD={_brace(config['password'])};",
    ]
    # Driver 18 encrypts by default and rejects the instance's self-signed cert.
    if "ODBC Driver" in config["driver"]:
        parts.append("TrustServerCertificate=yes;")
    return "".join(parts)


def main():
    config = get_config()
    missing = [
        name
        for name, value in (
            ("DB_USER", config["user"]),
            ("DB_PASSWORD", config["password"]),
        )
        if not value
    ]
    if missing:
        print(
            "Missing required environment variables: " + ", ".join(missing) + ".",
            file=sys.stderr,
        )
        print("Copy .env.example to .env and set the database login.", file=sys.stderr)
        sys.exit(1)

    try:
        conn = pyodbc.connect(build_connection_string(config), timeout=10)
    except pyodbc.Error as exc:
        _report_connect_error(config, exc)

    try:
        cursor = conn.cursor()
        print(cursor)
        cursor.execute("SELECT * FROM student_details")
        for row in cursor:
            print(row)
    except pyodbc.Error as exc:
        print("Query failed: " + _redact(str(exc)), file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()


def _env(name, default=""):
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    return value


def _brace(value):
    return "{" + value.replace("}", "}}") + "}"


def _redact(text):
    return re.sub(r"PWD=(\{(?:[^{}]|}})*\}|[^;]*)", "PWD=***", text)


def _report_connect_error(config, exc):
    detail = _redact(str(exc))
    if "Data source name not found" in detail or "Can't open lib" in detail:
        print(
            f"ODBC driver '{config['driver']}' is not installed.",
            file=sys.stderr,
        )
        print(
            "Install Microsoft ODBC Driver 18 for SQL Server, "
            "or set DB_DRIVER to an installed driver name.",
            file=sys.stderr,
        )
    else:
        print(
            f"Unable to connect to SQL Server at {config['server']} "
            f"(database '{config['database']}').",
            file=sys.stderr,
        )
        print(
            "Check DB_SERVER, DB_DATABASE, DB_USER, and DB_PASSWORD.",
            file=sys.stderr,
        )
    print("Details: " + detail, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
