import pytest

from lib.db import (
    create_customer,
    get_customer_by_id,
    update_customer,
    delete_customer
)


@pytest.fixture
def customer_data():
    return {
        "firstname": "Test",
        "lastname": "User",
        "email": "test@test.com",
        "telephone": "111111"
    }


@pytest.fixture
def customer_id(connection, customer_data):
    created_id = create_customer(connection, customer_data)

    yield created_id

    delete_customer(connection, created_id)


def test_create_customer(connection, customer_data):

    customer_id = create_customer(connection, customer_data)

    customer = get_customer_by_id(connection, customer_id)

    assert customer is not None
    assert customer["firstname"] == customer_data["firstname"]

    delete_customer(connection, customer_id)


def test_update_customer(connection, customer_id):

    new_data = {
        "firstname": "Updated",
        "lastname": "User",
        "email": "updated@test.com",
        "telephone": "222222"
    }

    update_customer(connection, customer_id, new_data)

    customer = get_customer_by_id(connection, customer_id)

    assert customer["firstname"] == "Updated"
    assert customer["lastname"] == "User"
    assert customer["email"] == "updated@test.com"
    assert customer["telephone"] == "222222"


def test_update_nonexistent_customer(connection, customer_data):

    rows = update_customer(connection, 99999999, customer_data)

    assert rows == 0


def test_delete_customer(connection, customer_id):

    delete_customer(connection, customer_id)

    customer = get_customer_by_id(connection, customer_id)

    assert customer is None


def test_delete_nonexistent_customer(connection):

    rows = delete_customer(connection, 99999999)

    assert rows == 0