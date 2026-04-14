def calculate_scholarship_v2(student, rules):
    percent_total = 0
    flat_total = 0

    applicable_rules = []

    for rule in rules:
        ctype = rule["criteria_type"]
        value = student.get(ctype.lower())

        if value is None:
            continue

        if ctype in ["SPORTS", "NCC", "ACADEMIC_TOPPER"]:
            if value == rule["min_value"]:
                applicable_rules.append(rule)
        else:
            if rule["min_value"] <= value <= rule["max_value"]:
                applicable_rules.append(rule)

    applicable_rules.sort(key=lambda x: x["priority"])

    non_stackable = [r for r in applicable_rules if not r["stackable"]]
    stackable = [r for r in applicable_rules if r["stackable"]]

    if non_stackable:
        best = max(non_stackable, key=lambda x: x["scholarship_percent"])
        if best["scholarship_type"] == "PERCENT":
            percent_total += best["scholarship_percent"]
        else:
            flat_total += best["scholarship_percent"]

    for r in stackable:
        if r["scholarship_type"] == "PERCENT":
            percent_total += r["scholarship_percent"]
        else:
            flat_total += r["scholarship_percent"]

    percent_total = min(percent_total, 100)

    return {"percent": percent_total, "flat": flat_total}