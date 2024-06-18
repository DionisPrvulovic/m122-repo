# Währungskonverter Projekt

## Übersicht

Dieses Repository enthält ein Währungskonverter-Projekt, das im Rahmen des TBZ Modul-122 entwickelt wurde. Das Projekt ist in mehrere Ordner strukturiert, um den Code und die Dokumentation zu organisieren.

## Repository-Struktur

- **project/**
  - Dieser Ordner enthält den Hauptcode für die Währungskonverter-Anwendung.
  - **currency.py**: Das Hauptskript für das Abrufen von Währungsdaten, Erstellen einer Tabelle und optionales Hochladen auf einen Server.
  - **currency.cfg**: Die Konfigurationsdatei mit API-Schlüsseln, SSH-Details und anderen Optionen.
  - **README.md**: Dokumentation für den Projektordner, die den Code und seine Funktionalität erklärt.

- **scripts/**
  - Dieser Ordner enthält verschiedene Skripte, die mit dem Projekt zu tun haben, wie z.B. Setup-Skripte, Dienstprogramme und möglicherweise Bereitstellungsskripte.

## Projektordner (`project/`)

### currency.py

Dieses Skript führt die folgenden Aufgaben aus:

1. **Abrufen von Währungsdaten**: Holt die neuesten Währungsdaten von der API, die in der `currency.cfg` Datei angegeben ist.
2. **Erstellen einer Tabelle**: Erstellt eine Tabelle mit den abgerufenen Währungsdaten und speichert sie lokal ab.
3. **Optionales Hochladen**: Lädt die erstellte Tabelle auf einen konfigurierten Server hoch, falls dies aktiviert ist.

### currency.cfg

Die `currency.cfg` Datei enthält die Konfiguration für das Skript:

- **API-Konfiguration**: API-Schlüssel und URL für den Abruf der Währungsdaten.
- **SSH-Konfiguration**: Details für den SSH-Zugriff, um Dateien auf einen Server hochzuladen.
- **Optionen**: Verschiedene Einstellungen wie das Erstellen einer Bilddatei der Tabelle, das Speichern der Daten als JSON-Datei, Log-Einstellungen und Darstellungsoptionen für die Tabelle.
- **Pfade**: Lokale und entfernte Pfade für das Speichern und Hochladen der erstellten Tabelle.

## Verwendung

1. **Konfiguration anpassen**: Passen Sie die `currency.cfg` Datei an Ihre Bedürfnisse an.
2. **Skript ausführen**: Führen Sie das `currency.py` Skript aus, um die Währungsdaten abzurufen und die Tabelle zu erstellen.
3. **Ergebnisse überprüfen**: Überprüfen Sie die generierte Tabelle und die optional erstellten JSON-Dateien und Logs.