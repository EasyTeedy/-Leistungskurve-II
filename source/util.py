# Utility-Funktionen für Dateihandling

import pandas as pd


def format_time(seconds):
    """Zeit in HH:MM:SS Format konvertieren.
    
    Args:
        seconds: Sekunden als Integer oder Float.
        
    Returns:
        String im Format HH:MM:SS.
    """
    hours = int(seconds) // 3600
    minutes = (int(seconds) % 3600) // 60
    secs = int(seconds) % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def load_activity_csv(csv_path):
    """Activity-CSV-Datei laden und validieren.
    
    Args:
        csv_path: Pfad zur CSV-Datei.
        
    Returns:
        DataFrame mit geladenen Daten.
        
    Raises:
        FileNotFoundError: Wenn Datei nicht existiert.
        ValueError: Wenn erforderliche Spalten fehlen.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV-Datei nicht gefunden: {csv_path}")
    
    # Spaltenamen bereinigen
    df.columns = df.columns.str.strip()
    
    # Erforderliche Spalten prüfen
    required_columns = ["PowerOriginal"]
    missing = [col for col in required_columns if col not in df.columns]
    
    if missing:
        raise ValueError(
            f"Erforderliche Spalten fehlen: {missing}. "
            f"Verfügbare Spalten: {list(df.columns)}"
        )
    
    return df


def validate_power_data(power_series):
    """Power-Daten validieren.
    
    Args:
        power_series: Pandas Series mit Leistungswerten.
        
    Returns:
        Boolean - True wenn valide, False wenn zu kurz.
    """
    return len(power_series) > 0