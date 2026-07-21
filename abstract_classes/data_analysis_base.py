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
        self.CW_A = 0.5625           # m^2 * cw * A
        self.WHEEL_DIAMETER_INCH = 27.0
        self.WHEEL_RADIUS_M = (self.WHEEL_DIAMETER_INCH * 0.0254) / 2.0
        self.RHO_AIR = 1.225         # kg/m^3
        self.KM_MOTOR = 1.5          # Nm/A
        self.C_R = 0.007              # Rollwiderstandsbeiwert

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Lädt die CSV-Datei."""
        pass

    # --- KINEMATIK ---
    
    @abstractmethod
    def get_dt(self) -> pd.Series:
        """Berechnet die Zeitdifferenz zwischen den Punkten."""
        pass

    @abstractmethod
    def get_distances(self) -> pd.Series:
        """Berechnet die Distanzen zwischen den Punkten."""
        pass

    @abstractmethod
    def get_speeds(self) -> pd.Series:
        """Berechnet die Geschwindigkeiten (ds / dt)."""
        pass

    @abstractmethod
    def get_accelerations(self) -> pd.Series:
        """Berechnet die Beschleunigungen (dv / dt)."""
        pass

    @abstractmethod
    def get_slopes(self) -> pd.Series:
        """Berechnet die Steigung der Strecke."""
        pass

    # --- KRÄFTE ---

    @abstractmethod
    def get_force_gravity(self) -> pd.Series:
        """Berechnet den Steigungswiderstand."""
        pass

    @abstractmethod
    def get_force_drag(self) -> pd.Series:
        """Berechnet den Luftwiderstand."""
        pass

    @abstractmethod
    def get_force_acceleration(self) -> pd.Series:
        """Berechnet den Beschleunigungswiderstand."""
        pass

    # --- ELEKTROTECHNIK ---

    @abstractmethod
    def get_torque(self) -> pd.Series:
        """Berechnet das Drehmoment am Rad."""
        pass

    @abstractmethod
    def get_motor_current(self) -> pd.Series:
        """Berechnet den resultierenden Motorstrom."""
        pass

   # --- KOMPLETTE ANALYSE ---
    
    @abstractmethod
    def run_analysis(self) -> pd.DataFrame:
        """Ruft alle obigen Methoden nacheinander auf und fügt sie im DataFrame zusammen."""
        pass