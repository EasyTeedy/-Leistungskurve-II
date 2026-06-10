# Leistungskurve II – Power Duration Curve Analyzer

Eine Python-Anwendung zur Berechnung und Visualisierung von Leistungskurven aus Trainingsaktivitätsdaten. Dieses Projekt analysiert Rohdaten von Trainingsgeräten und generiert detaillierte Leistungs-Zeit-Kurven für die sportliche Leistungsanalyse.

## 🎯 Projektübersicht

Das Tool verarbeitet CSV-Dateien mit Aktivitätsdaten und berechnet die **Power Duration Curve** – eine grafische Darstellung der maximalen durchschnittlichen Leistung über verschiedene Zeiträume. Dies ist besonders nützlich für:

- 🚴 Radsportler und Triathleten
- ⚡ Leistungsanalyse und Training
- 📊 Datengestützte Trainingsplanung
- 🔍 Vergleich von Trainingseinheiten

## 📋 Anforderungen

- **Python**: 3.13.x
- **Package Manager**: [PDM](https://pdm-backend.readthedocs.io/)

### Abhängigkeiten

Die erforderlichen Python-Pakete sind in `pyproject.toml` definiert:

- `pandas` (≥2.2.0, <3.0.0) – Datenverarbeitung und -analyse
- `matplotlib` (≥3.8.0) – Visualisierung von Kurven
- `plotly` (≥5.0.0) – Interaktive Grafiken
- `numpy` (≥2.0.0) – Numerische Berechnungen
- `nbformat` (≥5.10.0) – Notebook-Format-Unterstützung

## 🚀 Installation und Verwendung

### 1. Repository klonen

```bash
git clone <repository-url>
cd Leistungskurve_2
```

### 2. Abhängigkeiten installieren

```bash
pdm install
```

### 3. Virtuelle Umgebung aktivieren

```bash
source .venv/bin/activate
```

### 4. Programm ausführen

```bash
python main.py
```

## 📁 Projektstruktur

```
Leistungskurve_2/
├── main.py                    # Haupteinstiegspunkt
├── pyproject.toml             # Projekt- und Abhängigkeitskonfiguration
├── README.md                  # Diese Datei
├── data/
│   ├── activities/
│   │   └── activity.csv       # Eingabe-Trainingsaktivitätsdaten
│   └── fig/                   # Ausgabe-Diagramme und Visualisierungen
└── source/
    ├── power_analysis.py      # Kernmodul: Power-Kurven-Berechnung
    ├── plotting.py            # Visualisierung mit Matplotlib und Plotly
    └── util.py                # Utility-Funktionen (Dateihandling, Formatierung)
```

## 🔧 Funktionsweise

### Module

**`source/power_analysis.py`**
- `power_curve_analysis()` – Berechnet die Power-Dauer-Kurve
- Nutzt rollende Durchschnitte über alle möglichen Zeitfenster
- Gibt eine DataFrame mit Zeit (Sekunden) und maximaler Leistung (Watt) zurück

**`source/plotting.py`**
- `plot_power_curve()` – Visualisiert die Leistungskurve mit Matplotlib
- Logarithmische X-Achse für bessere Lesbarkeit
- Farbcodierung und Styling für verschiedene Trainingstypen

**`source/util.py`**
- `load_activity_csv()` – Lädt und validiert CSV-Aktivitätsdaten
- `validate_power_data()` – Prüft Datenqualität
- `format_time()` – Konvertiert Sekunden in HH:MM:SS Format

### Dateneingang

Das Programm erwartet eine CSV-Datei mit Trainingsmetriken. Die Datei **muss** folgende Spalte enthalten:

- **`PowerOriginal`** – Rohe Leistungswerte in Watt

Jede Zeile repräsentiert eine Messung im Abstand von 1 Sekunde.

### Datenverarbeitung

1. **Laden**: CSV-Daten werden mit `util.load_activity_csv()` eingelesen
2. **Bereinigung**: Spaltennamen werden gesäubert, fehlende Werte behandelt
3. **Berechnung**: `power_analysis.power_curve_analysis()` berechnet rollende Durchschnitte
4. **Visualisierung**: `plotting.plot_power_curve()` erzeugt Grafiken

### Ausgabe

Das Programm erzeugt:

- **Konsolenausgabe**: Statistische Zusammenfassung der Leistungsdaten
- **Visualisierungen**: Matplotlib-Grafiken zur Analyse
- **Datendateien**: Berechnete Power Duration Curves als PNG im Ordner `data/fig/`

## 📊 Beispiel-Workflow

```python
# main.py nutzt diese Module automatisch:

# 1. CSV-Datei laden (util.py)
from source.util import load_activity_csv

df = load_activity_csv("data/activities/activity.csv")

# 2. Leistungskurve berechnen (power_analysis.py)
from source.power_analysis import power_curve_analysis

power_curve = power_curve_analysis(
    power_data=df["PowerOriginal"],
    time_resolution_sec=1
)

# 3. Visualisieren (plotting.py)
from source.plotting import plot_power_curve

plot_power_curve(power_curve, color="green")
```

Die komplette Funktionalität wird durch Ausführung von `python main.py` aktiviert.

## 🛠️ Entwicklung

### Neue Abhängigkeiten hinzufügen

```bash
pdm add <package-name>
```

### Abhängigkeiten aktualisieren

```bash
pdm update
pdm lock
```

### Virtuelle Umgebung neu initialisieren

```bash
pdm install --fresh
```

**Hinweis**: Stellen Sie sicher, dass Ihre CSV-Aktivitätsdaten das Format und die erforderlichen Spalten erfüllen, bevor Sie das Programm ausführen.

