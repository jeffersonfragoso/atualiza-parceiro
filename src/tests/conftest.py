import pytest


@pytest.fixture
def app_test():
    from src.entrypoints.web.main import app

    # sobscrever por dependencias de teste
    # app.dependency_overrides[auth] = auth_test
    # app.dependency_overrides[database] = database_test

    yield app
