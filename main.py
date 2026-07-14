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
plt.xticks(np.arange(0, 100, 5))
plt.yticks(np.arange(500, 900, 50))


# 1. Zeit-Achse in Minuten umrechnen (für eine bessere Lesbarkeit im Plot)
time_minutes = np.cumsum(analyzer.get_dt()) / 60

# 2. Zwei Diagramme untereinander erstellen (2 Zeilen, 1 Spalte)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
ax2.set_xticks(np.arange(0, 301, 20))

# --- Diagramm 1: Geschwindigkeit über die Zeit ---
# (Die gefilterten Geschwindigkeiten aus deiner Analyse, umgerechnet in km/h (* 3.6))
speeds_kmh = analyzer.speeds * 3.6
ax1.plot(time_minutes, speeds_kmh, label='Geschwindigkeit', color='forestgreen', linewidth=1.5)
ax1.set_ylabel('v / (km/h)')
ax1.set_title('Geschwindigkeitsverlauf über die Zeit')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend()
ax1.set_yticks(np.arange(0, 61, 5))

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
ax2.set_yticks(np.arange(0, 2001, 250))

# Layout anpassen, damit sich die Achsenbeschriftungen nicht überschneiden
plt.tight_layout()





# Diagramme anzeigen
plt.show()


# --- WEITERE KENNGRÖSSEN BERECHNEN ---

# 1. Maximalleistung (höchster Wert aus deinem berechneten power_watt Array)
max_power = np.max(power_watt)

# 2. Höhenmeter Anstieg und Abstieg über die Differenzen berechnen
# (Nutzt dein originales Höhen-Array aus dem Analyzer)
elevation_diffs = analyzer.get_slopes() * analyzer.get_distances()
hm_up = np.sum(elevation_diffs[elevation_diffs > 0])
hm_down = np.abs(np.sum(elevation_diffs[elevation_diffs < 0]))


# --- AUSGABE DER FAHRTKENNGRÖSSEN IM TERMINAL ---

print("\n" + "="*40)
print("       ZUSAMMENFASSUNG DER FAHRT       ")
print("="*40)

# Berechnungen der Basis-Größen
v_avg = np.mean(analyzer.speeds) * 3.6  # m/s in km/h umrechnen
total_dist = np.sum(analyzer.get_distances()) / 1000  # Meter in km
total_time = np.sum(analyzer.get_dt()) / 60  # Sekunden in Minuten

# Saubere, untereinander ausgerichtete Ausgabe
print(f"{'Zurückgelegte Strecke:':<29} {total_dist:.2f} km")
print(f"{'Benötigte Zeit:':<29} {total_time:.1f} min")
print(f"{'Durchschnittsgeschwindigkeit:':<29} {v_avg:.1f} km/h")
print(f"{'Maximalleistung Motor:':<29} {max_power:.0f} W")
print(f"{'Höhenmeter (Anstieg):':<29} {hm_up:.0f} hm")
print(f"{'Höhenmeter (Abstieg):':<29} {hm_down:.0f} hm")

print("="*40 + "\n")