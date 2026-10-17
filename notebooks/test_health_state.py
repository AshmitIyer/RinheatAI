from ml.engineering.health_state import classify_health_state


TEST_CASES = [
    {
        "name": "Normal operation",
        "u_status": "NORMAL",
        "delta_p_status": "NORMAL",
        "u_change_1h": 0.0,
        "delta_p_change_1h": 0.0,
        "expected": "NORMAL",
    },
    {
        "name": "Low U only",
        "u_status": "LOW",
        "delta_p_status": "NORMAL",
        "u_change_1h": 0.0,
        "delta_p_change_1h": 0.0,
        "expected": "WATCH",
    },
    {
        "name": "High delta-P only",
        "u_status": "NORMAL",
        "delta_p_status": "HIGH",
        "u_change_1h": 0.0,
        "delta_p_change_1h": 0.0,
        "expected": "WATCH",
    },
    {
        "name": "Low U and high delta-P",
        "u_status": "LOW",
        "delta_p_status": "HIGH",
        "u_change_1h": 0.0,
        "delta_p_change_1h": 0.0,
        "expected": "DEGRADED",
    },
    {
        "name": "Low U with declining trend",
        "u_status": "LOW",
        "delta_p_status": "NORMAL",
        "u_change_1h": -10.0,
        "delta_p_change_1h": 0.0,
        "expected": "DEGRADED",
    },
    {
        "name": "High delta-P with increasing trend",
        "u_status": "NORMAL",
        "delta_p_status": "HIGH",
        "u_change_1h": 0.0,
        "delta_p_change_1h": 0.10,
        "expected": "DEGRADED",
    },
    {
        "name": "Strong combined deterioration",
        "u_status": "LOW",
        "delta_p_status": "HIGH",
        "u_change_1h": -10.0,
        "delta_p_change_1h": 0.10,
        "expected": "CRITICAL",
    },
]


print("=== Health State Tests ===")

for case in TEST_CASES:
    result = classify_health_state(
        u_status=case["u_status"],
        delta_p_status=case["delta_p_status"],
        u_change_1h=case["u_change_1h"],
        delta_p_change_1h=case["delta_p_change_1h"],
    )

    passed = result == case["expected"]

    print(
        f"{case['name']}: "
        f"{result} "
        f"{'PASS' if passed else 'FAIL'}"
    )

    assert passed

print("\nAll health-state tests passed.")
