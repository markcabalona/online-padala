from datetime import datetime
from http import HTTPStatus
from fastapi import HTTPException
from sqlite3 import Connection
from models.customer import Customer
from models.outlets import CreateOutlet, Outlet
from models.transaction import CreateTransaction, Transaction
from utils.ref_num_generator import outlet_number_generator, ref_num_generator
from utils.validate_outlet import validate_outlet


def fetch_outlets(db: Connection):
    try:
        result = db.execute(f"SELECT * FROM outlets").fetchall()

        res = [
            Outlet(outlet_num=entry[0], address=entry[1], service_fee=entry[2])
            for entry in result
        ]

        return res
    except Exception as e:

        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Server Error"
        )


def fetch_outlet(db: Connection, id: str):
    try:
        res = db.execute(
            f"""
            SELECT outlet_number,
                address,
                service_fee
            FROM outlets
            WHERE outlet_number = '{id}'
        """
        ).fetchone()

        if not res:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f"Outlet {id} not found."
            )

        return Outlet(
            outlet_num=res[0],
            address=res[1],
            service_fee=res[2],
        )
    except HTTPException as httpexception:
        raise httpexception
    except Exception as e:
        HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Error occured while fetching outlet {id}",
        )


def create_outlet(db: Connection, outlet=CreateOutlet):
    try:
        outlet_number = outlet_number_generator(db=db)

        db.execute(
            f"""
            INSERT INTO outlets(outlet_number,address,service_fee)
            VALUES('{outlet_number}','{outlet.address}',{outlet.service_fee});
        """
        )
        print("inserted")
        res = db.execute(
            f"""
            SELECT * FROM outlets
            WHERE outlet_number = '{outlet_number}'
        """
        ).fetchone()
        db.commit()
        return Outlet(
            outlet_num=res[0],
            address=res[1],
            service_fee=res[2],
        )

    except Exception as e:
        print(e)


def create_transaction(db: Connection, transaction: CreateTransaction):
    try:
        # check for outlet validity
        if (
            not validate_outlet(db=db, outlet_number=transaction.outlet_number)
            or transaction.outlet_number == ""
        ):
            raise HTTPException(
                status_code=HTTPStatus.NOT_ACCEPTABLE, detail="Invalid outlet number"
            )

        elif transaction.sender.full_name == "" or transaction.receiver.full_name == "":
            raise HTTPException(
                status_code=HTTPStatus.NOT_ACCEPTABLE,
                detail="Sender or receiver name cannot be empty",
            )
        elif transaction.amount < 500:
            raise HTTPException(
                status_code=HTTPStatus.NOT_ACCEPTABLE,
                detail="Amount must be at least 500",
            )

        sender_id = db.execute(
            f"""
        INSERT INTO customers(full_name,mobile_number)
        VALUES ('{transaction.sender.full_name}','{transaction.sender.mobile_number}');
        """
        ).lastrowid
        receiver_id = db.execute(
            f"""
        INSERT INTO customers(full_name,mobile_number)
        VALUES ('{transaction.receiver.full_name}','{transaction.receiver.mobile_number}');
        """
        ).lastrowid
        ref_num = ref_num_generator(db=db)

        transaction_id = db.execute(
            f"""
        INSERT INTO transactions(ref_num,sender_id,receiver_id,outlet_number,amount,date_created,is_done)
        VALUES('{ref_num}',{sender_id},{receiver_id},'{transaction.outlet_number}',{transaction.amount},'{transaction.date_created.isoformat()}',{False});
        """
        ).lastrowid

        db.commit()

        return Transaction(
            id=transaction_id,
            reference_number=ref_num,
            sender=fetch_customer(db=db, id=sender_id),
            receiver=fetch_customer(db=db, id=receiver_id),
            outlet=fetch_outlet(db=db, id=transaction.outlet_number),
            amount=transaction.amount,
            is_done=False,
            date_created=transaction.date_created,
        )

    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Transaction not completed",
        )


def fetch_transactions(db: Connection):
    try:
        res = db.execute(
            """
        SELECT id,
            ref_num,
            sender_id,
            receiver_id,
            outlet_number,
            amount,
            date_created,
            is_done
        FROM transactions
        """
        ).fetchall()

        transactions = []
        for entity in res:

            transactions.append(
                Transaction(
                    id=entity[0],
                    reference_number=entity[1],
                    sender=fetch_customer(db=db, id=entity[2]),
                    receiver=fetch_customer(db=db, id=entity[3]),
                    outlet=fetch_outlet(db=db, id=entity[4]),
                    amount=entity[5],
                    date_created=entity[6],
                    is_done=bool(entity[7]),
                )
            )
        return transactions
    except HTTPException as httpexception:
        print(httpexception)
        raise httpexception
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Fetch transaction failed",
        )


def fetch_single_transaction(db: Connection, ref_num: str):
    try:
        res = db.execute(
            f"""
        SELECT id,
            ref_num,
            sender_id,
            receiver_id,
            outlet_number,
            amount,
            date_created,
            is_done
        FROM transactions
        WHERE ref_num ='{ref_num}'
        """
        ).fetchone()

        if not res:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Transaction with reference number: {ref_num} does not exists.",
            )

        return Transaction(
            id=res[0],
            reference_number=res[1],
            sender=fetch_customer(db=db, id=res[2]),
            receiver=fetch_customer(db=db, id=res[3]),
            outlet=fetch_outlet(db=db, id=res[4]),
            amount=res[5],
            date_created=res[6],
            is_done=bool(res[7]),
        )

    except HTTPException as httpexception:
        print(httpexception)
        raise httpexception
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Fetch transaction failed",
        )


def update_transaction(db: Connection, id: int, updated_transaction: CreateTransaction):
    try:
        trans = db.execute(
            f"""
        SELECT * FROM transactions
        WHERE id = {id}
        """
        ).fetchone()
        if not trans:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Transaction {id} does not exists",
            )
        (sender_id, receiver_id) = db.execute(
            f"""
        SELECT sender_id, receiver_id
        FROM transactions
        WHERE id = {id}
        """
        ).fetchone()

        if updated_transaction.sender.full_name != "":
            db.execute(
                f"""
                UPDATE customers
                SET full_name = '{updated_transaction.sender.full_name}'
                WHERE id = {sender_id}
                """
            )
        if updated_transaction.sender.mobile_number != "":
            db.execute(
                f"""
                UPDATE customers
                SET mobile_number = '{updated_transaction.sender.mobile_number}'
                WHERE id = {sender_id}
                """
            )

        if updated_transaction.receiver.full_name != "":
            db.execute(
                f"""
                UPDATE customers
                SET full_name = '{updated_transaction.receiver.full_name}'
                WHERE id = {receiver_id}
            """
            )

        if updated_transaction.receiver.mobile_number != "":
            db.execute(
                f"""
                UPDATE customers
                SET mobile_number = '{updated_transaction.receiver.mobile_number}'
                WHERE id = {receiver_id}
                """
            )

        if updated_transaction.outlet_number != "":

            if not validate_outlet(
                db=db, outlet_number=updated_transaction.outlet_number
            ):
                raise HTTPException(
                    status_code=HTTPStatus.NOT_ACCEPTABLE,
                    detail="Invalid outlet number",
                )
            db.execute(
                f"""
             UPDATE transactions
             SET outlet_number = '{updated_transaction.outlet_number}'
             WHERE id = {id}
             """
            )

        if updated_transaction.amount > 0:
            if updated_transaction.amount < 500:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_ACCEPTABLE,
                    detail="Amount must be atleast 500",
                )

            db.execute(
                f"""
             UPDATE transactions
             SET amount = {updated_transaction.amount}
             WHERE id = {id}
             """
            )

        res = db.execute(
            f"""
        SELECT id,
            ref_num,
            sender_id,
            receiver_id,
            outlet_number,
            amount,
            date_created,
            is_done
        FROM transactions
        WHERE id = {id}
        """
        ).fetchone()

        db.commit()
        return Transaction(
            id=res[0],
            reference_number=res[1],
            sender=fetch_customer(db=db, id=res[2]),
            receiver=fetch_customer(db=db, id=res[3]),
            outlet=fetch_outlet(db=db, id=res[4]),
            amount=res[5],
            date_created=res[6],
            is_done=bool(res[7]),
        )
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:

        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Failed to update transaction"
        )


def delete_transaction(db: Connection, transaction_id: int):
    try:
        trans = db.execute(
            f"""
        SELECT * FROM transactions
        WHERE id = {transaction_id}
        """
        ).fetchone()
        if not trans:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Transaction {transaction_id} does not exists",
            )
        db.execute(
            f"""
        DELETE FROM transactions
        WHERE id= {transaction_id}
        """
        )
        db.commit()

        return {"message": "Transaction Deleted"}
    except HTTPException as http_exception:
        raise http_exception
    except:
        raise HTTPException(
            status_code=HTTPStatus.OK, detail="Transaction can not be deleted"
        )


def fetch_customer(db: Connection, id: int):
    try:
        res = db.execute(
            f"""
            SELECT id,
                full_name,
                mobile_number
            FROM customers
            WHERE id = {id}
        """
        ).fetchone()

        if not res:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f"Customer {id} not found."
            )

        return Customer(
            id=res[0],
            full_name=res[1],
            mobile_number=res[2],
        )
    except HTTPException as httpexception:
        raise httpexception
    except Exception as e:
        HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Error occured while fetching customer {id}",
        )
