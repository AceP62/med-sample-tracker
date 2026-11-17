# Med-Sample-Tracker

Ein leichtgewichtiges Python-Tool zur automatisierten Überwachung von Kühlketten- und Transportparametern medizinischer Proben.

## Hintergrund & Ziel
In der Telemedizin und medizinischen Logistik müssen sensible Parameter (wie Temperaturen bei Blutproben oder Vitaldaten im Home-Monitoring) zuverlässig auf Grenzwerte geprüft werden. Dieses Projekt demonstriert die automatisierte Auswertung von Transportdaten, die Erkennung kritischer Abweichungen sowie die Erstellung eines strukturierten Prüfberichts.

*Hinweis: Alle verwendeten Datensätze sind rein synthetisch und enthalten keine personenbezogenen Patientendaten.*

## Funktionen
- Einlesen strukturierter Probendaten (`CSV`)
- Automatisierte Prüfung auf Kühlketten-Unterbrechungen (Normbereich: `2.0 °C – 8.0 °C`)
- Überwachung der maximalen Transportdauer (`max. 120 Minuten`)
- Konsolenausgabe eines übersichtlichen Prüfberichts mit Alarm-Kennzeichnung

## Installation & Ausführung
Das Projekt nutzt ausschließlich die Python-Standardbibliothek (Python 3.10+).

1. Repository klonen:
   ```bash
   git clone [https://github.com/AceP62/med-sample-tracker.git](https://github.com/AceP62/med-sample-tracker.git)
   cd med-sample-tracker