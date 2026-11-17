import csv
import json
from datetime import datetime

# Medizinische Grenzwerte für den gekühlten Probentransport
MIN_TEMP_C = 2.0
MAX_TEMP_C = 8.0
CRITICAL_MIN_TEMP_C = 1.0
CRITICAL_MAX_TEMP_C = 10.0
MAX_TRANSPORT_MINUTES = 120


def check_sample(sample: dict) -> list[dict]:
    """Prüft eine Probe und gibt strukturierte Alarme mit Schweregrad zurück."""
    alerts = []
    temp = float(sample["temperature_c"])
    minutes = int(sample["transport_minutes"])

    if temp < MIN_TEMP_C:
        severity = "CRITICAL" if temp < CRITICAL_MIN_TEMP_C else "WARNING"
        alerts.append({
            "severity": severity,
            "type": "TEMPERATURE_LOW",
            "message": f"Unterkühlung ({temp} °C - Minimum: {MIN_TEMP_C} °C)"
        })
    elif temp > MAX_TEMP_C:
        severity = "CRITICAL" if temp > CRITICAL_MAX_TEMP_C else "WARNING"
        alerts.append({
            "severity": severity,
            "type": "TEMPERATURE_HIGH",
            "message": f"Überhitzung ({temp} °C - Maximum: {MAX_TEMP_C} °C)"
        })

    if minutes > MAX_TRANSPORT_MINUTES:
        alerts.append({
            "severity": "CRITICAL",
            "type": "TRANSPORT_TIMEOUT",
            "message": f"Transportzeit überschritten ({minutes} Min. - Maximum: {MAX_TRANSPORT_MINUTES} Min.)"
        })

    return alerts


def export_alerts_to_json(alert_records: list[dict], output_path: str) -> None:
    """Speichert alle erkannten Alarme als nachvollziehbares JSON-Protokoll."""
    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_alerts": len(alert_records),
        "alerts": alert_records
    }

    with open(output_path, mode="w", encoding="utf-8") as json_file:
        json.dump(report, json_file, indent=4, ensure_ascii=False)


def analyze_shipments(csv_path: str, json_output_path: str) -> None:
    """Liest Transportdaten ein, prüft Grenzwerte und exportiert Alarme."""
    total_samples = 0
    critical_samples = 0
    all_alert_records = []

    print("=" * 65)
    print(f"MED-SAMPLE-TRACKER | Prüfbericht vom {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print("=" * 65)

    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_samples += 1
            alerts = check_sample(row)

            if alerts:
                critical_samples += 1
                print(f"[ALARM] Probe {row['sample_id']} ({row['sample_type']} aus {row['origin']}):")
                for alert in alerts:
                    print(f"        -> [{alert['severity']}] {alert['message']}")
                    all_alert_records.append({
                        "sample_id": row["sample_id"],
                        "sample_type": row["sample_type"],
                        "origin": row["origin"],
                        "severity": alert["severity"],
                        "type": alert["type"],
                        "message": alert["message"]
                    })
            else:
                print(f"[OK]    Probe {row['sample_id']} ({row['sample_type']}) - Werte im Normbereich.")

    export_alerts_to_json(all_alert_records, json_output_path)

    print("-" * 65)
    print(f"Zusammenfassung: {total_samples} Proben geprüft | {critical_samples} auffällige Proben")
    print(f"Protokoll gespeichert unter: {json_output_path}")
    print("=" * 65)


if __name__ == "__main__":
    analyze_shipments("samples.csv", "alerts.json")