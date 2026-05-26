import pandas as pd
from source.power_analysis import calculate_power_curve


def main():
    # Relative path to the source CSV file (adjust if necessary)
    csv_filename = "data/activities/activity.csv"

    # 1. Load the CSV dataset
    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        print(f"Error: The file '{csv_filename}' could not be found!")
        return
    

    # Clean up column names by stripping any accidental leading/trailing whitespaces
    df.columns = df.columns.str.strip()

    # Verify that the required power metrics column is present
    if "PowerOriginal" not in df.columns:
        print("Error: The column 'PowerOriginal' is missing from the CSV file.")
        print("Available columns are:", list(df.columns))
        return

    # 2. Extract the relevant data series
    power_series = df["PowerOriginal"]
    time_step = 1  # Standard sampling rate: 1 row represents 1 second

    print(
        f"Processing power duration curve for {len(power_series)} seconds of data..."
    )

    # 3. Invoke the core module function to compute data points, save the screenshot, and show the plot
    result_df = calculate_power_curve(
        power_data=power_series, time_resolution_sec=time_step, plot_curve=True
    )

    # 4. Compute and display specific rolling mean checkpoints
    # Defining standard physiological intervals in seconds
    intervals = {
        "5 Seconds": 5,
        "10 Seconds": 10,
        "20 Seconds": 20,
        "1 Minute": 60,
        "5 Minutes": 5 * 60,
        "20 Minutes": 20 * 60,
    }

    print("\n==================================================")
    print("--- MAXIMUM MEAN POWER OUTPUTS (BEST EFFORTS) ---")
    print("==================================================")

    for name, seconds in intervals.items():
        # Ensure the recorded activity is long enough for the target interval window
        if len(power_series) >= seconds:
            # Compute the rolling average over the specific window size
            rolling_mean = power_series.rolling(window=seconds).mean()
            # Extract the absolute peak average value achieved
            max_value = rolling_mean.max()
            print(f"Max power over {name:<11}: {max_value:.1f} Watts")
        else:
            print(
                f"Max power over {name:<11}: Not available (activity duration too short)"
            )

    # 5. Display a brief console preview of the complete resulting dataset
    print("\n--- Complete Power Curve DataFrame Summary ---")
    print(result_df.head(10))  # Preview the short-duration sprint values
    print("...")
    print(result_df.tail(5))  # Preview the long-duration endurance thresholds


if __name__ == "__main__":
    main()