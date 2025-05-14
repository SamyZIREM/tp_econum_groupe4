import numpy as np  # Pour créer un vecteur de temps (np.linspace)
from scipy.integrate import odeint  # Pour résoudre l'équation différentielle

# Cette fonction représente l'équation différentielle donnée par le prof
# Elle modélise l'évolution de la température du câble Tc
def dTc_dt(Tc, t, ws, Ta, I):
    A = (- (ws ** 2) / 1600) * 0.4 - 0.1
    B = (Tc - Ta - (I ** 1.4 / 73785) * 130)
    dTc = (A * B) / 60
    return dTc

def predict_temperature(ws, Ta, I, Tc0):
    t_minutes = np.linspace(0, 30*60, 30*60+1)
    sol = odeint(dTc_dt, Tc0, t_minutes, args=(ws, Ta, I))
    return sol.flatten().tolist()

