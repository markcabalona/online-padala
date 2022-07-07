from sqlite3 import Connection


def validate_outlet(db: Connection, outlet_number: str):
    return db.execute(
        f"SELECT * FROM outlets WHERE outlet_number = '{outlet_number}'"
    ).fetchone()

    
