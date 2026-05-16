import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "budget_tracker",
    "user": "calgoneq",
    "password": ""
}

def init_db() -> None:
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                id      SERIAL PRIMARY KEY,
                sklep   TEXT NOT NULL,
                kwota   FLOAT NOT NULL,
                kategoria TEXT NOT NULL,
                data    TEXT NOT NULL)
            """);

def get_all_transactions(kategoria: str = None) -> list[dict]:
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            keys: tuple = ("id", "sklep", "kwota", "kategoria", "data")
            
            if kategoria is not None:
                cursor.execute("SELECT * FROM transactions WHERE kategoria = %s", (kategoria,))
            else:
                cursor.execute("SELECT * FROM transactions")

            rows = cursor.fetchall()
            list_of_dicts: list[dict] = [dict(zip(keys, row)) for row in rows]

            return list_of_dicts
        
def get_transaction_by_id(transaction_id: int) -> dict | None:
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            keys: tuple = ("id", "sklep", "kwota", "kategoria", "data")
            cursor.execute("SELECT * FROM transactions WHERE id = %s", (transaction_id,))
            row = cursor.fetchone()

            if row is None:
                return None
            response: dict = dict(zip(keys, row))
            
            return response

def add_transaction(transaction: dict) -> dict:
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            keys: tuple = ("id", "sklep", "kwota", "kategoria", "data")
            cursor.execute(
                "INSERT INTO transactions (sklep, kwota, kategoria, data) VALUES (%s, %s, %s, %s) RETURNING id, sklep, kwota, kategoria, data",
                (transaction["sklep"], transaction["kwota"], transaction["kategoria"], transaction["data"])
            )
            row = cursor.fetchone()
            response: dict = dict(zip(keys, row))

            return response

def remove_transaction(transaction_id: int) -> bool:
     with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))
            if cursor.rowcount > 0:
                return True
            else:
                return False