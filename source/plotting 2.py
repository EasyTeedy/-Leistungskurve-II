from source.power_analysis import power_curve_analysis
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def format_time(seconds):
    """Helper function to format seconds into HH:MM:SS."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d}"


def get_perfect_log_time_ticks(max_time):
    """Generates clean, log-spaced time ticks tailored to any data duration."""
    # Vordefinierte, glatte Zeitstempel (in Sekunden), die log-ähnlich wachsen
    potential_ticks = [
        1, 2, 5, 10, 20, 30,         # Sekunden
        60, 120, 300, 600, 1200,     # Minuten (1m, 2m, 5m, 10m, 20m)
        1800, 3600, 7200, 14400,     # 30m, 1h, 2h, 4h
        21600, 43200                 # 6h, 12h (für Langstrecken)
    ]
    
    # 1. Nur Ticks behalten, die innerhalb der echten Fahrdauer liegen
    ticks = [t for t in potential_ticks if t < max_time]
    
    # 2. Falls es bei langen Fahrten zu viele Ticks werden, dünnen wir sie geometrisch aus
    if len(ticks) > 6:
        indices = np.unique(np.geomspace(1, len(ticks), num=5, dtype=int)) - 1
        ticks = [ticks[i] for i in indices]
        
    # 3. Das exakte Ende der CSV-Daten IMMER als letzten Tick anhängen
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

    plt.figure(figsize=(15, 6))
    
    # Schaltet die X-Achse auf eine echte, mathematische Log-Skala um
    plt.xscale('log')

    # Plot der eigentlichen Watt-Kurve
    plt.plot(
        power_curve_df["Zeit_Sekunden"],
        power_curve_df["Leistung_Watt"],
        color=line_color, 
        linewidth=2,
        label="Today",
    )

    # Hintergrund-Fläche füllen
    plt.fill_between(
        power_curve_df["Zeit_Sekunden"],
        power_curve_df["Leistung_Watt"],
        color=fill_color,
        alpha=0.5,
    )

    # --- AUTOMATISCHE LOG-X-ACHSEN-FORMATIERUNG ---
    max_time = power_curve_df["Zeit_Sekunden"].max()
    
    # Hol dir die glatten, vordefinierten Log-Ticks
    tick_positions = get_perfect_log_time_ticks(max_time)
    
    # Formatiere die Sekunden-Ticks in gut lesbare HH:MM:SS Strings
    tick_labels = [format_time(t) for t in tick_positions]
    
    # Labels an der Achse setzen
    plt.xticks(tick_positions, tick_labels, rotation=45)
    # -----------------------------------------------

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
    
    # Repariert die defekte Zeitachse aus der CSV-Datei
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
