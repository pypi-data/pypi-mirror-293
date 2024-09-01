import psycopg2
import os


def close_conn(conn, cur) -> None:
    """
    Close the connection to the database.
    """
    cur.close()
    conn.close()


def get_conn():
    """
    Get a connection to the database.
    """
    db_host = os.environ.get("POSTGRES_HOST")
    db_password = os.environ.get("POSTGRES_PASSWORD")
    db_username = os.environ.get("POSTGRES_USER")
    return psycopg2.connect(
        database=os.environ.get("POSTGRES_DATABASE"),
        host=db_host,
        user=db_username,
        password=db_password,
        port=int(os.environ.get("POSTGRES_PORT")),
    )


def run_static_dml(conn, query: str) -> None:
    """
    Run a static DML statement without getting the results.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

    cur.close()
    conn.close()


def run_parameterized_item_dml(
    statement: str, params: tuple, with_results: bool = False
) -> list | None:
    """
    Run a parametrized DML SQL query.
    You can choose to return the results of the query.
    """
    results = None
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(statement, params)
    if with_results:
        results = cur.fetchall()
    conn.commit()

    close_conn(conn, cur)
    return results


def run_parameterized_dql(query: str, params: tuple) -> list:
    """
    Run a parameterized DQL statement and get the results.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    results = cur.fetchall()

    cur.close()
    conn.close()

    return results


def run_static_dql(query: str) -> list:
    """
    Run a static DQL statement and get the results.
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(query)
    result = cur.fetchall()

    close_conn(conn, cur)

    return result
