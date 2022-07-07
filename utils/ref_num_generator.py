from sqlite3 import Connection
import string
import random


def ref_num_generator(db: Connection):
    while True:
        ref_num = "".join(random.choice(string.ascii_letters) for _ in range(6))
        # check for duplicate
        if (
            db.execute(
                f"SELECT * FROM transactions WHERE ref_num = '{ref_num}'"
            ).fetchone()
            is None
        ):
            return ref_num


def outlet_number_generator(db: Connection):
    numerics = "0123456789"
    while True:
        outlet_number = (
            "".join(random.choice(numerics) for _ in range(3))
            + "-"
            + "".join(random.choice(numerics) for _ in range(3))
            + "-"
            + "".join(random.choice(numerics) for _ in range(4))
        )
        print(outlet_number)
        # check for duplicate
        if (
            db.execute(
                f"SELECT * FROM outlets WHERE outlet_number = '{outlet_number}'"
            ).fetchone()
            is None
        ):
            return outlet_number
