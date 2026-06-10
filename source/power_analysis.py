import numpy as np
import pandas as pd


def power_curve_analysis(power_data, time_resolution_sec=1):
    """Calculate power duration curve from raw power data.

    Args:
        power_data: Raw power values in Watts (pd.Series or np.ndarray).
        time_resolution_sec: Time interval per row in seconds (default: 1).

    Returns:
        DataFrame with 'Zeit_Sekunden' and 'Leistung_Watt' columns.
    """
    # Convert to numeric array, replace NaNs with 0
    power_array = np.nan_to_num(np.asarray(power_data, dtype=float))
    n_samples = len(power_array)

    if n_samples == 0:
        raise ValueError("Provided power data array is empty.")

    max_powers = []
    durations_sec = []

    # Calculate rolling mean for all possible window sizes
    # For each duration, find the maximum rolling average value
    for window_size in range(1, n_samples + 1):
        duration = window_size * time_resolution_sec

        # Calculate rolling mean
        rolling_mean = (
            pd.Series(power_array).rolling(window=window_size).mean()
        )
        max_power = rolling_mean.max()

        max_powers.append(max_power)
        durations_sec.append(duration)

        # Build result DataFrame
        power_curve_df = pd.DataFrame(
            {"Zeit_Sekunden": durations_sec, "Leistung_Watt": max_powers}
        )
    return power_curve_df

    


