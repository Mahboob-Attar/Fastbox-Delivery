"""Build report.json from simulated delivery results."""

import csv
import json


def generate_report(delivery_results):
    """Build the report dict: per-agent stats plus 'best_agent'.

    efficiency = total_distance / packages_delivered, rounded to 2 decimals.
    An agent with zero packages gets 0 for every field. best_agent is the
    agent with the lowest efficiency among agents that delivered at least
    one package (ties broken by the smaller agent id); None if nobody did.
    """
    report = {}

    for agent_id, result in delivery_results.items():
        count = len(result["packages"])
        if count == 0:
            report[agent_id] = {
                "packages_delivered": 0,
                "total_distance": 0.0,
                "efficiency": 0.0,
            }
        else:
            distance = result["total_distance"]
            report[agent_id] = {
                "packages_delivered": count,
                "total_distance": round(distance, 2),
                "efficiency": round(distance / count, 2),
            }

    delivered = [(aid, stats["efficiency"]) for aid, stats in report.items() if stats["packages_delivered"] > 0]
    report["best_agent"] = min(delivered, key=lambda item: (item[1], item[0]))[0] if delivered else None

    return report


def save_report(report, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)


def export_top_performer_csv(report, path):
    """Bonus: write the best agent's row to a CSV file."""
    best_agent_id = report.get("best_agent")
    if not best_agent_id:
        return
    stats = report[best_agent_id]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["agent_id", "packages_delivered", "total_distance", "efficiency"])
        writer.writerow([best_agent_id, stats["packages_delivered"], stats["total_distance"], stats["efficiency"]])
