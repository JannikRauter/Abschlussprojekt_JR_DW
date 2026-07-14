import logging
import math

import numpy as np

from src.battery_pack import BatteryPack


logger = logging.getLogger(__name__)


class LiPoBattery(BatteryPack):
    """ Modell eines LiPo-Akkupacks mit 10 seriellen Zellen. """

    SERIES_CELLS: int = 10
    CELL_RESISTANCE_OHM: float = 0.008

    SOC_POINTS: tuple[float, ...] = (
        0.00,
        0.04,
        0.09,
        0.13,
        0.17,
        0.21,
        0.26,
        0.30,
        0.40,
        0.52,
        0.64,
        0.76,
        0.88,
        1.00,
    )

    OCV_POINTS_V: tuple[float, ...] = (
        32.00,
        35.87,
        36.85,
        37.56,
        37.87,
        38.28,
        38.81,
        39.05,
        39.55,
        40.27,
        40.70,
        41.16,
        41.65,
        42.00,
    )

    def __init__(
        self,
        capacity_nom_Ah: float,
        parallel_cells: int,
        initial_soc: float = 1.0,
    ) -> None:
        """ Initialisiert das LiPo-Akkupack. """
        assert math.isfinite(capacity_nom_Ah), (
            "Die Batteriekapazität muss eine endliche Zahl sein."
        )
        assert capacity_nom_Ah > 0.0, (
            "Die Batteriekapazität muss größer als 0 Ah sein."
        )

        assert type(parallel_cells) is int, (
            "Die Anzahl paralleler Zellstränge muss eine Ganzzahl sein."
        )
        assert parallel_cells > 0, (
            "Die Anzahl paralleler Zellstränge muss größer als 0 sein."
        )

        assert math.isfinite(initial_soc), (
            "Der initiale SOC muss eine endliche Zahl sein."
        )
        assert 0.0 <= initial_soc <= 1.0, (
            "Der initiale SOC muss zwischen 0 und 1 liegen."
        )

        assert len(self.SOC_POINTS) == len(self.OCV_POINTS_V), (
            "SOC- und OCV-Kennlinie müssen gleich viele Werte enthalten."
        )
        assert all(
            self.SOC_POINTS[index] < self.SOC_POINTS[index + 1]
            for index in range(len(self.SOC_POINTS) - 1)
        ), "Die SOC-Stützstellen müssen streng aufsteigend sein."

        self.parallel_cells = parallel_cells

        # Bei Serienschaltung addieren sich die Widerstände.
        # Bei Parallelschaltung wird der Gesamtwiderstand kleiner.
        pack_resistance = (
            self.SERIES_CELLS
            * self.CELL_RESISTANCE_OHM
            / self.parallel_cells
        )

        assert pack_resistance > 0.0, (
            "Der berechnete Pack-Innenwiderstand muss größer als 0 sein."
        )
        assert math.isfinite(pack_resistance), (
            "Der berechnete Pack-Innenwiderstand muss endlich sein."
        )

        super().__init__(
            capacity_nom_Ah=capacity_nom_Ah,
            initial_soc=initial_soc,
            R_int=pack_resistance,
        )

        logger.info(
            "LiPoBattery initialisiert: "
            "%dS%dP, Kapazität=%.2f Ah, SOC=%.1f %%, "
            "R_Zelle=%.4f Ohm, R_Pack=%.4f Ohm",
            self.SERIES_CELLS,
            self.parallel_cells,
            capacity_nom_Ah,
            self.soc * 100.0,
            self.CELL_RESISTANCE_OHM,
            self.R_int,
        )

    def ocv(self) -> float:
        """ Berechnet die Leerlaufspannung anhand des aktuellen SOC. """
        
        assert 0.0 <= self.soc <= 1.0, (
            "Der SOC muss für die OCV-Berechnung zwischen 0 und 1 liegen."
        )

        open_circuit_voltage = float(
            np.interp(
                self.soc,
                self.SOC_POINTS,
                self.OCV_POINTS_V,
            )
        )

        assert math.isfinite(open_circuit_voltage), (
            "Die berechnete Leerlaufspannung muss endlich sein."
        )
        assert 32.0 <= open_circuit_voltage <= 42.0, (
            "Die LiPo-Leerlaufspannung liegt außerhalb "
            "des gültigen Bereichs von 32 bis 42 V."
        )

        logger.debug(
            "LiPo-OCV berechnet: SOC=%.2f %%, OCV=%.2f V",
            self.soc * 100.0,
            open_circuit_voltage,
        )

        return open_circuit_voltage