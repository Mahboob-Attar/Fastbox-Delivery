import json

import pytest

from src.data_loader import FastBoxError, load_data

DICT_STYLE = {
    "warehouses": {"W1": [0, 0], "W2": [50, 75]},
    "agents": {"A1": [5, 5], "A2": [60, 60]},
    "packages": [
        {"id": "P1", "warehouse": "W1", "destination": [30, 40]},
        {"id": "P2", "warehouse": "W2", "destination": [70, 90]},
    ],
}

LIST_STYLE = {
    "warehouses": [{"id": "W1", "location": [0, 0]}],
    "agents": [{"id": "A1", "location": [5, 5]}],
    "packages": [{"id": "P1", "warehouse_id": "W1", "destination": [1, 1]}],
}


def write(tmp_path, payload, name="data.json"):
    path = tmp_path / name
    text = payload if isinstance(payload, str) else json.dumps(payload)
    path.write_text(text, encoding="utf-8")
    return path


def test_dict_style_input(tmp_path):
    data = load_data(write(tmp_path, DICT_STYLE))
    assert set(data.warehouses) == {"W1", "W2"}
    assert set(data.agents) == {"A1", "A2"}
    assert len(data.packages) == 2


def test_list_style_input(tmp_path):
    data = load_data(write(tmp_path, LIST_STYLE))
    assert data.warehouses["W1"].location.x == 0
    assert data.agents["A1"].location.y == 5
    assert data.packages[0].warehouse_id == "W1"


def test_missing_file(tmp_path):
    with pytest.raises(FastBoxError):
        load_data(tmp_path / "missing.json")


def test_invalid_json(tmp_path):
    with pytest.raises(FastBoxError):
        load_data(write(tmp_path, "{not json", name="bad.json"))


def test_unknown_warehouse_reference(tmp_path):
    payload = json.loads(json.dumps(DICT_STYLE))
    payload["packages"].append({"id": "P9", "warehouse": "W404", "destination": [1, 1]})
    with pytest.raises(FastBoxError, match="W404"):
        load_data(write(tmp_path, payload))


def test_missing_destination(tmp_path):
    payload = json.loads(json.dumps(DICT_STYLE))
    del payload["packages"][0]["destination"]
    with pytest.raises(FastBoxError):
        load_data(write(tmp_path, payload))


def test_non_numeric_coordinates(tmp_path):
    payload = json.loads(json.dumps(DICT_STYLE))
    payload["warehouses"]["W1"] = ["a", "b"]
    with pytest.raises(FastBoxError):
        load_data(write(tmp_path, payload))
