# Currency Conversion System

## Projektbeschreibung

Dieses Projekt wurde im Rahmen des Moduls 122 entwickelt. Ziel des Projekts ist es, eine API (in diesem Fall die CurrencyAPI) zu nutzen, um Daten zur Umrechnung von CHF in andere Währungen zu erhalten. Das System funktioniert gemäß dem beigefügten Diagramm und besteht aus mehreren Schritten, darunter Datenabruf, -verarbeitung und -weitergabe.

## Inhaltsverzeichnis

- [Currency Conversion System](#currency-conversion-system)
  - [Projektbeschreibung](#projektbeschreibung)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [Voraussetzungen](#voraussetzungen)
  - [Installation](#installation)
  - [Nutzung](#nutzung)
  - [Systemarchitektur](#systemarchitektur)
  - [API-Endpunkt](#api-endpunkt)

## Voraussetzungen

- Python 3.x
- `requests` Bibliothek

## Installation

1. Klonen Sie das Repository:

   ```bash
   git clone https://github.com/IhrBenutzername/currency-conversion-system.git
   ```

2. Navigieren Sie in das Projektverzeichnis:

   ```bash
   cd currency-conversion-system
   ```

3. Installieren Sie die erforderlichen Bibliotheken:

   ```bash
   pip install requests
   ```

## Nutzung

1. Führen Sie das Skript `currency_conversion.py` aus, um die aktuellen Wechselkurse abzurufen und zu verarbeiten:

   ```bash
   python currency_conversion.py
   ```

2. Die verarbeiteten Daten werden in verschiedenen Formaten gespeichert (`data.raw`, `config.cfg`, `log.log`).

## Systemarchitektur

Das System ist in mehrere Komponenten unterteilt, wie im Diagramm dargestellt:

1. **Input**:
   - Abruf von Daten aus verschiedenen Quellen (z. B. Analytics Data, SQL-DB Data, Encrypted Data).

2. **Processing**:
   - Verarbeitung der Daten im zentralen System (`[IhrSystem]`).

3. **Output**:
   - Weitergabe der verarbeiteten Daten an verschiedene Ausgabekanäle (z. B. Execution, Config, Cloud, Publish, DB Storage, Communication).

## API-Endpunkt

Der API-Endpunkt, der in diesem Projekt verwendet wird, lautet:

```
https://api.currencyapi.com/v3/latest?apikey=cur_live_4SCh6zYYyQQ0hzWuDw7l4uU3gyzO4ehTMlmGJmcR&currencies=EUR,USD,CAD,CHF&base_currency=CHF
```