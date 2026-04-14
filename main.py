from fastapi import FastAPI
from pydantic import BaseModel
from engine import calculate_scholarship_v2
from data import RULES, COLLEGES
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

            results.append({
                "college_id": college_id,
                "college_name": college_info.get("name", "Unknown"),
                "location": college_info.get("location", ""),
                "percent": scholarship["percent"],
                "flat": scholarship["flat"]
            })

    results.sort(key=lambda x: (x["percent"], x["flat"]), reverse=True)

    return {"results": results}