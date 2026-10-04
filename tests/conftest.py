import pytest

from homepilot_domain import Service, Store, seed_demo


@pytest.fixture
def svc():
    store = Store()
    store.put(seed_demo())
    return Service(store)
