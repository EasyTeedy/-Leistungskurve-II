import numpy as np
import pandas as pd


def power_curve_analysis(power_data, time_resolution_sec=1):
    """Power-Dauer-Kurve aus Rohdaten berechnen.

    Args:
        power_data: Leistungswerte in Watt (pd.Series oder np.ndarray).
        time_resolution_sec: Zeitintervall pro Zeile in Sekunden (Standard: 1).

    Returns:
        DataFrame mit 'Zeit_Sekunden' und 'Leistung_Watt' Spalten.
    """
    # In numerisches Array konvertieren, NaNs durch 0 ersetzen
    power_array = np.nan_to_num(np.asarray(power_data, dtype=float))
    n_samples = len(power_array)

    if n_samples == 0:
        raise ValueError("Provided power data array is empty.")

    max_powers = []
    durations_sec = []

    # Rolling-Mittelwert für alle möglichen Fenstergrößen berechnen
    # Für jede Dauer den maximalen Rolling-Average ermitteln
    for window_size in range(1, n_samples + 1):
        duration = window_size * time_resolution_sec

        # Rolling-Mittelwert berechnen
        rolling_mean = (
            pd.Series(power_array).rolling(window=window_size).mean()
        )
        max_power = rolling_mean.max()

        max_powers.append(max_power)
        durations_sec.append(duration)

        # Ergebnis-DataFrame aufbauen
        power_curve_df = pd.DataFrame(
            {"Zeit_Sekunden": durations_sec, "Leistung_Watt": max_powers}
        )
    return power_curve_df

    


