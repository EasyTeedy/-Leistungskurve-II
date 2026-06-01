import numpy as np
import pandas as pd


def get_perfect_log_time_ticks(max_time):
    # Eine Liste von "schönen" Zeitstempeln in Sekunden, die log-ähnlich wachsen
    potential_ticks = [
        1, 2, 5, 10, 20, 30,         # Sekundenbereich
        60, 120, 300, 600, 1200,     # Minutenbereich (1m, 2m, 5m, 10m, 20m)
        1800, 3600, 7200, 14400,     # Halbe Stunde, 1h, 2h, 4h
        21600, 43200                 # 6h, 12h (für Ultra-Endurance)
    ]
    
    # 1. Filtere alle Ticks heraus, die kleiner als unsere Maximalzeit sind
    ticks = [t for t in potential_ticks if t < max_time]
    
    # 2. Wenn wir zu viele Ticks haben (z.B. bei 4 Stunden Fahrt), dünnen wir sie logarithmisch aus
    if len(ticks) > 6:
        # Wir wählen via Index-Slicing gleichmäßig verteilte Indizes
        indices = np.unique(np.geomspace(1, len(ticks), num=5, dtype=int)) - 1
        ticks = [ticks[i] for i in indices]
        
    # 3. Das exakte Ende der CSV IMMER als finalen Tick hinzufügen
    ticks.append(max_time)
    
    # Duplikate entfernen und sortieren
    return np.unique(ticks).astype(int)


def power_curve_analysis(power_data, time_resolution_sec=1):
    """Calculates the power duration curve from raw power data.

    Parameters:
    -----------
    power_data : pd.Series or np.ndarray
        The raw power values in Watts.
    time_resolution_sec : int, default=1
        The time interval per row in seconds.

    Returns:
    --------
    pd.DataFrame
        DataFrame containing 'Zeit_Sekunden' and 'Leistung_Watt'.
    """
    # Convert input to a clean numeric NumPy array and replace NaNs with 0
    power_array = np.nan_to_num(np.asarray(power_data, dtype=float))
    n_samples = len(power_array)

    if n_samples == 0:
        raise ValueError("Provided power data array is empty.")

    max_powers = []
    durations_sec = []

    # Calculate rolling maximum averages for every possible duration window
    # druchschnitt von 1 Sekunde, 2 Sekunden, ..., bis zur gesamten Fahrtzeit 
    # Von diesen Mittelwert sammlung wird dann der Maxwert genommen und ist dann der representante Wert der jeweiligen Dauer
    for window_size in range(1, n_samples + 1):
        duration = window_size * time_resolution_sec

        # Efficient rolling mean calculation using pandas
        rolling_mean = (
            pd.Series(power_array).rolling(window=window_size).mean()
        )
        max_power = rolling_mean.max()

        max_powers.append(max_power)
        durations_sec.append(duration)

        # Generate the resulting DataFrame
        power_curve_df = pd.DataFrame(
            {"Zeit_Sekunden": durations_sec, "Leistung_Watt": max_powers}
        )
    return power_curve_df

    


