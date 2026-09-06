import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../src")
    )
)

import monitor


def test_cpu_returns_result():
    result = monitor.check_cpu()

    assert result["check"] == "cpu"
    assert result["status"] in ["OK", "WARNING"]
    assert isinstance(result["value"], float)


def test_memory_returns_result():
    result = monitor.check_memory()

    assert result["check"] == "memory"
    assert result["status"] in ["OK", "WARNING"]


def test_disk_returns_result():
    result = monitor.check_disk()

    assert result["check"] == "disk"
    assert result["status"] in ["OK", "WARNING"]


def test_process_returns_result():
    result = monitor.check_process("bash")

    assert result["check"] == "process"
    assert result["status"] in ["OK", "WARNING"]


def test_tcp_success():
    result = monitor.check_tcp(
        "127.0.0.1",
        8000
    )

    assert result["check"] == "tcp"
    assert result["status"] == "UP"


def test_http_success():
    result = monitor.check_http(
        "http://127.0.0.1:8000/health"
    )

    assert result["check"] == "http"
    assert result["status"] == "UP"
