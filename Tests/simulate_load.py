import requests
import time

API_URL = "http://127.0.0.1:8000/predict"

def simulate_users(user_count, with_cache=False):
    print(f"\n--- Test avec {user_count} utilisateurs/minute {'(avec cache)' if with_cache else ''} ---")
    start = time.perf_counter()
    total_energy = 0
    for i in range(user_count):
        payload = {
            "Tc0": 30,
            "Ta": 25,
            "ws": 2 + (i % 3),  # changer le vent
            "I": 100 + (i % 5) * 50  # changer l’intensité
        }
        response = requests.post(API_URL, json=payload)
        data = response.json()
        total_energy += data["energy_joules"]
    duration = time.perf_counter() - start
    print(f"Temps total : {duration:.4f} s")
    print(f"Énergie totale estimée : {total_energy:.6f} J")
    print(f"CO₂ estimé total : {(total_energy / 3600000) * 50:.6e} g")

# Lancer les 4 tests :
simulate_users(10)       # 10 utilisateurs/minute
simulate_users(100)      # 100 utilisateurs/minute
simulate_users(1000)     # 1000 utilisateurs/minute sans cache
simulate_users(1000, with_cache=True)  # avec cache (même données = gain)
