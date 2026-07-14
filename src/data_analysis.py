import os
import sys

hauptordner = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if hauptordner not in sys.path:
    sys.path.append(hauptordner)


import numpy as np
from abstract_classes.data_analysis_base import AbstractDataAnalysis
from signal_processing import moving_average

class DataAnalysis(AbstractDataAnalysis):

    def load_data(self):

        self.data_array = np.genfromtxt(
            self.file_path, 
            delimiter=';', 
            names=True, 
            dtype=None, 
            encoding='utf-8'
        )
        
        # Sicherstellen, dass alle wichtigen Spaltennamen im Header existieren
        available_columns = self.data_array.dtype.names
        assert 'lat' in available_columns, "Spalte lat fehlt!"
        assert 'lon' in available_columns, "Spalte lon fehlt!"
        assert 'ele' in available_columns, "Spalte ele fehlt!"
        assert 'time' in available_columns, "Spalte time fehlt!"

    def get_dt(self) -> np.ndarray:
        """Berechnet die vergangenen Sekunden von Punkt zu Punkt."""
        # Wandelt in String um, schneidet das 'Z' ab und parst erst dann zeitzonenfrei
        time_strings = np.char.rstrip(self.data_array['time'].astype(str), 'Z')
        zeiten = time_strings.astype('datetime64[s]').astype(np.int64)
        
        dt = np.diff(zeiten)
        return np.insert(dt, 0, 1.0).astype(float)

    def get_distances(self) -> np.ndarray:
        """Haversine-Formel"""
        # Koordinaten in Radianten umrechnen
        lats = np.radians(self.data_array['lat'])
        lons = np.radians(self.data_array['lon'])
        
        # Vorherige und aktuelle Punkte voneinander trennen
        lat1, lat2 = lats[:-1], lats[1:]
        lon1, lon2 = lons[:-1], lons[1:]
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        
        # Distanz berechnen und für den ersten Punkt eine 0.0 vorne anfügen
        strecken = 6371000 * c
        return np.insert(strecken, 0, 0.0)

    def get_speeds(self) -> np.ndarray:
        """v = ds / dt (ohne Warnungen bei dt == 0)"""
        ds = self.distances
        dt = self.dt
        return np.divide(ds, dt, out=np.zeros_like(ds), where=dt > 0)

    def get_accelerations(self, speeds_input: np.ndarray) -> np.ndarray:
        """a = dv / dt (ohne Warnungen bei dt == 0)"""
        v = speeds_input
        dt = self.dt
        dv = np.diff(v)
        dv_vollstaendig = np.insert(dv, 0, 0.0)
        return np.divide(dv_vollstaendig, dt, out=np.zeros_like(dv_vollstaendig), where=dt > 0)

    def get_slopes(self) -> np.ndarray:
        """Steigung = d_ele / ds (ohne Warnungen bei ds == 0)"""
        ele = self.data_array['ele']
        ds = self.distances
        d_ele = np.diff(ele)
        d_ele_vollstaendig = np.insert(d_ele, 0, 0.0)
        return np.divide(d_ele_vollstaendig, ds, out=np.zeros_like(d_ele_vollstaendig), where=ds > 0)

    # --- KRÄFTE (PHYSIK-FORMELN) ---

    def get_force_gravity(self) -> np.ndarray:
        """F_gravity = m * g * slope"""
        return self.TOTAL_MASS * 9.81 * self.slopes

    def get_force_drag(self) -> np.ndarray:
        """F_drag = 0.5 * rho * cwA * v²"""
        return 0.5 * self.RHO_AIR * self.CW_A * (self.speeds ** 2)

    def get_force_acceleration(self) -> np.ndarray:
        """F_acceleration = m * a"""
        return self.TOTAL_MASS * self.accelerations

    # --- ELEKTROTECHNIK ---

    def get_torque(self) -> np.ndarray:
        """Drehmoment: T = F_total * r (Begrenzt auf minimal 0.0)"""
        torque = self.forces_total * self.WHEEL_RADIUS_M
        
        # np.clip schneidet Werte ab: Alles unter 0.0 wird zu 0.0
        return np.clip(torque, 0.0, None)

    def get_motor_current(self) -> np.ndarray:
        """Motorstrom: I = T / Km"""
        return self.torque / self.KM_MOTOR

    # --- DER MANAGER ---

    def run_analysis(self):
        """Führt die gesamte Berechnung aus und speichert die Ergebnisse als Attribute."""
        # 1. Daten über NumPy einlesen
        self.load_data()
        
        # 2. Kinematik berechnen
        self.dt = self.get_dt()
        self.distances = self.get_distances()
        
        # Rohwerte berechnen
        raw_speeds = self.get_speeds()
        raw_accelerations = self.get_accelerations(raw_speeds)
        raw_slopes = self.get_slopes()
        
        # Glätten mit der importierten Funktion
        self.speeds = moving_average(raw_speeds, window_size=15)
        self.accelerations = moving_average(raw_accelerations, window_size=15)
        self.slopes = moving_average(raw_slopes, window_size=15)
        
        # 3. Kräfte berechnen
        self.F_gravity = self.get_force_gravity()
        self.F_drag = self.get_force_drag()
        self.F_acceleration = self.get_force_acceleration()
        
        # Gesamtkraft berechnen
        self.forces_total = self.F_gravity + self.F_drag + self.F_acceleration
        
        # 4. Elektrotechnik berechnen
        self.torque = self.get_torque()
        self.I_motor = self.get_motor_current()





if __name__ == "__main__":
    folder = os.path.dirname(__file__)
    csv_pfad = os.path.abspath(os.path.join(folder, '..', 'final_project_input_data.csv'))
    
    analyzer = DataAnalysis(csv_pfad)
    
    print("--- Versuche Daten zu laden ---")
    analyzer.load_data()
    
    print("--- Inhalt von self.data_array (erste 5 Zeilen): ---")
    print(analyzer.data_array[:5])

    print("--- volle Analyse ---")
    full_analysis = analyzer.run_analysis()

    print("\n--- ERGEBNISSE (Erste 5 Zeitschritte) ---")
    print(f"{'Zeitdifferenz (dt):':<25} {analyzer.dt[:5]}")
    print(f"{'Distanzen (ds in m):':<25} {analyzer.distances[:5]}")
    print(f"{'Geschw. (v in m/s):':<25} {analyzer.speeds[:5]}")
    print(f"{'Beschleunigung (a):':<25} {analyzer.accelerations[:5]}")
    print(f"{'Steigung (slope):':<25} {analyzer.slopes[:5]}")
    
    print("\n--- PHYSTK & MOTOR (Erste 5 Zeitschritte) ---")
    print(f"{'Hangabtrieb (F_grav):':<25} {analyzer.F_gravity[:5]}")
    print(f"{'Luftwiderstand (F_drag):':<25} {analyzer.F_drag[:5]}")
    print(f"{'Gesamtkraft (F_total):':<25} {analyzer.forces_total[:5]}")
    print(f"{'Drehmoment (T in Nm):':<25} {analyzer.torque[:5]}")
    print(f"{'Motorstrom (I in A):':<25} {analyzer.I_motor[:5]}")