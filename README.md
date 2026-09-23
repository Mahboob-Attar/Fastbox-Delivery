# FastBox Mystery Delivery System

## Overview

Given a set of warehouses, delivery agents, and packages, this program:

1. Assigns each package to the nearest agent (distance from agent to the
   package's **warehouse**, not its destination).
2. Simulates each agent's route for the day, in order, tracking where the
   agent actually is after each delivery.
3. Calculates total distance and efficiency per agent.
4. Picks the most efficient agent.
5. Writes `report.json` and prints a short summary.

## Input format

Two shapes are supported, since both appear in the supplied files:

**Dict style** (`test_case_1.json` ... `test_case_10.json`):

```json
{
  "warehouses": {"W1": [0, 0]},
  "agents": {"A1": [5, 5]},
  "packages": [{"id": "P1", "warehouse": "W1", "destination": [1, 1]}]
}
```

**List style** (`base_case.json`):

```json
{
  "warehouses": [{"id": "W1", "location": [0, 0]}],
  "agents": [{"id": "A1", "location": [5, 5]}],
  "packages": [{"id": "P1", "warehouse_id": "W1", "destination": [1, 1]}]
}
```

`src/data_loader.py` detects which shape it's looking at and converts both
into the same `Warehouse` / `Agent` / `Package` objects, so nothing
downstream cares which format was used. Warehouse and agent counts, and
package counts, are never assumed — everything is read from the file.

## How to run

```bash
python -m venv .venv
source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -r requirements.txt

python -m src.main                              # uses base_case.json
python -m src.main --input test_case_3.json
python -m src.main --input test_case_3.json --output report.json
```

Optional flags:

| Flag | What it does |
|---|---|
| `--random-delays --seed N` | Prints a random delay per delivery (does not affect distance or efficiency) |
| `--ascii-routes` | Prints each agent's route as a simple diagram |
| `--csv-export PATH` | Writes the top performer's stats to a CSV file |

## How to run tests

```bash
pytest
```

`tests/test_all_cases.py` runs the whole pipeline (load -> assign ->
simulate -> report) against every file matching `base_case.json` /
`test_case_*.json` in the project root and checks that every package is
delivered exactly once. Nothing about the 11 supplied files is hardcoded.

## Algorithm

**Assignment.** For each package, compute the distance from every agent's
starting location to the package's warehouse, and assign it to the
smallest one. Ties go to the lexicographically smaller agent id.

**Distance.** Standard Euclidean distance, `sqrt((x2-x1)^2 + (y2-y1)^2)`,
via `math.hypot`.

**Delivery simulation.** Each agent processes its packages in the order
they appeared in the input. Starting from the agent's own location, each
package adds `distance(current, warehouse) + distance(warehouse,
destination)` to the running total, and `current` becomes that
destination for the next package. No return trip to the start.

**Efficiency.** `total_distance / packages_delivered`, rounded to 2
decimals. An agent with zero packages gets `0` for everything instead of
a division error.

**Best agent.** The agent with the lowest efficiency among those who
delivered at least one package — not the one with the lowest total
distance. Ties go to the smaller agent id. If nobody delivered anything,
`best_agent` is `null`.

## Time complexity

With `A` agents and `P` packages:

* Assignment checks every agent for every package: `O(P × A)`.
* Delivery simulation visits every package once: `O(P)`.
* Reporting is one pass over the agents: `O(A)`.

Overall: `O(P × A)`.

## Project layout

```text
src/
├── data_loader.py   # read + normalize + validate the input file
├── models.py        # Point, Warehouse, Agent, Package, SimulationData
├── distance.py       # euclidean_distance
├── assignment.py      # nearest-agent assignment
├── delivery.py         # route simulation
├── reporter.py          # report + CSV export
└── main.py              # CLI: wires the above together

tests/
├── test_distance.py
├── test_assignment.py
├── test_delivery.py
├── test_reporter.py
├── test_data_loader.py
└── test_all_cases.py    # runs every supplied file end-to-end
```

## Bonus features

* **Random delivery delays** — a seeded `random.Random` generates a delay
  per delivery in `main.py`, printed separately from the report so it can
  never affect distance or efficiency.
* **ASCII route display** — prints each agent's stops as a simple
  step-by-step diagram.
* **CSV export** — `reporter.export_top_performer_csv` writes the best
  agent's row with the standard `csv` module.

"New agent joining mid-day" wasn't implemented — there's no single obvious
rule for exactly when a mid-simulation agent should start being considered
without adding real scheduling, so it was left out rather than guessed at.
# Fastbox-Delivery
