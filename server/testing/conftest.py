#!/usr/bin/env python3
import sys
from unittest.mock import MagicMock
import pytest

fake_module = MagicMock()
fake_instance = MagicMock()
fake_instance.first_name.return_value = "TestUser"
fake_instance.sentence.return_value = "Test Sentence"
fake_module.Faker.return_value = fake_instance
sys.modules['faker'] = fake_module

from app import app
from models import db
from seed import make_messages

@pytest.fixture(scope='session', autouse=True)
def setup_db():
    with app.app_context():
        db.create_all()
        make_messages()
        yield
        db.session.remove()
        db.drop_all()

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))