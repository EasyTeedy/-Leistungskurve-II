from source.power_analysis import power_curve_analysis
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def format_time(seconds):
    """Zeit in HH:MM:SS Format konvertieren."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d}"


def get_perfect_log_time_ticks(max_time):
    """Logarithmische Zeitachsen-Ticks generieren."""
    # Vordefinierte Zeitintervalle in Sekunden
    potential_ticks = [
        1, 2, 5, 10, 20, 30,         # Sekunden
        60, 120, 300, 600, 1200,     # Minuten
        1800, 3600, 7200, 14400,     # Stunden
        21600, 43200                 # 6h, 12h
    ]
    
    # Ticks innerhalb der Fahrtdauer behalten
    ticks = [t for t in potential_ticks if t < max_time]
    
    # Bei zu vielen Ticks reduzieren (Ziel: 12 Ticks)
    if len(ticks) > 15:
        indices = np.unique(np.linspace(0, len(ticks)-1, num=12, dtype=int))
        ticks = [ticks[i] for i in indices]
    
    # Endpunkt immer einschließen
    ticks.append(max_time)
    return np.unique(ticks).astype(int)


def plot_power_curve(power_curve_df, color):
    if color == "green":
        line_color = "#7cb342"
        fill_color = "#f5f5f5"
    elif color == "blue":
        line_color = "#42a5f5"
        fill_color = "#e3f2fd"
    elif color == "orange":
        line_color = "#ff9800"
        fill_color = "#fff3e0"
    else:
        line_color = "#b342b3"
        fill_color = "#f5f5f5"

    plt.figure(figsize=(18, 7))
    
    # Logarithmische Skalierung für X-Achse
    plt.xscale('log')

    # Power-Kurve plotten
    plt.plot(
        power_curve_df["Zeit_Sekunden"],
        power_curve_df["Leistung_Watt"],
        color=line_color, 
        linewidth=2,
        label="Today",
    )

    # Hintergrund füllen
    plt.fill_between(
        power_curve_df["Zeit_Sekunden"],
        power_curve_df["Leistung_Watt"],
        color=fill_color,
        alpha=0.5,
    )

    # X-Achse mit Zeit-Labels formatieren
    max_time = power_curve_df["Zeit_Sekunden"].max()
    tick_positions = get_perfect_log_time_ticks(max_time)
    tick_labels = [format_time(t) for t in tick_positions]
    
    # Ticks anwenden und Minor-Ticks deaktivieren
    ax = plt.gca()
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45)
    ax.xaxis.set_minor_locator(plt.NullLocator())

    # Chart styling and labeling
    plt.title("Power Curve Analysis", fontsize=14, pad=15)
    plt.ylabel("Power (Watts)", fontsize=12)
    plt.xlabel("Duration (HH:MM:SS)", fontsize=12, labelpad=10)
    plt.grid(True, linestyle="-", color="#eeeeee", alpha=0.7)
    plt.tight_layout() 

    plt.savefig("data/fig/power_curve_chart.png")
    plt.close()



def output_terminal_summary(power_series, result_df):
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
        if len(power_series) >= seconds:
            rolling_mean = power_series.rolling(window=seconds).mean()
            max_value = rolling_mean.max()
            print(f"Max power over {name:<11}: {max_value:.1f} Watts")
        else:
            print(
                f"Max power over {name:<11}: Not available (activity duration too short)"
            )

    print("\n--- Complete Power Curve DataFrame Summary ---")
    print(result_df.head(10)) 
    print("...")
    print(result_df.tail(5)) 




def read_and_plot_power_curve():
    csv_filename = "data/activities/activity.csv"

    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        print(f"Error: The file '{csv_filename}' could not be found!")
        return

    df.columns = df.columns.str.strip()
    
    # Duration-Spalte aus Zeilenindizes setzen
    df["Duration"] = range(1, len(df) + 1)

    if "PowerOriginal" not in df.columns:
        print("Error: The column 'PowerOriginal' is missing from the CSV file.")
        print("Available columns are:", list(df.columns))
        return

    power_series = df["PowerOriginal"]
    time_step = 1 

    print(
        f"Processing power duration curve for {len(power_series)} seconds of data..."
    )

    result_df = power_curve_analysis(power_data=power_series, time_resolution_sec=time_step)

    output_terminal_summary(power_series, result_df)
    plot_power_curve(result_df, color="green")
