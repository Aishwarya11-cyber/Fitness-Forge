from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fitness Forge API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Fitness Forge Backend is running"}

@app.get("/health")
def health():
    return {"status": "online"}

@app.post("/assessment")
def assessment(data: dict):
    goal = data.get("goal", "General Fitness")
    level = data.get("level", "Beginner")

    if goal == "Muscle Gain":
        workout = [
            "Bodyweight Squats",
            "Push Ups",
            "Lunges",
            "Glute Bridges",
        ]
        workout_type = "Strength Training"
    elif goal == "Weight Loss":
        workout = [
            "Jumping Jacks",
            "Bodyweight Squats",
            "Mountain Climbers",
            "Walking / Jogging",
        ]
        workout_type = "Cardio + Strength"
    else:
        workout = [
            "Bodyweight Squats",
            "Push Ups",
            "Plank",
            "Stretching",
        ]
        workout_type = "General Fitness"

    if level == "Beginner":
        intensity = "Low to Moderate"
        duration = "25 minutes"
        score = 65
    elif level == "Intermediate":
        intensity = "Moderate"
        duration = "35 minutes"
        score = 75
    else:
        intensity = "High"
        duration = "45 minutes"
        score = 85

    return {
        "goal": goal,
        "level": level,
        "fitness_score": score,
        "workout_type": workout_type,
        "intensity": intensity,
        "duration": duration,
        "workout": workout,
    }
