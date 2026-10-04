"""Persistence backends. A backend stores one JSON document per household."""
from __future__ import annotations

from pathlib import Path
from typing import Protocol


class Backend(Protocol):
    def load_all(self) -> dict[str, str]: ...
    def save(self, household_id: str, doc: str) -> None: ...


class JsonFileBackend:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load_all(self) -> dict[str, str]:
        import json
        if not self.path.exists():
            return {}
        return {k: json.dumps(v) for k, v in json.loads(self.path.read_text()).items()}

    def save(self, household_id: str, doc: str) -> None:
        import json
        data = json.loads(self.path.read_text()) if self.path.exists() else {}
        data[household_id] = json.loads(doc)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data))


class DynamoBackend:
    """DynamoDB table with partition key `household_id` (String); state stored as a JSON string attribute."""

    def __init__(self, table_name: str, region: str | None = None, client=None):
        import boto3
        self.table = table_name
        self.client = client or boto3.client("dynamodb", region_name=region)

    def load_all(self) -> dict[str, str]:
        out: dict[str, str] = {}
        for page in self.client.get_paginator("scan").paginate(TableName=self.table):
            for item in page["Items"]:
                out[item["household_id"]["S"]] = item["state"]["S"]
        return out

    def save(self, household_id: str, doc: str) -> None:
        self.client.put_item(TableName=self.table,
                             Item={"household_id": {"S": household_id}, "state": {"S": doc}})
