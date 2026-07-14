from src.data_analysis import DataAnalysis
import numpy as np
import matplotlib.pyplot as plt

analyzer = DataAnalysis("final_project_input_data.csv")

analyzer.run_analysis()

cumulative_distance = np.cumsum(analyzer.distances) / 1000

fig, ax = plt.subplots(figsize=(10, 5))

# Höhenprofil zeichnen
ax.plot(cumulative_distance, analyzer.data_array['ele'], label='Höhenprofil', color='#1f77b4', linewidth=1.5)

ax.set_xlabel('Distanz / km')
ax.set_ylabel('Höhe / m')
ax.set_title('Höhenprofil der Fahrt')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.6)

plt.show()


# 1. Zeit-Achse in Minuten umrechnen (für eine bessere Lesbarkeit im Plot)
time_minutes = np.cumsum(analyzer.get_dt()) / 60

# 2. Zwei Diagramme untereinander erstellen (2 Zeilen, 1 Spalte)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# --- Diagramm 1: Geschwindigkeit über die Zeit ---
# (Die gefilterten Geschwindigkeiten aus deiner Analyse, umgerechnet in km/h (* 3.6))
speeds_kmh = analyzer.speeds * 3.6
ax1.plot(time_minutes, speeds_kmh, label='Geschwindigkeit', color='forestgreen', linewidth=1.5)
ax1.set_ylabel('v / (km/h)')
ax1.set_title('Geschwindigkeitsverlauf über die Zeit')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend()

# --- Diagramm 2: Berechnete Motorleistung über die Zeit ---
# Drehmoment holen
torque = analyzer.get_torque()

# Winkelgeschwindigkeit der Räder berechnen (v / r)
omega = analyzer.speeds / analyzer.WHEEL_RADIUS_M

# Mechanische Motorleistung am Rad (P = T * omega)
power_watt = torque * omega
ax2.plot(time_minutes, power_watt, label='Motorleistung', color='crimson', linewidth=1.5)
ax2.set_xlabel('t / min')
ax2.set_ylabel('P / W')
ax2.set_title('Benötigte Motorleistung über die Zeit')
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend()

# Layout anpassen, damit sich die Achsenbeschriftungen nicht überschneiden
plt.tight_layout()

# Diagramme anzeigen
plt.show()