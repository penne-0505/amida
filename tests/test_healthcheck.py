from __future__ import annotations

import io

from amida_bot.healthcheck import HealthState, _build_handler


def test_health_state_returns_starting_before_ready() -> None:
    state = HealthState(service="amida-bot", version="0.1.0")

    status, payload = state.response()

    assert status == 503
    assert payload["status"] == "error"
    assert payload["reason"] == "bot is starting"


def test_health_state_returns_disconnected_after_gateway_loss() -> None:
    state = HealthState(service="amida-bot", version="0.1.0")
    state.mark_ready()
    state.mark_gateway_disconnected()

    status, payload = state.response()

    assert status == 503
    assert payload["status"] == "error"
    assert payload["reason"] == "discord gateway disconnected"


def test_healthcheck_handler_serves_status_code_and_json_body() -> None:
    state = HealthState(service="amida-bot", version="0.1.0")
    handler = _build_handler(path="/healthz", state=state)

    response = _dispatch(handler, b"GET /healthz HTTP/1.1\r\nHost: localhost\r\n\r\n")

    assert b"HTTP/1.1 503 Service Unavailable" in response
    assert b"Content-Type: application/json; charset=utf-8" in response
    assert b"Cache-Control: no-store" in response
    assert b'"reason": "bot is starting"' in response

    state.mark_ready()

    response = _dispatch(handler, b"GET /healthz HTTP/1.1\r\nHost: localhost\r\n\r\n")

    assert b"HTTP/1.1 200 OK" in response
    assert b'"status": "ok"' in response
    assert b'"service": "amida-bot"' in response
    assert b'"version": "0.1.0"' in response


def _dispatch(handler_class: type, raw_request: bytes) -> bytes:
    socket = _FakeSocket(raw_request)
    handler_class(socket, ("127.0.0.1", 0), object())
    return socket.wfile.getvalue()


class _FakeSocket:
    def __init__(self, raw_request: bytes) -> None:
        self.rfile = io.BytesIO(raw_request)
        self.wfile = io.BytesIO()

    def makefile(self, mode: str, *args, **kwargs):  # noqa: ANN002, ANN003
        if "r" in mode:
            return self.rfile
        if "w" in mode:
            return self.wfile
        raise ValueError(f"unsupported mode: {mode}")

    def sendall(self, data: bytes) -> None:
        self.wfile.write(data)

    def close(self) -> None:
        pass
