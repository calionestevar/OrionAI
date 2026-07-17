# tests/conftest.py
import pytest
import os

@pytest.fixture(scope="session", autouse=True)
def disable_transformers():
    """Disable transformers model loading for faster tests"""
    os.environ["ORIONAI_DISABLE_ML"] = "1"


@pytest.fixture(scope="session")
def orion():
    """Global OrionAI instance for all tests"""
    from orionai import OrionAI
    return OrionAI()


@pytest.fixture(scope="session")
def genesis():
    """Global Genesis instance for all tests"""
    from orionai import Genesis
    return Genesis("test-model")