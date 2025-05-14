from fastapi import FastAPI
from pydantic import BaseModel
from predict import predict_temperature
import time
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from predict import simulate_heavy_computation
import os

app = FastAPI()

class PredictionInput(BaseModel):
    ws: float
    Ta: float
    I: float
    Tc0: float

@app.post("/predict")
def predict(input_data: PredictionInput):
    start = time.perf_counter()  # plus précis que time.time()
    resultats = predict_temperature(
        input_data.ws,
        input_data.Ta,
        input_data.I,
        input_data.Tc0
    )
    duration = time.perf_counter() - start

    POWER_WATTS = 30
    energy_joules = POWER_WATTS * duration
    co2_grams = (energy_joules / 3600000) * 50

    return {
        "predictions": resultats,
        "duration_seconds": duration,
        "energy_joules": energy_joules,
        "co2_grams": co2_grams
    }

# Servir le front
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/simulate-carbon")
def simulate_carbon():
    emissions = simulate_heavy_computation()
    return {
        "co2_measured_grams": emissions
    }
