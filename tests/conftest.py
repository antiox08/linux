import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pytest
import threading
import time

from echo_server.server import run_server

HOST = "127.0.0.1"
PORT = 8080


@pytest.fixture(scope="session")
def host():
    return HOST


@pytest.fixture(scope="session")
def port():
    return PORT


@pytest.fixture(scope="session", autouse=True)
def start_server():
    thread = threading.Thread(
        target=run_server,
        kwargs={"host": HOST, "port": PORT},
        daemon=True
    )

    thread.start()

    time.sleep(1)

    yield