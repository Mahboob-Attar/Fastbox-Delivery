from src.reporter import generate_report


def result(distance, count):
    return {"packages": list(range(count)), "total_distance": distance}


def test_efficiency_is_distance_over_package_count():
    report = generate_report({"A1": result(100.0, 4)})
    assert report["A1"]["efficiency"] == 25.0


def test_zero_packages_no_division_by_zero():
    report = generate_report({"A1": result(0.0, 0)})
    assert report["A1"] == {"packages_delivered": 0, "total_distance": 0.0, "efficiency": 0.0}


def test_best_agent_is_lowest_efficiency_not_lowest_distance():
    results = {
        "A1": result(40.0, 1),  # efficiency 40
        "A2": result(60.0, 3),  # efficiency 20, more distance but better
    }
    report = generate_report(results)
    assert report["best_agent"] == "A2"


def test_best_agent_tie_broken_by_smaller_id():
    results = {"A2": result(50.0, 1), "A1": result(50.0, 1)}
    report = generate_report(results)
    assert report["best_agent"] == "A1"


def test_best_agent_excludes_zero_package_agents():
    results = {"A1": result(0.0, 0), "A2": result(30.0, 1)}
    report = generate_report(results)
    assert report["best_agent"] == "A2"


def test_best_agent_none_when_nobody_delivered():
    results = {"A1": result(0.0, 0), "A2": result(0.0, 0)}
    report = generate_report(results)
    assert report["best_agent"] is None
