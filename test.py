import guardrails
from guardrails import Guard
# Neuer, empfohlener Import-Pfad (vermeidet die DeprecationWarning)
from guardrails_ai.regex_match import RegexMatch

# Guard initialisieren
guard = Guard().use(
    RegexMatch(
        regex=r"^Hallo.*",  # Erlaubt alles, was mit "Hallo" beginnt
        on_fail="exception",
    )
)

print("--- Test 1: Gültige Eingabe ---")
try:
    res1 = guard.validate("Hallo Welt")
    print(f"Erfolgreich validiert: {res1.validation_passed}")
    print(f"Ausgabe: {res1.validated_output}")
except Exception as e:
    print(f"Fehler in Test 1: {e}")

print("\n--- Test 2: Ungültige Eingabe ---")
try:
    res2 = guard.validate("Guten Tag Welt")
    print(f"Erfolgreich: {res2.validated_output}")
except Exception as e:
    print(f"Erwarteter Validierungsfehler abgefangen: {e}")