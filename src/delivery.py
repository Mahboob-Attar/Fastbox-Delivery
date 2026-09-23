"""Walk each agent through its assigned packages and total the distance.

Packages are processed in their original input order. The agent starts at
its own location; for each package it travels current -> warehouse ->
destination, and the destination becomes its new current location for the
next package. There is no return trip to the start.
"""

from .distance import euclidean_distance


def simulate_deliveries(warehouses, agents, assignments):
    """Return {agent_id: {"packages": [...], "total_distance": float}}."""
    results = {}

    for agent_id, agent in agents.items():
        packages = assignments.get(agent_id, [])
        current_location = agent.location
        total_distance = 0.0

        for package in packages:
            warehouse = warehouses[package.warehouse_id]
            total_distance += euclidean_distance(current_location, warehouse.location)
            total_distance += euclidean_distance(warehouse.location, package.destination)
            current_location = package.destination

        results[agent_id] = {"packages": packages, "total_distance": total_distance}

    return results
