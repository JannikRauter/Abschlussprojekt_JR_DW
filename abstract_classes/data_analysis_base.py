from abc import ABC, abstractmethod
import pandas as pd

class AbstractDataAnalysis(ABC):
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        
        # Konstanten aus den Vorlesungsfolien
        self.MASS_DRIVER = 70.0      # kg
        self.MASS_BIKE = 10.0        # kg
        self.TOTAL_MASS = self.MASS_DRIVER + self.MASS_BIKE
        self.CW_A = 0.5625           # m² (cw * A)
        self.WHEEL_DIAMETER_INCH = 27.0
        self.WHEEL_RADIUS_M = (self.WHEEL_DIAMETER_INCH * 0.0254) / 2.0  # Umrechnung in Meter
        self.RHO_AIR = 1.225         # kg/m³ (Standard-Luftdichte)
        self.KM_MOTOR = 1.5          # Nm/A (Motorkonstante)

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Lädt die CSV-Datei und validiert die Spalten (lat, lon, ele, time)."""
        pass

    @abstractmethod
    def process_trajectory(self) -> pd.DataFrame:
        """Berechnet Zeitdifferenz, Distanz (Haversine), Geschwindigkeit und Steigung."""
        pass

    @abstractmethod
    def calculate_physics_and_current(self) -> pd.DataFrame:
        """
        Berechnet die Kräftebilanz, die mechanische Leistung, 
        das Rad-Drehmoment T und den resultierenden Motorstrom I.
        """
        pass