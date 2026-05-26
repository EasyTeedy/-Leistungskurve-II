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

- `pandas` (≥3.0.3) – Datenverarbeitung und -analyse
- `matplotlib` (≥3.10.9) – Visualisierung von Kurven
- `plotly-express` (≥0.4.1) – Interaktive Grafiken
- `numpy` (≥2.4.6) – Numerische Berechnungen

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
│   ├── ekg_data/              # EKG-Daten (optional)
│   └── fig/                   # Ausgabe-Diagramme und Visualisierungen
└── source/
    └── power_analysis.py      # Kernmodul für Leistungskurven-Berechnung
```

## 🔧 Funktionsweise

### Dateneingang

Das Programm erwartet eine CSV-Datei mit Trainingsmetriken. Die Datei **muss** folgende Spalte enthalten:

- **`PowerOriginal`** – Rohe Leistungswerte in Watt

Jede Zeile repräsentiert eine Messung im Abstand von 1 Sekunde.

### Datenverarbeitung

1. **Laden**: CSV-Daten werden mit Pandas eingelesen
2. **Bereinigung**: Spaltennamen werden gesäubert, fehlende Werte behandelt
3. **Berechnung**: Rollende Durchschnitte für alle Zeitfenster werden berechnet
4. **Generierung**: Eine DataFrame mit Zeit (Sekunden) und maximaler Leistung (Watt) wird erstellt

### Ausgabe

Das Programm erzeugt:

- **Konsolenausgabe**: Statistische Zusammenfassung der Leistungsdaten
- **Visualisierungen**: Matplotlib- und Plotly-Grafiken zur Analyse
- **Datendateien**: Berechnete Power Duration Curves als CSV (optional)

## 📊 Beispiel-Workflow

```python
# 1. CSV-Datei laden
df = pd.read_csv("data/activities/activity.csv")

# 2. Leistungskurve berechnen
power_curve = calculate_power_curve(
    power_data=df["PowerOriginal"],
    time_resolution_sec=1,
    plot_curve=True
)

# 3. Ergebnisse anschauen
print(power_curve.head())
```

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

