"""FastBox CLI.

    python -m src.main
    python -m src.main --input test_case_3.json
    python -m src.main --input test_case_3.json --output report.json
"""

import argparse
import random
import sys

from .assignment import assign_packages
from .data_loader import FastBoxError, load_data
from .delivery import simulate_deliveries
from .reporter import export_top_performer_csv, generate_report, save_report

DEFAULT_INPUT = "base_case.json"
DEFAULT_OUTPUT = "report.json"


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Simulate one day of FastBox deliveries.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help=f"input JSON file (default: {DEFAULT_INPUT})")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help=f"report output path (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--random-delays", action="store_true", help="bonus: print a random delay per delivery")
    parser.add_argument("--seed", type=int, default=None, help="seed for --random-delays")
    parser.add_argument("--ascii-routes", action="store_true", help="bonus: print each agent's route")
    parser.add_argument("--csv-export", metavar="PATH", default=None, help="bonus: export top performer to CSV")
    return parser.parse_args(argv)


def verify_invariants(data, delivery_results):
    """Every input package must show up exactly once across all agents."""
    delivered_ids = [p.id for result in delivery_results.values() for p in result["packages"]]
    input_ids = [p.id for p in data.packages]

    if len(delivered_ids) != len(set(delivered_ids)):
        raise FastBoxError("A package was assigned to more than one agent.")
    if sorted(delivered_ids) != sorted(input_ids):
        raise FastBoxError("Delivered packages do not match the input packages.")


def print_summary(data, report):
    print("FastBox Delivery Simulation")
    print("=" * 27)
    print()
    print(f"Packages processed: {len(data.packages)}")
    print()

    for agent_id in data.agents:
        stats = report[agent_id]
        print(f"{agent_id}:")
        print(f"  Packages delivered: {stats['packages_delivered']}")
        print(f"  Total distance: {stats['total_distance']:.2f}")
        print(f"  Efficiency: {stats['efficiency']:.2f}")
        print()

    best_agent = report.get("best_agent")
    print(f"Best agent: {best_agent if best_agent else 'N/A (no deliveries made)'}")


def print_ascii_routes(delivery_results):
    print("\nRoutes:\n")
    for agent_id, result in delivery_results.items():
        print(f"{agent_id} ROUTE\n\nStart")
        for package in result["packages"]:
            print(f"  |\n  v\n{package.warehouse_id}\n  |\n  v\n{package.id} Destination")
        print()


def print_random_delays(delivery_results, seed):
    rng = random.Random(seed)
    print("\nSimulated delivery delays (informational only, not part of distance):")
    for agent_id, result in delivery_results.items():
        delays = [round(rng.uniform(0, 15), 2) for _ in result["packages"]]
        if delays:
            print(f"  {agent_id}: {delays}")


def run(argv=None):
    args = parse_args(argv)

    try:
        data = load_data(args.input)
        assignments = assign_packages(data.warehouses, data.agents, data.packages)
        delivery_results = simulate_deliveries(data.warehouses, data.agents, assignments)
        verify_invariants(data, delivery_results)

        report = generate_report(delivery_results)
        save_report(report, args.output)

        print_summary(data, report)
        print(f"\nReport saved to: {args.output}")

        if args.random_delays:
            print_random_delays(delivery_results, args.seed)
        if args.ascii_routes:
            print_ascii_routes(delivery_results)
        if args.csv_export:
            export_top_performer_csv(report, args.csv_export)
            print(f"\nTop performer exported to: {args.csv_export}")

        return 0

    except FastBoxError as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(run())
