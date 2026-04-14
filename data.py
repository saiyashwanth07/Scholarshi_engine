import csv

# ---------- HELPERS ----------
def convert_value(val):
    try:
        return float(val)
    except:
        return val


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

            rules.setdefault(college_id, []).append(rule)

    return rules


# ---------- LOAD COLLEGES ----------
def load_colleges():
    colleges = {}

    with open("colleges.csv", newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            colleges[int(row["id"])] = row

    return colleges


# ---------- LOAD COURSES ----------
def load_courses():
    courses = []

    with open("courses.csv", newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            courses.append(row)

    return courses


# ---------- LOAD FEES ----------
def load_fees():
    fees = {}

    with open("fees.csv", newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            fees[int(row["course_id"])] = float(row["total_fee"])

    return fees


# ---------- LOAD EVERYTHING SAFELY ----------
try:
    RULES = load_rules()
    COLLEGES = load_colleges()
    COURSES = load_courses()
    FEES = load_fees()
except Exception as e:
    print("Error loading data:", e)
    RULES, COLLEGES, COURSES, FEES = {}, {}, [], {}