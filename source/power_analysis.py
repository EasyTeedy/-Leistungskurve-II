import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calculate_power_curve(
    power_data, time_resolution_sec=1, plot_curve=True
):
    """Calculates the power duration curve from raw power data.

    Parameters:
    -----------
    power_data : pd.Series or np.ndarray
        The raw power values in Watts.
    time_resolution_sec : int, default=1
        The time interval per row in seconds.
    plot_curve : bool, default=True
        Whether to save and display the final chart.

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

    # Plot, save, and display the chart
    if plot_curve:
        plt.figure(figsize=(15, 6))
        plt.plot(
            power_curve_df["Zeit_Sekunden"],
            power_curve_df["Leistung_Watt"],
            color="#7cb342",  # Distinct athletic green
            linewidth=2,
            label="Today",
        )

        # Soft background fill under the curve for better visual appeal
        plt.fill_between(
            power_curve_df["Zeit_Sekunden"],
            power_curve_df["Leistung_Watt"],
            color="#f5f5f5",
            alpha=0.5,
        )

        # Chart styling and labeling
        plt.title("Power Curve Analysis", fontsize=14, pad=15)
        plt.ylabel("Power (Watts)", fontsize=12)
        plt.xlabel("Duration (HH:MM:SS)", fontsize=12, labelpad=10)
        plt.grid(True, linestyle="-", color="#eeeeee", alpha=0.7)

        # Logarithmic scale on the X-axis for power duration metrics
        plt.xscale("log")

        # Automatically determine optimal tick locations on the log scale
        max_time = power_curve_df["Zeit_Sekunden"].max()
        plt.xlim(1, max_time)

        # Generate log-spaced tick locations based on data duration
        if max_time <= 60:
            tick_positions = np.array([1, 5, 10, 30, max_time])
        elif max_time <= 3600:
            tick_positions = np.array(
                [1, 10, 30, 60, 300, 600, 1200, max_time]
            )
        else:
            tick_positions = np.array(
                [1, 10, 60, 300, 1200, 3600, 7200, max_time]
            )

        # Keep only unique ticks that fall within the actual duration range
        tick_positions = np.unique(
            [p for p in tick_positions if p <= max_time]
        )

        # Format ticks dynamically into clean HH:MM:SS strings
        tick_labels = []
        for t in tick_positions:
            hours = int(t // 3600)
            minutes = int((t % 3600) // 60)
            seconds = int(t % 60)
            tick_labels.append(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        # Apply customized ticks and labels to the X-axis
        plt.xticks(tick_positions, tick_labels, fontsize=9, rotation=0)

        plt.legend(loc="upper right")
        plt.tight_layout()

        # Save image file to repository folder for README integration
        plt.savefig("data/fig/Power_Curve.png", dpi=300)
        print("-> 'Power_Curve.png' successfully created.")

        # Display interactive local window panel
        print("-> Opening interactive plot window...")
        plt.show()
        plt.close()

    return power_curve_df