"""Domain objects used throughout the simulation."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Warehouse:
    id: str
    location: Point


@dataclass
class Agent:
    id: str
    location: Point


@dataclass
class Package:
    id: str
    warehouse_id: str
    destination: Point


@dataclass
class SimulationData:
    """Everything parsed out of an input file, grouped together."""

    warehouses: Dict[str, Warehouse]
    agents: Dict[str, Agent]
    packages: List[Package] = field(default_factory=list)
