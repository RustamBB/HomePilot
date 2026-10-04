import boto3
import pytest
from moto import mock_aws

from homepilot_domain import Commitment, Service, Store, seed_demo
from homepilot_domain.backends import DynamoBackend
from datetime import datetime


@pytest.fixture
def table(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "x"); monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "x")
    with mock_aws():
        c = boto3.client("dynamodb", region_name="us-east-1")
        c.create_table(TableName="hp", BillingMode="PAY_PER_REQUEST",
                       AttributeDefinitions=[{"AttributeName": "household_id", "AttributeType": "S"}],
                       KeySchema=[{"AttributeName": "household_id", "KeyType": "HASH"}])
        yield c


def test_state_survives_restart_via_dynamodb(table):
    s1 = Store(backend=DynamoBackend("hp", client=table)); s1.put(seed_demo())
    svc = Service(s1)
    p = svc.propose("demo", [Commitment(kind="task", title="Permission slip", person="ali",
                                        due_at=datetime(2026, 10, 19, 8))], "sam")
    svc.confirm("demo", p["id"], "sam")
    s2 = Store(backend=DynamoBackend("hp", client=table))  # "restart"
    s2svc = Service(s2)
    assert [t["title"] for t in s2svc.tasks("demo", "ali")] == ["Permission slip"]
    assert s2svc.audit("demo")[0]["tool"] == "confirm_plan"
