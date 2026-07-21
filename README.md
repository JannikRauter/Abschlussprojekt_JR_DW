# Abschlussprojekt_JR_DW
Asbchlussprojekt Programmieren I von Jannik Rauter und David Wierer.
# Abschlussprojekt_JR_DW

Abschlussprojekt Programmieren I von Jannik Rauter und David Wierer.

## Projektbeschreibung

Dieses Projekt ist eine Python-Anwendung zur Auslegung und Simulation eines E-Bikes auf Basis realer GPS-Daten.

Aus einer CSV-Datei mit GPS-Koordinaten, Zeitstempeln, Höheninformationen und Temperaturdaten werden verschiedene fahrdynamische und elektrische Größen berechnet. Dazu gehören unter anderem:

- zurückgelegte Strecke
- Geschwindigkeit
- Beschleunigung
- Steigung
- Höhenprofil
- Luftdichte
- Rollwiderstand
- Luftwiderstand
- Steigungswiderstand
- Beschleunigungswiderstand
- Drehmoment am Rad
- Motorstrom
- benötigte Motorleistung
- Ladezustand der Akkus

Zusätzlich werden zwei verschiedene Akkutypen simuliert:

- LiPo-Akku
- NMC-Akku

Die beiden Akkutypen unterscheiden sich durch ihre OCV-Kennlinien und ihren Innenwiderstand.

Ziel des Projekts ist es, anhand einer realen Route abzuschätzen, welche Motorleistung und Batteriekapazität für ein E-Bike benötigt werden.

## Projektstruktur

```text
Abschlussprojekt_JR_DW/
│
├── abstract_classes/
│   ├── __init__.py
│   ├── battery_base.py
│   ├── data_analysis_base.py
│   └── simulation_base.py
│
├── src/
│   ├── __init__.py
│   ├── battery_lipo.py
│   ├── battery_nmc.py
│   ├── battery_pack.py
│   ├── data_analysis.py
│   ├── signal_processing.py
│   └── simulation.py
│
├── tests/
│   ├── __init__.py
│   └── test_batteries.py
│
├── final_project_input_data.csv
├── main.py
├── requirements.txt
├── README.md
├── strecke_interaktiv.html
└── .gitignore
```

## Voraussetzungen

Für die Ausführung wird Python benötigt.

Empfohlen:

```text
Python 3.14 oder neuer
```

Das Projekt wurde unter Windows mit PowerShell und einer virtuellen Python-Umgebung entwickelt.

## Installation

### 1. Repository klonen

```bash
git clone https://github.com/JannikRauter/Abschlussprojekt_JR_DW.git
cd Abschlussprojekt_JR_DW
```

Alternativ kann das Repository auch als ZIP-Datei von GitHub heruntergeladen und entpackt werden.

### 2. Virtuelle Umgebung erstellen

Windows PowerShell:

```bash
python -m venv .venv
```

### 3. Virtuelle Umgebung aktivieren

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Wenn die virtuelle Umgebung aktiv ist, steht im Terminal links:

```text
(.venv)
```

Falls PowerShell das Aktivieren blockiert, kann für diese Sitzung folgender Befehl verwendet werden:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Danach erneut aktivieren:

```bash
.venv\Scripts\Activate.ps1
```

### 4. Benötigte Pakete installieren

```bash
pip install -r requirements.txt
```

Falls `pytest` nicht in der `requirements.txt` enthalten ist, muss es zusätzlich installiert werden:

```bash
pip install pytest
```

Für eine sichere Testausführung sollte `pytest` zusätzlich in der `requirements.txt` stehen:

```text
pytest==9.1.1
```

## Benötigte Eingabedatei

Für die Simulation wird folgende Datei benötigt:

```text
final_project_input_data.csv
```

Diese Datei muss im Hauptverzeichnis des Projekts liegen:

```text
Abschlussprojekt_JR_DW/final_project_input_data.csv
```

Die Datei darf nicht umbenannt oder verschoben werden, außer der Pfad wird im Code entsprechend angepasst.

## Projekt ausführen

Das Projekt muss aus dem Hauptverzeichnis gestartet werden.

Richtig:

```bash
python main.py
```

Nicht aus dem Ordner `src` starten.

Falsch:

```bash
cd src
python simulation.py
```

Beim Ausführen werden die GPS-Daten eingelesen, verarbeitet und ausgewertet. Anschließend werden mehrere Diagramme erstellt und eine Zusammenfassung der Fahrt im Terminal ausgegeben.

Zusätzlich wird versucht, eine interaktive HTML-Karte der Strecke zu erzeugen.

Die erzeugte Karte wird unter folgendem Namen gespeichert:

```text
strecke_interaktiv.html
```

Außerdem wird eine Logdatei erstellt:

```text
logging.log
```

## Erwartete Ausgaben

Nach dem Start von:

```bash
python main.py
```

werden unter anderem folgende Ergebnisse berechnet beziehungsweise ausgegeben:

- zurückgelegte Strecke
- benötigte Zeit
- Durchschnittsgeschwindigkeit
- maximale Motorleistung
- Höhenmeter im Anstieg
- Höhenmeter im Abstieg
- berechneter Verbrauch in Ah
- ausgelegte Batteriekapazität
- Diagramme zu Höhenprofil, Geschwindigkeit, Motorleistung und Ladezustand
- interaktive HTML-Karte der Route

## Tests ausführen

Als Erweiterung wurden Unit-Tests mit `pytest` umgesetzt.

Die Testdatei befindet sich hier:

```text
tests/test_batteries.py
```

Tests ausführen:

```bash
pytest -v
```

Erwartetes Ergebnis:

```text
22 passed
```

Die Tests prüfen unter anderem:

- Erstellung von LiPo- und NMC-Akkus
- SOC-Berechnung beim Entladen
- SOC-Berechnung beim Laden
- Begrenzung des SOC auf 0 % und 100 %
- OCV-Werte bei leerem und vollem Akku
- Spannungsverhalten unter Lade- und Entladestrom
- Fehlerbehandlung bei ungültigem Start-SOC
- Fehlerbehandlung bei ungültiger Anzahl paralleler Zellstränge
- Fehlerbehandlung bei negativer Zeitdauer

Falls `pytest` nicht gefunden wird:

```bash
pip install pytest
```

Danach erneut:

```bash
pytest -v
```

## Kurzablauf für den Lektor

Für eine komplette frische Ausführung:

```bash
git clone https://github.com/JannikRauter/Abschlussprojekt_JR_DW.git
cd Abschlussprojekt_JR_DW
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
pytest -v
```

Falls PowerShell die Aktivierung der virtuellen Umgebung blockiert:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.venv\Scripts\Activate.ps1
```

## Softwareaufbau

Das Projekt ist objektorientiert aufgebaut.

### `abstract_classes/`

Dieser Ordner enthält abstrakte Basisklassen beziehungsweise Schnittstellen.

```text
battery_base.py
data_analysis_base.py
simulation_base.py
```

Diese Dateien definieren die grundlegende Struktur für die späteren Implementierungen.

### `src/`

Dieser Ordner enthält die eigentliche Programmlogik.

```text
battery_pack.py
battery_lipo.py
battery_nmc.py
data_analysis.py
signal_processing.py
simulation.py
```

Die zentrale Datenanalyse und Fahrphysik befindet sich in:

```text
src/data_analysis.py
```

Die Glättung von Messdaten erfolgt über:

```text
src/signal_processing.py
```

Die Akkumodelle befinden sich in:

```text
src/battery_pack.py
src/battery_lipo.py
src/battery_nmc.py
```

### `tests/`

Dieser Ordner enthält automatische Tests.

```text
tests/test_batteries.py
```

## Datenanalyse

Die GPS-Daten werden aus der Datei `final_project_input_data.csv` eingelesen.

Die CSV-Datei muss mindestens folgende Spalten enthalten:

```text
lat
lon
ele
time
temperature
```

Die Datei `src/data_analysis.py` prüft beim Einlesen, ob diese Spalten vorhanden sind.

Aus den Daten werden berechnet:

- Zeitdifferenzen zwischen den Messpunkten
- GPS-Distanzen mit der Haversine-Formel
- Geschwindigkeit
- Beschleunigung
- Steigung
- Luftdichte
- Luftwiderstand
- Rollwiderstand
- Steigungswiderstand
- Beschleunigungswiderstand
- Gesamtkraft
- Drehmoment
- Motorstrom

## Signalverarbeitung

Zur Glättung verrauschter GPS- und Bewegungsdaten wird ein gleitender Mittelwert verwendet.

Die Funktion befindet sich in:

```text
src/signal_processing.py
```

Dadurch werden unter anderem Geschwindigkeit, Steigung, Beschleunigung und Kräfte geglättet.

## Akkumodell

Die Akkus werden objektorientiert modelliert.

Gemeinsame Funktionen für LiPo und NMC befinden sich in:

```text
src/battery_pack.py
```

Die konkreten Akkutypen befinden sich in:

```text
src/battery_lipo.py
src/battery_nmc.py
```

Die beiden Akkutypen unterscheiden sich durch:

- OCV-Kennlinie
- Zellinnenwiderstand

### LiPo-Akku

Der LiPo-Akku ist als 10SxP-Akkupack modelliert.

Eigenschaften:

```text
10 Zellen in Serie
x parallele Zellstränge
Zellinnenwiderstand: 8 mOhm
OCV-Kennlinie: 32 V bis 42 V
```

### NMC-Akku

Der NMC-Akku ist ebenfalls als 10SxP-Akkupack modelliert.

Eigenschaften:

```text
10 Zellen in Serie
x parallele Zellstränge
Zellinnenwiderstand: 7 mOhm
OCV-Kennlinie: 32 V bis 42 V
```

## Vorzeichenkonvention für den Batteriestrom

Im Projekt gilt folgende Konvention:

```text
current > 0  bedeutet Entladen
current < 0  bedeutet Laden
```

Beispiele:

```text
current = 10 A   -> Akku wird entladen
current = -10 A  -> Akku wird geladen
```

## SOC-Grenzen

Der Ladezustand wird als Wert zwischen 0.0 und 1.0 gespeichert.

```text
0.0 entspricht 0 %
1.0 entspricht 100 %
```

Der SOC wird auf den gültigen Bereich begrenzt:

```text
0.0 <= SOC <= 1.0
```

Wenn der SOC rechnerisch unter 0 % fällt oder über 100 % steigt, wird eine Warnung über das Logging-System ausgegeben und der Wert auf die jeweilige Grenze gesetzt.

## Logging und Fehlerbehandlung

Das Projekt verwendet das Python-Modul `logging`.

Die Logdatei wird unter folgendem Namen gespeichert:

```text
logging.log
```

Im Code werden zusätzlich `assert`-Anweisungen verwendet, um ungültige Zustände frühzeitig zu erkennen.

Beispiele:

- fehlende CSV-Spalten
- ungültiger Start-SOC
- negative Batteriekapazität
- ungültige Anzahl paralleler Zellstränge
- negative Zeitdauer
- unplausible Temperaturwerte
- ungültige Luftdichtewerte

## Erweiterungen

Zusätzlich zu den Minimalanforderungen wurden mehrere Erweiterungen umgesetzt.

### 1. Rollwiderstand

Der Rollwiderstand wird in der Fahrphysik berücksichtigt und fließt in die benötigte Gesamtkraft und damit in die Motorleistung ein.

Verwendete Grundidee:

```text
F_roll = c_r * m * g * cos(alpha)
```

Dabei ist:

```text
c_r       Rollwiderstandsbeiwert
m         Gesamtmasse aus Fahrer und Fahrrad
g         Erdbeschleunigung
alpha     Steigungswinkel
```

Wenn das Fahrrad steht, wird der Rollwiderstand auf 0 gesetzt.

### 2. Interaktive HTML-Karte mit Folium

Die gefahrene Strecke wird auf einer interaktiven HTML-Karte dargestellt.

Datei:

```text
strecke_interaktiv.html
```

Die Strecke wird mit `folium` geplottet. Die Höhenmeter werden farblich markiert. Zusätzlich werden Start- und Zielpunkt gesetzt.

Die Karte kann nach dem Ausführen von `main.py` im Browser geöffnet werden.

### 3. Unit-Tests

Für die Batterieklassen wurden automatische Unit-Tests mit `pytest` erstellt.

Datei:

```text
tests/test_batteries.py
```

Ausführung:

```bash
pytest -v
```

Erwartetes Ergebnis:

```text
22 passed
```

### 4. Indirekte Parameterstudien

Mehrere wichtige Simulationsparameter sind im Code zentral als Variablen beziehungsweise Konstanten definiert und können verändert werden.

Beispiele:

```text
Masse Fahrer
Masse Fahrrad
Gesamtmasse
Radgröße
Luftwiderstandsbeiwert mal Stirnfläche
Rollwiderstandsbeiwert
Motorkonstante
Akkukapazität
Anzahl paralleler Zellstränge
```

Dadurch können verschiedene Szenarien simuliert werden, ohne die komplette Programmlogik umzuschreiben.

Beispielsweise kann untersucht werden, wie sich eine andere Fahrer- oder Fahrradmasse auf Kraft, Motorleistung, Strom und Batteriekapazität auswirkt.

### 5. Luftdichte aus Höhe und Temperatur

Die Luftdichte wird nicht nur als konstanter Wert angenommen, sondern aus Höhe und Temperatur berechnet.

Dazu werden die Höhenmeter aus den GPS-Daten und die Temperaturdaten aus der CSV-Datei verwendet.

Die berechnete Luftdichte fließt anschließend in die Luftwiderstandsberechnung ein und beeinflusst dadurch die benötigte Motorleistung.

## Diagramme

Beim Ausführen des Programms werden Diagramme erzeugt, unter anderem:

- Höhenprofil über Distanz
- Geschwindigkeit über Zeit
- Motorleistung über Zeit
- Ladezustand der LiPo-Batterie über Zeit
- Ladezustand der NMC-Batterie über Zeit

Die Diagramme werden mit `matplotlib` dargestellt.

## Häufige Probleme und Lösungen

### Problem: Virtuelle Umgebung ist nicht aktiv

Prüfen, ob im Terminal links `(.venv)` steht.

Falls nicht:

```bash
.venv\Scripts\Activate.ps1
```

### Problem: PowerShell blockiert die virtuelle Umgebung

Für diese Sitzung erlauben:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Danach erneut aktivieren:

```bash
.venv\Scripts\Activate.ps1
```

### Problem: Pakete fehlen

Falls ein Fehler wie `ModuleNotFoundError` erscheint:

```bash
pip install -r requirements.txt
```

Falls `pytest` fehlt:

```bash
pip install pytest
```

### Problem: Eingabedatei wird nicht gefunden

Prüfen, ob folgende Datei im Hauptverzeichnis liegt:

```text
final_project_input_data.csv
```

### Problem: Tests werden nicht gefunden

Prüfen, ob die Testdatei an folgender Stelle liegt:

```text
tests/test_batteries.py
```

Die Testfunktionen müssen mit `test_` beginnen.

Tests starten mit:

```bash
pytest -v
```

### Problem: Projekt wird aus dem falschen Ordner gestartet

Das Projekt muss aus dem Hauptverzeichnis gestartet werden:

```bash
python main.py
```

Nicht aus dem Ordner `src`.

## Git und Versionsverwaltung

Das Projekt wurde mit Git und GitHub versioniert.

Für eine bessere Nachvollziehbarkeit wurden Commit-Nachrichten nach dem Prinzip der Conventional Commits verwendet.

Beispiele:

```text
feat: LiPo-Batteriemodell hinzufügen
feat: NMC-Batteriemodell hinzufügen
test: Batterie-Unit-Tests hinzufügen
fix: NMC-Batteriedatei wiederherstellen
docs: README erweitern
```

## Hinweise zur Bewertung

Das Projekt enthält:

- Python-Projekt mit Objektorientierung
- abstrakte Basisklassen
- Verarbeitung realer GPS-Daten
- E-Bike-Auslegung anhand einer Route
- Berechnung von Geschwindigkeit, Beschleunigung, Steigung und Leistung
- zwei verschiedene Akkutypen
- Akku-Simulation mit SOC-Verlauf
- Logging
- Fehlerbehandlung mit Assertions
- `requirements.txt`
- README mit Installations- und Ausführungsanleitung
- Unit-Tests als Erweiterung
- Rollwiderstand als Erweiterung
- Luftdichteberechnung als Erweiterung
- interaktive Folium-Karte als Erweiterung
- änderbare Parameter für indirekte Parameterstudien

## Autoren

Jannik Rauter  
David Wierer
