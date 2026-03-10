import socket
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs

HOST = "127.0.0.1"
PORT = 8080


def parse_request(request_data):
    lines = request_data.split("\r\n")

    request_line = lines[0]
    method, path, _ = request_line.split()

    headers = {}
    for line in lines[1:]:
        if line == "":
            break
        name, value = line.split(":", 1)
        headers[name.strip()] = value.strip()

    return method, path, headers


def get_status_from_query(path):
    parsed = urlparse(path)
    params = parse_qs(parsed.query)

    if "status" not in params:
        return HTTPStatus.OK

    try:
        status_code = int(params["status"][0])
        return HTTPStatus(status_code)
    except Exception:
        return HTTPStatus.OK


def build_response(method, addr, headers, status):

    body_lines = [
        f"Request Method: {method}",
        f"Request Source: {addr}",
        f"Response Status: {status.value} {status.phrase}",
    ]

    for k, v in headers.items():
        body_lines.append(f"{k}: {v}")

    body = "\r\n".join(body_lines)

    response = (
        f"HTTP/1.1 {status.value} {status.phrase}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(body.encode())}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
        f"{body}"
    )

    return response.encode()


def run_server(host=HOST, port=PORT):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(10)

        print(f"Server started on {host}:{port}")

        while True:
            conn, addr = server.accept()

            with conn:
                data = conn.recv(65536).decode()

                if not data:
                    continue

                method, path, headers = parse_request(data)

                status = get_status_from_query(path)

                response = build_response(method, addr, headers, status)

                conn.sendall(response)