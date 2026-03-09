from lib.db import (
    create_customer,
    get_customer_by_id,
    update_customer,
    delete_customer
)


def test_create_customer(connection):

    data = {
        "firstname": "Ivan",
        "lastname": "Ivanov",
        "email": "ivan@test.com",
        "telephone": "123456789"
    }

    customer_id = create_customer(connection, data)

    customer = get_customer_by_id(connection, customer_id)

    assert customer is not None
    assert customer["firstname"] == "Ivan"


def test_update_customer(connection):

    data = {
        "firstname": "Test",
        "lastname": "User",
        "email": "test@test.com",
        "telephone": "111111"
    }

    customer_id = create_customer(connection, data)

    new_data = {
        "firstname": "Updated",
        "lastname": "User",
        "email": "updated@test.com",
        "telephone": "222222"
    }

    update_customer(connection, customer_id, new_data)

    customer = get_customer_by_id(connection, customer_id)

    assert customer["firstname"] == "Updated"
    assert customer["email"] == "updated@test.com"


def test_update_nonexistent_customer(connection):

    data = {
        "firstname": "AAA",
        "lastname": "BBB",
        "email": "ccc@test.com",
        "telephone": "000"
    }

    rows = update_customer(connection, 99999999, data)

    assert rows == 0


def test_delete_customer(connection):

    data = {
        "firstname": "Delete",
        "lastname": "Me",
        "email": "delete@test.com",
        "telephone": "333333"
    }

    customer_id = create_customer(connection, data)

    delete_customer(connection, customer_id)

    customer = get_customer_by_id(connection, customer_id)

    assert customer is None


def test_delete_nonexistent_customer(connection):

    rows = delete_customer(connection, 99999999)

    assert rows == 0