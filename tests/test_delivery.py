import math

from src.delivery import simulate_deliveries
from src.models import Agent, Package, Point, Warehouse


def test_single_package_route():
    warehouses = {"W1": Warehouse("W1", Point(0, 0))}
    agents = {"A1": Agent("A1", Point(3, 0))}
    package = Package("P1", "W1", Point(0, 4))

    results = simulate_deliveries(warehouses, agents, {"A1": [package]})

    # agent -> warehouse (3) + warehouse -> destination (4)
    assert math.isclose(results["A1"]["total_distance"], 7.0)


def test_agent_with_no_packages():
    warehouses = {"W1": Warehouse("W1", Point(0, 0))}
    agents = {"A1": Agent("A1", Point(3, 0))}

    results = simulate_deliveries(warehouses, agents, {"A1": []})

    assert results["A1"]["total_distance"] == 0.0
    assert results["A1"]["packages"] == []


def test_second_package_starts_from_first_destination():
    warehouses = {"W1": Warehouse("W1", Point(0, 0))}
    agents = {"A1": Agent("A1", Point(0, 0))}
    p1 = Package("P1", "W1", Point(10, 0))
    p2 = Package("P2", "W1", Point(10, 5))

    results = simulate_deliveries(warehouses, agents, {"A1": [p1, p2]})

    # leg 1: (0,0)->W1 = 0, W1->(10,0) = 10
    # leg 2: (10,0)->W1 = 10, W1->(10,5) = sqrt(125)
    expected = 0 + 10 + 10 + math.hypot(10, 5)
    assert math.isclose(results["A1"]["total_distance"], expected)


def test_agents_simulated_independently():
    warehouses = {"W1": Warehouse("W1", Point(0, 0)), "W2": Warehouse("W2", Point(100, 100))}
    agents = {"A1": Agent("A1", Point(0, 0)), "A2": Agent("A2", Point(100, 100))}
    p1 = Package("P1", "W1", Point(3, 4))
    p2 = Package("P2", "W2", Point(103, 104))

    results = simulate_deliveries(warehouses, agents, {"A1": [p1], "A2": [p2]})

    assert math.isclose(results["A1"]["total_distance"], 5.0)
    assert math.isclose(results["A2"]["total_distance"], 5.0)
