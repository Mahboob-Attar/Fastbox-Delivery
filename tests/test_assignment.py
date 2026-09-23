from src.assignment import assign_packages
from src.models import Agent, Package, Point, Warehouse


def test_package_goes_to_nearest_agent():
    warehouses = {"W1": Warehouse("W1", Point(0, 0))}
    agents = {
        "A1": Agent("A1", Point(5, 5)),
        "A2": Agent("A2", Point(1, 1)),  # closest to W1
        "A3": Agent("A3", Point(50, 50)),
    }
    packages = [Package("P1", "W1", Point(30, 40))]

    result = assign_packages(warehouses, agents, packages)

    assert result["A2"] == packages
    assert result["A1"] == []
    assert result["A3"] == []


def test_assignment_uses_warehouse_not_destination():
    # A1 is near the destination but far from the warehouse; A2 is the
    # opposite. The agent closer to the warehouse must win.
    warehouses = {"W1": Warehouse("W1", Point(0, 0))}
    agents = {
        "A1": Agent("A1", Point(100, 100)),
        "A2": Agent("A2", Point(1, 1)),
    }
    packages = [Package("P1", "W1", Point(99, 99))]

    result = assign_packages(warehouses, agents, packages)

    assert result["A2"] == packages
    assert result["A1"] == []


def test_tie_goes_to_smaller_agent_id():
    warehouses = {"W1": Warehouse("W1", Point(0, 0))}
    agents = {"A2": Agent("A2", Point(10, 0)), "A1": Agent("A1", Point(0, 10))}
    packages = [Package("P1", "W1", Point(5, 5))]

    result = assign_packages(warehouses, agents, packages)

    assert result["A1"] == packages
    assert result["A2"] == []


def test_every_agent_included_even_with_zero_packages():
    warehouses = {"W1": Warehouse("W1", Point(0, 0))}
    agents = {"A1": Agent("A1", Point(0, 0)), "A2": Agent("A2", Point(1, 1))}
    packages = [Package("P1", "W1", Point(5, 5))]

    result = assign_packages(warehouses, agents, packages)

    assert set(result.keys()) == {"A1", "A2"}
    assert result["A2"] == []


def test_original_package_order_preserved_per_agent():
    warehouses = {"W1": Warehouse("W1", Point(0, 0))}
    agents = {"A1": Agent("A1", Point(0, 0))}
    packages = [
        Package("P1", "W1", Point(1, 1)),
        Package("P2", "W1", Point(2, 2)),
        Package("P3", "W1", Point(3, 3)),
    ]

    result = assign_packages(warehouses, agents, packages)

    assert [p.id for p in result["A1"]] == ["P1", "P2", "P3"]
