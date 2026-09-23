"""Assign each package to the nearest agent (by distance to its warehouse)."""

from .distance import euclidean_distance


def assign_packages(warehouses, agents, packages):
    """Return {agent_id: [Package, ...]} for every agent (possibly empty).

    Distance is measured agent -> warehouse, never agent -> destination.
    Ties are broken by the smaller agent id, so results are deterministic.
    """
    assignments = {agent_id: [] for agent_id in agents}

    for package in packages:
        warehouse = warehouses[package.warehouse_id]

        nearest_agent = min(
            agents.values(),
            key=lambda agent: (euclidean_distance(agent.location, warehouse.location), agent.id),
        )
        assignments[nearest_agent.id].append(package)

    return assignments
