import csv

# ---------- LOAD RULES ----------
def load_rules():
    rules = {}

    with open("rules.csv", newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            college_id = int(row["college_id"])

            rule = {
                "criteria_type": row["criteria_type"],
                "min_value": convert_value(row["min_value"]),
                "max_value": convert_value(row["max_value"]),
                "scholarship_percent": float(row["scholarship_percent"]),
                "scholarship_type": row["scholarship_type"],
                "stackable": row["stackable"] == "TRUE",
                "priority": int(row["priority"])
            }

            if college_id not in rules:
                rules[college_id] = []

            rules[college_id].append(rule)

    return rules


def convert_value(val):
    try:
        return float(val)
    except:
        return val


RULES = load_rules()


# ---------- LOAD COLLEGES ----------
def load_colleges():
    colleges = {}

    with open("colleges.csv", newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            colleges[int(row["id"])] = row

    return colleges


COLLEGES = load_colleges()