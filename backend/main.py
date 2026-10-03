
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai


# Load environment variables from backend/.env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Create FastAPI application
app = FastAPI(
    title="Fitness Forge API",
    version="1.2.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Fitness Forge Backend is running"
    }


# Health check endpoint
@app.get("/health")
def health():
    return {
        "status": "online"
    }


# Fitness assessment endpoint
@app.post("/assessment")
def assessment(data: dict):
    goal = data.get("goal", "General Fitness")
    level = data.get("level", "Beginner")

    # Select workout based on fitness goal
    if goal == "Muscle Gain":
        workout = [
            "Bodyweight Squats",
            "Push Ups",
            "Lunges",
            "Glute Bridges"
        ]
        workout_type = "Strength Training"

    elif goal == "Weight Loss":
        workout = [
            "Jumping Jacks",
            "Bodyweight Squats",
            "Mountain Climbers",
            "Walking / Jogging"
        ]
        workout_type = "Cardio + Strength"

    else:
        workout = [
            "Bodyweight Squats",
            "Push Ups",
            "Plank",
            "Stretching"
        ]
        workout_type = "General Fitness"

    # Select workout intensity and duration
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
        "workout": workout
    }


# AI chatbot endpoint
@app.post("/chat")
def chat(data: dict):
    # Validate the request
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a message."
        )

    message = message.strip()

    if len(message) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Please keep your message under 2000 characters."
        )

    # Check API key configuration
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail=(
                "GEMINI_API_KEY is missing. "
                "Check the backend/.env file."
            )
        )

    try:
        # Connect to Gemini
        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        # Instructions for the Fitness Forge assistant
        prompt = f"""
You are the friendly AI assistant for Fitness Forge.

Your responsibilities:
- Answer general questions in simple, helpful language.
- Help with beginner fitness, exercise, nutrition, and healthy habits.
- Explain technical concepts in beginner-friendly language.
- Keep answers clear and reasonably short.
- Do not diagnose medical conditions or prescribe treatments.
- For serious health concerns, recommend a qualified healthcare professional.
- Do not claim to be a doctor or a human.
- Never request passwords or API keys.

User message:
{message}
"""

        # Generate AI response
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        answer = response.text

        if not answer or not answer.strip():
            raise HTTPException(
                status_code=502,
                detail=(
                    "Gemini returned an empty response. "
                    "Please try again."
                )
            )

        # Return response to frontend
        return {
            "reply": answer.strip()
        }

    except HTTPException:
        raise

    except Exception as e:
        # Log the technical error in the backend terminal
        print("CHATBOT ERROR:", repr(e))

        # Return a useful error message
        raise HTTPException(
            status_code=502,
            detail=(
                f"Chatbot error: {type(e).__name__}: {str(e)}"
            )
        )
