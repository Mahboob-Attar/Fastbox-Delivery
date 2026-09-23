"""Runs the full pipeline against every supplied base_case/test_case file.

Doesn't hardcode expected assignments — just checks that each file loads,
every package ends up delivered exactly once, and a report can be built.
"""

from pathlib import Path

import pytest

from src.assignment import assign_packages
from src.data_loader import load_data
from src.delivery import simulate_deliveries
from src.reporter import generate_report

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILES = sorted(PROJECT_ROOT.glob("base_case.json")) + sorted(
    PROJECT_ROOT.glob("test_case_*.json")
)


@pytest.mark.parametrize("input_file", INPUT_FILES, ids=lambda p: p.name)
def test_full_pipeline_on_supplied_file(input_file):
    data = load_data(input_file)

    assignments = assign_packages(data.warehouses, data.agents, data.packages)
    delivery_results = simulate_deliveries(data.warehouses, data.agents, assignments)
    report = generate_report(delivery_results)

    delivered_ids = [p.id for result in delivery_results.values() for p in result["packages"]]
    input_ids = [p.id for p in data.packages]

    # no duplicates, no losses
    assert len(delivered_ids) == len(set(delivered_ids))
    assert sorted(delivered_ids) == sorted(input_ids)

    # every agent shows up in the report, plus best_agent
    assert set(report.keys()) == set(data.agents.keys()) | {"best_agent"}

    # packages_delivered sums to the input package count
    total_delivered = sum(report[agent_id]["packages_delivered"] for agent_id in data.agents)
    assert total_delivered == len(data.packages)


def test_at_least_the_eleven_supplied_files_were_found():
    assert len(INPUT_FILES) == 11
