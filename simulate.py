import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def dTc_dt(Tc, t, ws, Ta, I):
    A = (- (ws ** 2) / 1600) * 0.4 - 0.1
    B = (Tc - Ta - (I ** 1.4 / 73785) * 130)
    dTc = (A * B) / 60
    return dTc

def predict_manual(ws, Ta, I, Tc0):
    dt = 1e-6
    t_total = 30 * 60
    Tc = Tc0
    t = 0
    t_values = [0]
    Tc_values = [Tc0]
    next_t = 60

    while t < t_total:
        dTc = dTc_dt(Tc, t, ws, Ta, I)
        Tc += dTc * dt
        t += dt

        if t >= next_t:
            t_values.append(t / 60)
            Tc_values.append(Tc)
            next_t += 60

    return np.array(t_values), np.array(Tc_values)

def predict_odeint(ws, Ta, I, Tc0):
    t_minutes = np.linspace(0, 30*60, 30*60+1)
    sol = odeint(dTc_dt, Tc0, t_minutes, args=(ws, Ta, I))
    return t_minutes, sol.flatten()

def plot_comparaison(ws, Ta, Tc0, intensites):
    plt.figure()
    for I in intensites:
        t1, T1 = predict_odeint(ws, Ta, I, Tc0)
        t2, T2 = predict_manual(ws, Ta, I, Tc0)
        plt.plot(t1, T1, '--', label=f'Odeint - I={I}A')
        plt.plot(t2, T2, '-', label=f'For loop - I={I}A')

    plt.title("Température du câble selon l'intensité")
    plt.xlabel("Temps (minutes)")
    plt.ylabel("Température (°C)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    ws = 5
    Ta = 25
    Tc0 = 30
    intensites = [100, 150, 200, 300]
    plot_comparaison(ws, Ta, Tc0, intensites)
