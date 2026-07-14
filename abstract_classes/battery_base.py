from abc import ABC, abstractmethod


class BatteryBase(ABC):
    @abstractmethod
    def __init__(self, capacity_nom_Ah: float, initial_soc: float = 1.0):
        self.C_nom = capacity_nom_Ah * 3600.0  # Kapazität in As
        self.soc = initial_soc

    @abstractmethod
    def apply_current(self, current: float, duration: float) -> None:
        pass

    @abstractmethod
    def voltage(self, current: float = 0.0) -> float:
        pass
