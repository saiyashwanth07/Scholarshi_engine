from fastapi import FastAPI
from pydantic import BaseModel
from engine import calculate_scholarship_v2
from data import RULES, COLLEGES, COURSES, FEES
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  # ✅ FIRST create app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StudentInput(BaseModel):
    jee_percentile: float | None = None
    board_percentage: float | None = None
    sports: str | None = None
    ncc: str | None = None

@app.post("/evaluate")
def evaluate(student: StudentInput):
    student = student.dict()
    results = []

    for college_id, rules in RULES.items():
        scholarship = calculate_scholarship_v2(student, rules)

        if scholarship["percent"] > 0 or scholarship["flat"] > 0:
            college_info = COLLEGES.get(college_id, {})

            # get courses of this college
            college_courses = [c for c in COURSES if int(c["college_id"]) == college_id]

            for course in college_courses:
                course_id = int(course["id"])
                total_fee = FEES.get(course_id, 0)

                percent = scholarship["percent"]
                flat = scholarship["flat"]

                # calculate final fee
                discounted_fee = total_fee - (total_fee * percent / 100) - flat

                results.append({
                    "college_name": college_info.get("name", "Unknown"),
                    "location": college_info.get("location", ""),
                    "course": course["course_name"],
                    "original_fee": total_fee,
                    "scholarship_percent": percent,
                    "final_fee": max(discounted_fee, 0)
                })

    # sort by best outcome (lowest final fee)
    results.sort(key=lambda x: x["final_fee"])

    return {"results": results}