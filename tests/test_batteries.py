import logging

import pytest

from src.battery_lipo import LiPoBattery
from src.battery_nmc import NMCBattery


@pytest.mark.parametrize(
    "battery_class, cell_resistance",
    [
        (LiPoBattery, 0.008),
        (NMCBattery, 0.007),
    ],
)
def test_battery_can_be_created(battery_class, cell_resistance) -> None:
    """ Prüft, ob ein Akku korrekt erstellt werden kann. """
    battery = battery_class(
        capacity_nom_Ah=10.0,
        parallel_cells=4,
        initial_soc=1.0,
    )

    assert battery.get_soc() == pytest.approx(1.0)
    assert battery.parallel_cells == 4

    expected_resistance = 10 * cell_resistance / 4
    assert battery.R_int == pytest.approx(expected_resistance)


@pytest.mark.parametrize("battery_class", [LiPoBattery, NMCBattery])
def test_discharge_reduces_soc(battery_class) -> None:
    """ Prüft, ob Entladen den SOC verringert. """
    battery = battery_class(
        capacity_nom_Ah=10.0,
        parallel_cells=4,
        initial_soc=1.0,
    )

    battery.apply_current(current=5.0, duration=3600.0)

    assert battery.get_soc() == pytest.approx(0.5)


@pytest.mark.parametrize("battery_class", [LiPoBattery, NMCBattery])
def test_charge_increases_soc(battery_class) -> None:
    """ Prüft, ob Laden den SOC erhöht. """
    battery = battery_class(
        capacity_nom_Ah=10.0,
        parallel_cells=4,
        initial_soc=0.5,
    )

    battery.apply_current(current=-2.5, duration=3600.0)

    assert battery.get_soc() == pytest.approx(0.75)


@pytest.mark.parametrize("battery_class", [LiPoBattery, NMCBattery])
def test_soc_is_limited_to_zero(battery_class, caplog) -> None:
    """ Prüft, ob der SOC nicht unter 0 fallen kann. """
    battery = battery_class(
        capacity_nom_Ah=10.0,
        parallel_cells=4,
        initial_soc=0.1,
    )

    with caplog.at_level(logging.WARNING):
        battery.apply_current(current=100.0, duration=3600.0)

    assert battery.get_soc() == pytest.approx(0.0)
    assert battery.is_empty()
    assert "SOC würde unter 0" in caplog.text


@pytest.mark.parametrize("battery_class", [LiPoBattery, NMCBattery])
def test_soc_is_limited_to_one(battery_class, caplog) -> None:
    """ Prüft, ob der SOC nicht über 100 Prozent steigen kann. """
    battery = battery_class(
        capacity_nom_Ah=10.0,
        parallel_cells=4,
        initial_soc=0.9,
    )

    with caplog.at_level(logging.WARNING):
        battery.apply_current(current=-100.0, duration=3600.0)

    assert battery.get_soc() == pytest.approx(1.0)
    assert battery.is_full()
    assert "SOC würde über 100" in caplog.text


@pytest.mark.parametrize("battery_class", [LiPoBattery, NMCBattery])
def test_ocv_at_empty_and_full_soc(battery_class) -> None:
    """ Prüft die OCV-Grenzwerte bei leerem und vollem Akku. """
    empty_battery = battery_class(
        capacity_nom_Ah=10.0,
        parallel_cells=4,
        initial_soc=0.0,
    )

    full_battery = battery_class(
        capacity_nom_Ah=10.0,
        parallel_cells=4,
        initial_soc=1.0,
    )

    assert empty_battery.ocv() == pytest.approx(32.0)
    assert full_battery.ocv() == pytest.approx(42.0)


@pytest.mark.parametrize("battery_class", [LiPoBattery, NMCBattery])
def test_voltage_drops_under_discharge_current(battery_class) -> None:
    """ Prüft, ob die Klemmenspannung beim Entladen sinkt. """
    battery = battery_class(
        capacity_nom_Ah=10.0,
        parallel_cells=4,
        initial_soc=1.0,
    )

    open_circuit_voltage = battery.voltage(current=0.0)
    loaded_voltage = battery.voltage(current=10.0)

    assert loaded_voltage < open_circuit_voltage


@pytest.mark.parametrize("battery_class", [LiPoBattery, NMCBattery])
def test_voltage_increases_under_charge_current(battery_class) -> None:
    """ Prüft, ob die Klemmenspannung beim Laden steigt. """
    battery = battery_class(
        capacity_nom_Ah=10.0,
        parallel_cells=4,
        initial_soc=0.5,
    )

    open_circuit_voltage = battery.voltage(current=0.0)
    charge_voltage = battery.voltage(current=-10.0)

    assert charge_voltage > open_circuit_voltage


@pytest.mark.parametrize("battery_class", [LiPoBattery, NMCBattery])
def test_invalid_initial_soc_raises_assertion(battery_class) -> None:
    """ Prüft, ob ein ungültiger Start-SOC abgefangen wird. """
    with pytest.raises(AssertionError):
        battery_class(
            capacity_nom_Ah=10.0,
            parallel_cells=4,
            initial_soc=1.5,
        )


@pytest.mark.parametrize("battery_class", [LiPoBattery, NMCBattery])
def test_invalid_parallel_cells_raises_assertion(battery_class) -> None:
    """ Prüft, ob ungültige Parallelzellen abgefangen werden. """
    with pytest.raises(AssertionError):
        battery_class(
            capacity_nom_Ah=10.0,
            parallel_cells=0,
            initial_soc=1.0,
        )


@pytest.mark.parametrize("battery_class", [LiPoBattery, NMCBattery])
def test_negative_duration_raises_assertion(battery_class) -> None:
    """ Prüft, ob negative Zeitdauern abgefangen werden. """
    battery = battery_class(
        capacity_nom_Ah=10.0,
        parallel_cells=4,
        initial_soc=1.0,
    )

    with pytest.raises(AssertionError):
        battery.apply_current(current=5.0, duration=-1.0)