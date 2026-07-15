from abc import abstractmethod
import logging

from abstract_classes.battery_base import BatteryBase


logger = logging.getLogger(__name__)


class BatteryPack(BatteryBase):
    """
    Enthält alle Funktionen, die für LiPo und NMC identisch sind.
    """

    def __init__(
        self,
        capacity_nom_Ah: float,
        initial_soc: float,
        R_int: float,
    ):
        assert capacity_nom_Ah > 0, "Die Batteriekapazität muss größer als 0 sein."
        assert 0.0 <= initial_soc <= 1.0, "Der initiale SOC muss zwischen 0 und 1 liegen."
        assert R_int >= 0, "Der Innenwiderstand darf nicht negativ sein."

        super().__init__(capacity_nom_Ah, initial_soc)
        self.R_int = R_int

        logger.info(
            "BatteryPack initialisiert: capacity=%.2f Ah, SOC=%.1f %%, R_int=%.4f Ohm",
            capacity_nom_Ah,
            self.soc * 100,
            self.R_int,
        )

    def apply_current(self, current: float, duration: float) -> None:
        """
        Aktualisiert Ladezustand (SOC) anhand des Stroms.

        current > 0  -> Entladen
        current < 0  -> Laden
        duration in Sekunden
        """

        assert duration >= 0, "Die Dauer darf nicht negativ sein."

        old_soc = self.soc

        delta_soc = current * duration / self.C_nom
        new_soc = self.soc - delta_soc

        if new_soc < 0.0:
            logger.warning(
                "SOC würde unter 0 %% fallen: %.2f %%. SOC wird auf 0 %% begrenzt.",
                new_soc * 100,
            )
            new_soc = 0.0

        elif new_soc > 1.0:
            logger.warning(
                "SOC würde über 100 %% steigen: %.2f %%. SOC wird auf 100 %% begrenzt.",
                new_soc * 100,
            )
            new_soc = 1.0

        assert 0.0 <= new_soc <= 1.0, "SOC außerhalb des gültigen Bereichs."

        self.soc = new_soc

        logger.debug(
            "SOC aktualisiert: %.2f %% -> %.2f %% bei I=%.2f A, t=%.2f s",
            old_soc * 100,
            self.soc * 100,
            current,
            duration,
        )

    def voltage(self, current: float = 0.0) -> float:
        """
        Klemmenspannung unter Last.
        """

        ocv = self.ocv()
        voltage = ocv - current * self.R_int

        logger.debug(
            "Spannung berechnet: OCV=%.2f V, I=%.2f A, R=%.4f Ohm, U=%.2f V",
            ocv,
            current,
            self.R_int,
            voltage,
        )

        return voltage

    @abstractmethod
    def ocv(self) -> float:
        """
        Open-Circuit-Voltage.
        Wird von LiPo bzw. NMC implementiert.
        """
        pass

    def get_soc(self) -> float:
        return self.soc

    def is_empty(self) -> bool:
        return self.soc <= 0.0

    def is_full(self) -> bool:
        return self.soc >= 1.0

    def __str__(self):
        return (
            f"{self.__class__.__name__}: "
            f"SOC={self.soc * 100:.1f}% | "
            f"Spannung={self.voltage():.2f} V"
        )