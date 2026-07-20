from src.data_analysis import DataAnalysis
from src.battery_lipo import LiPoBattery
from src.battery_nmc import NMCBattery

import numpy as np
import matplotlib.pyplot as plt

import logging

logging.basicConfig(
    level=logging.INFO,
    filename='logging.log',  
    filemode='a',               
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
logger.info("main gestartet. Initialisiere Datenanalyse und Batterie-Simulation...")

analyzer = DataAnalysis("final_project_input_data.csv")

analyzer.run_analysis()

cumulative_distance = np.cumsum(analyzer.distances) / 1000

fig, ax = plt.subplots(figsize=(10, 5))

# Höhenprofil zeichnen
logging.info("Erzeuge Diagramm 1: Höhenprofil")
ax.plot(cumulative_distance, analyzer.data_array['ele'], label='Höhenprofil', color='#1f77b4', linewidth=1.5)

ax.set_xlabel('Distanz / km')
ax.set_ylabel('Höhe / m')
ax.set_title('Höhenprofil der Fahrt')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.6)
plt.xticks(np.arange(0, 100, 5))
plt.yticks(np.arange(500, 900, 50))


# Zeit-Achse in Minuten umrechnen (für eine bessere Lesbarkeit im Plot)
time_minutes = np.cumsum(analyzer.get_dt()) / 60

# 2. Zwei Diagramme untereinander erstellen (2 Zeilen, 1 Spalte)
logging.info("Erzeuge Diagramm 2: Geschwindigkeit und Motorleistung über die Zeit")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
ax2.set_xticks(np.arange(0, 301, 20))

# Geschwindigkeit über die Zeit
# (Die gefilterten Geschwindigkeiten aus deiner Analyse, umgerechnet in km/h (* 3.6))
speeds_kmh = analyzer.speeds * 3.6
ax1.plot(time_minutes, speeds_kmh, label='Geschwindigkeit', color='forestgreen', linewidth=1.5)
ax1.set_ylabel('v / (km/h)')
ax1.set_title('Geschwindigkeitsverlauf über die Zeit')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend()
# FIX: Dynamische Achse für die reale Höchstgeschwindigkeit
max_speed = np.max(speeds_kmh)
ax1.set_ylim(0, max_speed * 1.1)
ax1.set_yticks(np.arange(0, max_speed * 1.1, 5 if max_speed < 40 else 10))

#  Motorleistung über die Zeit
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
# FIX: Dynamische Achse für die reale Höchstleistung
max_power = np.max(power_watt)
ax2.set_ylim(0, max_power * 1.1)
ax2.set_yticks(np.arange(0, max_power * 1.1, 250 if max_power < 2000 else 500))

# Layout anpassen, damit sich die Achsenbeschriftungen nicht überschneiden
plt.tight_layout()



# 1. Benötigte Ladung aus den analysierten Daten ermitteln
dt_s = analyzer.dt             # Zeitdifferenzen in Sekunden
strom_a = analyzer.I_motor     # Berechneter Motorstrom in Ampere

# Ladung Q (As) = Summe über alle Zeitschritte (Strom * Zeitdifferenz)
gesamt_ladung_as = np.sum(strom_a * dt_s)
gesamt_ladung_ah = gesamt_ladung_as / 3600.0  # Umrechnung in Amperestunden (Ah)

# Dimensionierung: Wir wollen, dass die Batterie am Ende noch 10 % Restladung (SoC = 10%) hat
KAPAZITAET_AH = gesamt_ladung_ah / 0.9
PARALLEL_CELLS = 1

# Batterien für die Simulation instanziieren
lipo = LiPoBattery(capacity_nom_Ah=KAPAZITAET_AH, parallel_cells=PARALLEL_CELLS, initial_soc=1.0)
nmc = NMCBattery(capacity_nom_Ah=KAPAZITAET_AH, parallel_cells=PARALLEL_CELLS, initial_soc=1.0)

# Listen zum Aufzeichnen des Ladezustands (State of Charge in %)
soc_lipo_verlauf = []
soc_nmc_verlauf = []

# Simulationsschleife über die gesamte Fahrt
for i in range(len(dt_s)):
    # Aktuellen SoC sichern (in Prozent)
    soc_lipo_verlauf.append(lipo.get_soc() * 100.0)
    soc_nmc_verlauf.append(nmc.get_soc() * 100.0)
    
    # Strom über die Zeitdauer auf die Batterie anwenden (aktualisiert SoC intern)
    lipo.apply_current(current=strom_a[i], duration=dt_s[i])
    nmc.apply_current(current=strom_a[i], duration=dt_s[i])



fig3, (ax3_lipo, ax3_nmc) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
ax3_nmc.set_xticks(np.arange(0, 301, 20))

# Subplot 1: LiPo Ladezustand
ax3_lipo.plot(time_minutes, soc_lipo_verlauf, label='LiPo Ladezustand (SoC)', color='#1f77b4', linewidth=2)
ax3_lipo.set_ylabel('LiPo SoC / %')
ax3_lipo.set_title('Ladezustand (SoC) über die Fahrzeit')
ax3_lipo.set_ylim(-5, 105)
ax3_lipo.grid(True, linestyle='--', alpha=0.6)
ax3_lipo.legend(loc='upper right')

# Subplot 2: NMC Ladezustand
ax3_nmc.plot(time_minutes, soc_nmc_verlauf, label='NMC Ladezustand (SoC)', color='#ff7f0e', linewidth=2, linestyle='--')
ax3_nmc.set_xlabel('t / min')
ax3_nmc.set_ylabel('NMC SoC / %')
ax3_nmc.set_ylim(-5, 105)
ax3_nmc.grid(True, linestyle='--', alpha=0.6)
ax3_nmc.legend(loc='upper right')
logging.info("Erzeuge Diagramm 3: Ladezustand (SoC) der Batterien über die Zeit")

plt.tight_layout()



#  WEITERE KENNGRÖSSEN BERECHNEN

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
logging.info("Berechnete Kennzahlen und Ausgabe: Durchschnittsgeschwindigkeit, Gesamtdistanz, Gesamtzeit, Maximalleistung, Höhenmeter Anstieg/Abstieg, berechneter Verbrauch")
# Saubere, untereinander ausgerichtete Ausgabe
print(f"{'Zurückgelegte Strecke:':<29} {total_dist:.2f} km")
print(f"{'Benötigte Zeit:':<29} {total_time:.1f} min")
print(f"{'Durchschnittsgeschwindigkeit:':<29} {v_avg:.1f} km/h")
print(f"{'Maximalleistung Motor:':<29} {max_power:.0f} W")
print(f"{'Höhenmeter (Anstieg):':<29} {hm_up:.0f} hm")
print(f"{'Höhenmeter (Abstieg):':<29} {hm_down:.0f} hm")

print("-" * 40)
print(f"{'Berechneter Verbrauch:':<29} {gesamt_ladung_ah:.2f} Ah")
print(f"{'Ausgelegte Kapazität (10% SoC):':<29} {KAPAZITAET_AH:.2f} Ah")
print("="*40 + "\n")


# Erweiterung: Interaktive Karte mit Folium und Reverse Geocoding

lats = analyzer.data_array['lat']
lons = analyzer.data_array['lon']
eles = analyzer.data_array['ele']


# HTML KARTE MIT FOLIUM ERZEUGEN falls folium installiert ist
try:
    import folium
    import branca.colormap as cm
    
    logging.info("Erzeuge interaktive Karte mit farbigem Höhenprofil...")
    
    # Karte auf den Mittelpunkt der Fahrt zentrieren
    map_center = [np.mean(lats), np.mean(lons)]
    m = folium.Map(location=map_center, zoom_start=13, tiles='OpenStreetMap')
    
    # Kontinuierliche Farbskala (Colormap) basierend auf Höhenwerten erzeugen
    cmap = cm.linear.viridis.scale(int(np.min(eles)), int(np.max(eles)))
    cmap.caption = 'Höhe über dem Meeresspiegel / m'
    
    # Koordinaten als Paare vorbereiten
    coordinates = list(zip(lats, lons))
    
    # Die Fahrtstrecke als farbcodierte Linie (ColorLine) zeichnen
    folium.ColorLine(
        positions=coordinates,
        colors=eles,          # Höhenmeter steuern die Farbe
        colormap=cmap,        # Die Farbskala
        weight=5,
        opacity=0.9
    ).add_to(m)
    
    # 4. Die schwebende Höhen-Legende zur HTML-Karte hinzufügen
    cmap.add_to(m)
    
    # 5. Start & Ziel Marker setzen
    folium.Marker(
        location=coordinates[0], 
        popup="<b>Startpunkt</b>", 
        icon=folium.Icon(color='green', icon='play')
    ).add_to(m)
    
    folium.Marker(
        location=coordinates[-1], 
        popup="<b>Zielpunkt</b>", 
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(m)
    
    # HTML-Datei speichern
    karten_pfad = 'strecke_interaktiv.html'
    m.save(karten_pfad)
    print(f"-> Interaktive HTML-Karte unter '{karten_pfad}' gespeichert!")

except Exception as e:
    logging.warning("Folium-Karte mit Höhenskala konnte nicht erstellt werden: %s", e)

# Alle Diagramme ausgeben
plt.show()