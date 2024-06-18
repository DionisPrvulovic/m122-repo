# Projektdefinition: Währungskonverter System

## Übersicht

Dieses Dokument beschreibt den Ablauf des Währungskonverter-Systems, das entwickelt wurde, um aktuelle Wechselkurse von einer API abzurufen und in eine Tabelle zu konvertieren. Diese Tabelle wird als PNG-Bild gespeichert und auf einen Server hochgeladen, um sie im Webbrowser darzustellen. Zusätzlich werden Logs erstellt und optional die abgerufenen JSON-Daten gespeichert.

## Systemablauf

Das System arbeitet wie folgt:

1. **Konfiguration**:
   - Die Konfigurationsdatei `currency.cfg` enthält alle notwendigen Einstellungen, wie API-Schlüssel, Endpunkte, SSH-Zugangsdaten, und Optionen zur Dateierstellung und -übertragung.

2. **Datenabruf**:
   - Das Skript `currency.py` verwendet die Informationen aus der `currency.cfg`, um die neuesten Wechselkurse von einem API-Endpunkt im JSON-Format abzurufen.

3. **Datenverarbeitung**:
   - Die abgerufenen Daten werden verarbeitet, um eine Tabelle zu erstellen, die die Wechselkurse verschiedener Währungen in Schweizer Franken (CHF) darstellt.

4. **Erstellung der Tabelle**:
   - Eine PNG-Datei der Tabelle wird erstellt und im `dump`-Verzeichnis des Projektordners gespeichert.

5. **Logging**:
   - Ein Log-File wird erstellt, um mögliche Fehler und wichtige Ereignisse während der Ausführung des Skripts zu protokollieren.

6. **Optionale Speicherung**:
   - Die JSON-Daten des API-Endpunkts können ebenfalls im `dump`-Verzeichnis gespeichert werden, wenn dies in der `currency.cfg` konfiguriert ist.

7. **Dateiübertragung**:
   - Die erstellte PNG-Datei wird auf einen Linux-Ubuntu-Server hochgeladen, der Nginx nutzt, um die Tabelle grafisch im Webbrowser darzustellen.
   - Optional kann die Tabelle bei jeder Generierung per E-Mail verschickt werden, sofern dies in der `currency.cfg` konfiguriert ist.

## Diagramm

Das folgende Aktivitätsdiagramm stellt den Ablauf des Systems grafisch dar:

![Aktivitätsdiagramm](activity_diagram.png)

## Zusammenfassung

Das Währungskonverter-System ist ein umfassendes Tool, das die folgenden Aufgaben automatisiert:
- Abrufen und Verarbeiten von Wechselkursdaten.
- Erstellung und Speicherung einer Tabelle als PNG-Bild.
- Logging wichtiger Ereignisse und Fehler.
- Optionale Speicherung der Rohdaten.
- Hochladen der Tabelle auf einen Server und optionaler E-Mail-Versand.

Alle diese Funktionen sind über die `currency.cfg` Datei konfigurierbar, was Flexibilität und Anpassungsfähigkeit des Systems gewährleistet.

