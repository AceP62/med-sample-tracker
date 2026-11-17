import csv
from datetime import datetime

# Medizinische Grenzwerte für den gekühlten Probentransport
MIN_TEMP_C = 2.0
MAX_TEMP_C = 8.0
MAX_TRANSPORT_MINUTES = 120


def check_sample(sample: dict) -> list[str]:
    """Prüft eine einzelne Probe auf Kühlketten- und Zeitüberschreitungen."""
    alerts = []
    temp = float(sample["temperature_c"])
    minutes = int(sample["transport_minutes"])

    if temp < MIN_TEMP_C:
        alerts.append(f"Unterkühlung ({temp} °C - Minimum: {MIN_TEMP_C} °C)")
    elif temp > MAX_TEMP_C:
        alerts.append(f"Überhitzung ({temp} °C - Maximum: {MAX_TEMP_C} °C)")

    if minutes > MAX_TRANSPORT_MINUTES:
        alerts.append(f"Transportzeit überschritten ({minutes} Min. - Maximum: {MAX_TRANSPORT_MINUTES} Min.)")

    return alerts


def analyze_shipments(file_path: str) -> None:
    """Liest die Transportdaten aus der CSV-Datei und gibt einen Statusbericht aus."""
    total_samples = 0
    critical_samples = 0

    print("=" * 60)
    print(f"MED-SAMPLE-TRACKER | Prüfbericht vom {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print("=" * 60)

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_samples += 1
            alerts = check_sample(row)

            if alerts:
                critical_samples += 1
                print(f"[ALARM] Probe {row['sample_id']} ({row['sample_type']} aus {row['origin']}):")
                for alert in alerts:
                    print(f"        -> {alert}")
            else:
                print(f"[OK]    Probe {row['sample_id']} ({row['sample_type']}) - Werte im Normbereich.")

    print("-" * 60)
    print(f"Zusammenfassung: {total_samples} Proben geprüft | {critical_samples} kritische Abweichungen")
    print("=" * 60)


if __name__ == "__main__":
    analyze_shipments("samples.csv")