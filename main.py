from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Tuple
from selector import select_top_volunteers

# ---------- Define Input Schema ----------

class VolunteerInfo(BaseModel):
    location: Tuple[float, float]
    audit_score: int

class VolunteerRequest(BaseModel):
    volunteer_dict: Dict[str, VolunteerInfo]
    ward_location: Tuple[float, float]
    required_volunteers: int = 2

# ---------- FastAPI App ----------

app = FastAPI()

@app.post("/select-volunteers")
def select_volunteers(payload: VolunteerRequest):
    # Convert to simple dict structure for processing
    volunteer_dict = {
        vid: {"location": v.location, "audit_score": v.audit_score}
        for vid, v in payload.volunteer_dict.items()
    }

    selected_ids = select_top_volunteers(
        volunteer_dict,
        payload.ward_location,
        payload.required_volunteers
    )
    return {"selected_ids": selected_ids}
