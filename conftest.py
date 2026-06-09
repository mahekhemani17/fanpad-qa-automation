import pytest
import time
from utils.helpers import send_completion_email

_start_time = None
_failed_tests = []

def pytest_sessionstart(session):
    global _start_time
    _start_time = time.time()

def pytest_runtest_logreport(report):
    if report.failed and report.when == "call":
        _failed_tests.append(report.nodeid)

def pytest_sessionfinish(session, exitstatus):
    global _start_time
    duration = f"{round(time.time() - _start_time)}s" if _start_time else "N/A"
    passed = session.testscollected - session.testsfailed
    failed = session.testsfailed
    send_completion_email(passed, failed, duration, _failed_tests)