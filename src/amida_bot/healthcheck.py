from __future__ import annotations

import json
import logging
import threading
import time
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.metadata import PackageNotFoundError, version as get_version
from urllib.parse import urlsplit

logger = logging.getLogger(__name__)

SERVICE_NAME = "amida-bot"


def resolve_service_version() -> str:
    try:
        return get_version(SERVICE_NAME)
    except PackageNotFoundError:
        return "unknown"


class HealthState:
    def __init__(self, service: str, version: str) -> None:
        self._service = service
        self._version = version
        self._started_at = time.monotonic()
        self._lock = threading.Lock()
        self._is_ready = False
        self._gateway_connected = False
        self._is_closing = False

    def mark_ready(self) -> None:
        with self._lock:
            self._is_ready = True
            self._gateway_connected = True
            self._is_closing = False

    def mark_gateway_disconnected(self) -> None:
        with self._lock:
            self._gateway_connected = False

    def mark_closing(self) -> None:
        with self._lock:
            self._is_ready = False
            self._gateway_connected = False
            self._is_closing = True

    def response(self) -> tuple[int, dict[str, object]]:
        with self._lock:
            is_ready = self._is_ready
            gateway_connected = self._gateway_connected
            is_closing = self._is_closing

        payload: dict[str, object] = {
            "service": self._service,
            "version": self._version,
            "timestamp": _utc_timestamp(),
            "uptime_seconds": int(time.monotonic() - self._started_at),
        }

        if is_ready and gateway_connected and not is_closing:
            payload["status"] = "ok"
            return HTTPStatus.OK, payload

        payload["status"] = "error"
        payload["reason"] = _resolve_unhealthy_reason(
            is_ready=is_ready,
            gateway_connected=gateway_connected,
            is_closing=is_closing,
        )
        return HTTPStatus.SERVICE_UNAVAILABLE, payload


class HealthCheckServer:
    def __init__(self, host: str, port: int, path: str, state: HealthState) -> None:
        self._host = host
        self._port = port
        self._path = path
        self._state = state
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    @property
    def port(self) -> int:
        if self._server is None:
            return self._port
        return int(self._server.server_address[1])

    def start(self) -> None:
        if self._server is not None:
            return

        server = ThreadingHTTPServer(
            (self._host, self._port),
            _build_handler(path=self._path, state=self._state),
        )
        thread = threading.Thread(
            target=server.serve_forever,
            name="amida-healthcheck",
            daemon=True,
        )
        thread.start()

        self._server = server
        self._thread = thread

    def shutdown(self) -> None:
        if self._server is None:
            return

        self._server.shutdown()
        self._server.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)

        self._server = None
        self._thread = None


def _build_handler(path: str, state: HealthState) -> type[BaseHTTPRequestHandler]:
    class HealthCheckHandler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_GET(self) -> None:  # noqa: N802
            self._handle_request(include_body=True)

        def do_HEAD(self) -> None:  # noqa: N802
            self._handle_request(include_body=False)

        def log_message(self, format: str, *args: object) -> None:
            logger.debug("healthcheck %s - %s", self.client_address[0], format % args)

        def _handle_request(self, *, include_body: bool) -> None:
            if urlsplit(self.path).path != path:
                self._write_json(
                    status=HTTPStatus.NOT_FOUND,
                    payload={"status": "error", "reason": "not found"},
                    include_body=include_body,
                )
                return

            status, payload = state.response()
            self._write_json(status=status, payload=payload, include_body=include_body)

        def _write_json(
            self,
            *,
            status: int,
            payload: dict[str, object],
            include_body: bool,
        ) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            if include_body:
                self.wfile.write(body)

    return HealthCheckHandler


def _resolve_unhealthy_reason(
    *,
    is_ready: bool,
    gateway_connected: bool,
    is_closing: bool,
) -> str:
    if is_closing:
        return "bot is shutting down"
    if not is_ready:
        return "bot is starting"
    if not gateway_connected:
        return "discord gateway disconnected"
    return "health check degraded"


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
