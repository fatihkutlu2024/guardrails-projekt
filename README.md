# 🛡️ HR Guardrails LLM Assistant

## Projektbeschreibung

Dieses Projekt ist meine Abgabe für die **Guardrails Challenge**.

Ein KI-HR-Assistent mit mehrstufiger Validierung. Das System nutzt **Input- und Output-Guards** mit strukturierten Pydantic-Schemas, um Datenschutzverstöße (DSGVO), unzulässige Rechtsberatung und Prompt-Injections in Unternehmensumgebungen zuverlässig abzufangen.

Das Projekt verwendet hierbei einen eigenen Custom-Guardrail-Ansatz auf Basis von **OpenAI Structured Outputs** und **Pydantic**.

---

## Architektur & Funktionsweise

Das System schützt Unternehmensrichtlinien über einen dreistufigen Ablauf:

1. **Input Guard:** Prüft die Benutzerfrage vor der Verarbeitung auf Richtlinienverstöße (z. B. Gehälter Dritter, Rechtsberatung, Rollen-Täuschung). Bei einem Verstoß wird die Anfrage sofort mit `BLOCK` abgelehnt.
2. **Core LLM:** Generiert eine hilfsbereite Antwort im Rahmen der betrieblichen Richtlinien.
3. **Output Guard & Re-Ask-Schleife:** Kontrolliert die generierte Antwort vor der Auslieferung. Verstößt die Antwort gegen Richtlinien, wird dem LLM das konkrete Feedback übermittelt, um die Antwort in bis zu 2 Korrekturschleifen (`max_attempts_llm_check = 2`) nachzubessern.

Für alle 3 Stufen wird standardmäßig das Modell **`gpt-4o-mini`** eingesetzt.

---

## 📁 Projektstruktur

```text
Guardrails_Projekt/
├── src/
│   ├── __init__.py
│   ├── main.py          # Orchestrierung, Core-LLM & Re-Ask-Logik
│   ├── validator.py     # Input- und Output-Guardrails
│   └── schemas.py       # Pydantic-Datenmodelle & Enums
├── tests/
│   ├── __init__.py
│   ├── test_cases.py    # Testdatensatz mit HR-Szenarien
│   ├── test_guard.py    # Testdatei für HR_Guard
│   ├── test_unprotected.py # Testdatei für Ablauf ohne Guard
    └── test_results.py  # Ergebnisse der Tests
├── .env.example         # Vorlage für Umgebungsvariablen
├── docs/
│   └── evaluation.md    # Auswertung der Testdaten
├── .gitignore
├── requirements.txt     # Python-Abhängigkeiten
├── README.md
└── DESIGN.md            # Architektur und Entscheidungen
```

---

## Installation & Setup

### 1. Repository klonen
```sh
git clone [https://github.com/fatihkutlu2024/Guardrails_Projekt.git](https://github.com/fatihkutlu2024/Guardrails_Projekt.git)
cd Guardrails_Projekt
```

### 2. Virtuelle Umgebung erstellen & aktivieren

**Mit Standard-Python:**
```sh
python -m venv .venv
# Linux / macOS:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\activate
```

**Oder mit uv:**
```sh
uv venv
.venv\Scripts\activate
```

### 3. Abhängigkeiten installieren
```sh
pip install -r requirements.txt
# oder mit uv:
uv pip install -r requirements.txt
```

### 4. API-Key konfigurieren
Erstelle eine `.env`-Datei im Hauptverzeichnis (orientiere dich an `.env.example`):
```env
OPENAI_API_KEY=dein-openai-api-key-hier
```

---

## Verwendung & Tests

### Einzelne Anfrage ausführen
```sh
python -m src.main
# mit uv:
uv run python -m src.main
```

### Testsuite mit Ergebnistabelle ausführen
Führt alle definierten Testfälle aus und visualisiert die Validierungsergebnisse in einer übersichtlichen Terminal-Tabelle:

```sh
python -m tests.test_guard
# mit uv:
uv run python -m tests.test_guard
```


## Weitere Dokumentation

*   **Architektur & Trade-offs:** Eine detaillierte Begründung meiner Designentscheidungen, der Wahl der HR-Domäne sowie eine Diskussion der Kompromisse zwischen Latenz und Kosten findest du in der [DESIGN.md](DESIGN.md).
*   **Testergebnisse:** Die Testergebnisse aller 11 Szenarien findest du in [test_results.md](tests/test_results.md).
*   **Evaluierung der Ergebnsse:** Die Evaluierung der Ergebnisse findest du in [evaluation.md](docs/evaluation.md).