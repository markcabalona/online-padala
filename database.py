import sqlite3
from os.path import exists
from typing import List, Optional

from constants import DB_EXTENSION, SMART_PADALA_OUTLETS, SmartPadalaOutlet


class Database:
    def __init__(
        self, db_name: str = "test", file_extension: str = DB_EXTENSION
    ) -> None:
        db_exists = exists(f"{db_name}.{file_extension}")
        self.connection = sqlite3.connect(f"{db_name}.{file_extension}",check_same_thread=False)
        self.__create_tables()
        if not db_exists:
            self.__populate_outlets()

    def __create_tables(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS customers(
                id INTEGER NOT NULL,
                full_name VARCHAR NOT NULL,
                mobile_number VARCHAR(11),

                PRIMARY KEY (id)
            );
        """
        )

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS outlets(
                outlet_number VARCHAR NOT NULL,
                address VARCHAR NOT NULL,
                service_fee NUMERIC,

                PRIMARY KEY (outlet_number)
            );
        """
        )

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER NOT NULL,
                ref_num VARCHAR NOT NULL,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                outlet_number VARCHAR NOT NULL,
                amount NUMERIC NOT NULL,
                date_created VARCHAR,
                is_done BOOL,

                PRIMARY KEY (id),
                FOREIGN KEY(sender_id) REFERENCES customers(id),
                FOREIGN KEY(receiver_id) REFERENCES customers(id),
                FOREIGN KEY(outlet_number) REFERENCES outlets(outlet_number)
            );
        """
        )

    # default outlets
    def __populate_outlets(
        self, outlets: List[SmartPadalaOutlet] = SMART_PADALA_OUTLETS
    ):
        for outlet in outlets:
            self.connection.execute(
                f"""
                    INSERT INTO outlets(outlet_number,address,service_fee)
                    VALUES ("{outlet.outlet_number}","{outlet.address}",{outlet.service_fee});
                """
            )
            self.connection.commit()

    def close(self):
        self.connection.close()


db = Database(db_name='online_padala')