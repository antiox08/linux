import pytest
import pymysql


def pytest_addoption(parser):
    parser.addoption("--host", default="localhost")
    parser.addoption("--port", default=3306, type=int)
    parser.addoption("--database", default="bitnami_opencart")
    parser.addoption("--user", default="root")
    parser.addoption("--password", default="root")


@pytest.fixture(scope="session")
def connection(request):

    host = request.config.getoption("--host")
    port = request.config.getoption("--port")
    database = request.config.getoption("--database")
    user = request.config.getoption("--user")
    password = request.config.getoption("--password")

    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor
    )

    yield connection

    connection.close()