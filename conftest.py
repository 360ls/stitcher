"""
Configuration for pytest.
"""

import pytest

def pytest_addoption(parser):
    """
    Controls running of opencv-required tests.
    """
    parser.addoption("--opencv", action="store_true", help="Run opencv-required tests.")
