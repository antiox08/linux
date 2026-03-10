def create_customer(connection, customer_data: dict) -> int:

    sql = """
    INSERT INTO oc_customer 
    (firstname, lastname, email, telephone)
    VALUES (%s, %s, %s, %s)
    """

    with connection.cursor() as cursor:
        cursor.execute(
            sql,
            (
                customer_data["firstname"],
                customer_data["lastname"],
                customer_data["email"],
                customer_data["telephone"],
            ),
        )

        connection.commit()
        return cursor.lastrowid


def get_customer_by_id(connection, customer_id: int):

    sql = "SELECT * FROM oc_customer WHERE customer_id=%s"

    with connection.cursor() as cursor:
        cursor.execute(sql, (customer_id,))
        return cursor.fetchone()


def update_customer(connection, customer_id: int, data: dict):

    sql = """
    UPDATE oc_customer
    SET firstname=%s,
        lastname=%s,
        email=%s,
        telephone=%s
    WHERE customer_id=%s
    """

    with connection.cursor() as cursor:
        cursor.execute(
            sql,
            (
                data["firstname"],
                data["lastname"],
                data["email"],
                data["telephone"],
                customer_id,
            ),
        )

        connection.commit()
        return cursor.rowcount


def delete_customer(connection, customer_id: int):

    sql = "DELETE FROM oc_customer WHERE customer_id=%s"

    with connection.cursor() as cursor:
        cursor.execute(sql, (customer_id,))
        connection.commit()

        return cursor.rowcount