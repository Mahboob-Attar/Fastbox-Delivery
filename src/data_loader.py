"""Load an input JSON file into Warehouse/Agent/Package objects.

Two input shapes show up in the supplied test files and both are supported:

  Dict style (test_case_*.json):
      "warehouses": {"W1": [0, 0]}
      "agents":     {"A1": [5, 5]}
      "packages":   [{"id": "P1", "warehouse": "W1", "destination": [1, 1]}]

  List style (base_case.json):
      "warehouses": [{"id": "W1", "location": [0, 0]}]
      "agents":     [{"id": "A1", "location": [5, 5]}]
      "packages":   [{"id": "P1", "warehouse_id": "W1", "destination": [1, 1]}]

Both are normalized into the same Warehouse/Agent/Package objects before
anything else touches them.
"""

import json
from pathlib import Path

from .models import Agent, Package, Point, SimulationData, Warehouse


class FastBoxError(Exception):
    """Raised for any invalid input or broken invariant."""


def load_data(path):
    """Read, parse, and validate an input file. Returns a SimulationData."""
    raw = _read_json(path)

    if not isinstance(raw, dict):
        raise FastBoxError("Input file must contain a JSON object.")

    warehouses = _load_warehouses(raw.get("warehouses"))
    agents = _load_agents(raw.get("agents"))
    packages = _load_packages(raw.get("packages"), warehouses)

    return SimulationData(warehouses=warehouses, agents=agents, packages=packages)


def _read_json(path):
    file_path = Path(path)
    if not file_path.exists():
        raise FastBoxError(f"Input file not found: {path}")
    try:
        with file_path.open(encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise FastBoxError(f"Input file is not valid JSON: {exc}") from exc


def _parse_point(coord, what):
    if not isinstance(coord, (list, tuple)) or len(coord) != 2:
        raise FastBoxError(f"{what} must be a [x, y] coordinate, got {coord!r}.")
    x, y = coord
    if isinstance(x, bool) or isinstance(y, bool) or not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise FastBoxError(f"{what} coordinates must be numbers, got {coord!r}.")
    return Point(float(x), float(y))


def _load_warehouses(raw):
    if not raw:
        raise FastBoxError("'warehouses' is missing or empty.")

    warehouses = {}
    if isinstance(raw, dict):
        for warehouse_id, coord in raw.items():
            warehouses[warehouse_id] = Warehouse(
                warehouse_id, _parse_point(coord, f"Warehouse '{warehouse_id}'")
            )
    elif isinstance(raw, list):
        for entry in raw:
            if not isinstance(entry, dict) or "id" not in entry or "location" not in entry:
                raise FastBoxError(f"Invalid warehouse entry: {entry!r}")
            warehouse_id = entry["id"]
            warehouses[warehouse_id] = Warehouse(
                warehouse_id, _parse_point(entry["location"], f"Warehouse '{warehouse_id}'")
            )
    else:
        raise FastBoxError("'warehouses' must be an object or a list.")

    return warehouses


def _load_agents(raw):
    if not raw:
        raise FastBoxError("'agents' is missing or empty.")

    agents = {}
    if isinstance(raw, dict):
        for agent_id, coord in raw.items():
            agents[agent_id] = Agent(agent_id, _parse_point(coord, f"Agent '{agent_id}'"))
    elif isinstance(raw, list):
        for entry in raw:
            if not isinstance(entry, dict) or "id" not in entry or "location" not in entry:
                raise FastBoxError(f"Invalid agent entry: {entry!r}")
            agent_id = entry["id"]
            agents[agent_id] = Agent(
                agent_id, _parse_point(entry["location"], f"Agent '{agent_id}'")
            )
    else:
        raise FastBoxError("'agents' must be an object or a list.")

    return agents


def _load_packages(raw, warehouses):
    if not raw:
        raise FastBoxError("'packages' is missing or empty.")
    if not isinstance(raw, list):
        raise FastBoxError("'packages' must be a list.")

    packages = []
    seen_ids = set()

    for entry in raw:
        if not isinstance(entry, dict):
            raise FastBoxError(f"Invalid package entry: {entry!r}")

        package_id = entry.get("id")
        if not package_id:
            raise FastBoxError(f"Package is missing an 'id': {entry!r}")
        if package_id in seen_ids:
            raise FastBoxError(f"Duplicate package id '{package_id}'.")
        seen_ids.add(package_id)

        warehouse_id = entry.get("warehouse") or entry.get("warehouse_id")
        if not warehouse_id:
            raise FastBoxError(f"Package '{package_id}' is missing a warehouse reference.")
        if warehouse_id not in warehouses:
            raise FastBoxError(
                f"Package '{package_id}' references warehouse '{warehouse_id}', "
                "but it does not exist."
            )

        destination = entry.get("destination")
        if destination is None:
            raise FastBoxError(f"Package '{package_id}' is missing a 'destination'.")
        point = _parse_point(destination, f"Package '{package_id}' destination")

        packages.append(Package(package_id, warehouse_id, point))

    return packages
