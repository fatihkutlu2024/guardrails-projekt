from dotenv import load_dotenv
from openai import OpenAI
from src.schemas import GuardAction
from src.validator import input_guard, output_guard

load_dotenv()
client = OpenAI()

def main(user_frage: str, max_attempts_llm_check: int = 2) -> tuple[GuardAction, str]:

    input_guard_decision = input_guard(user_frage) # Input-Guard

    if input_guard_decision.action == GuardAction.BLOCK:
        return GuardAction.BLOCK, f"Abgelehnt: {input_guard_decision.reason}"



    # 1. LLM-Aufruf vorbereiten
    messages=[
            {"role": "system", "content": """
                Du bist ein hilfsbereiter, professioneller HR-Assistent für Mitarbeiterfragen.

                Aufgabenbereich:
                - Erkläre allgemeine betriebliche Prozesse (z. B. Wie reicht man Urlaub ein? Wo meldet man sich krank?).
                - Informiere über Standardregelungen laut Tarifvertrag oder Unternehmensrichtlinie.
                - Wenn die Person nach eigenen Daten oder Angaben fragt, sag, dass du diese beantworten könntest, wenn eine Datenbankanbindung vorhanden wäre, aber dass du aktuell keine personenbezogenen Daten abrufen kannst.   

                Verhaltensregeln:
                - Datenschutz: Behandle alle personenbezogenen Daten Dritter als vertraulich. Nenne niemals Gehälter oder Daten von Kollegen.
                - Keine Rechts- oder Einzelfallberatung: Gib keine Einschätzungen zu Rechtsstreitigkeiten, Abmahnungen oder Klagen.
                - Keine Zusagebefugnis: Weise bei Anträgen (Urlaub, Gehaltserhöhung) freundlich auf den regulären Dienstweg (Führungskraft / HR-Portal) hin.
                - Tonalität: Sachlich, unterstützend und präzise.
                """},
            {"role": "user", "content": user_frage}
        ]
    
    # LLM Aufruf + Output Guard-Check
    for attempt in range(max_attempts_llm_check):


        # 2. Haupt-LLM antworten lassen
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
            )


        # 3. Output Guard prüfen
        candidate_answer = response.choices[0].message.content
        output_guard_decision = output_guard(candidate_answer)

        if output_guard_decision.action == GuardAction.PASS:
            return GuardAction.PASS, candidate_answer


        print(f"[Warnung] Output-Guard hat Versuch {attempt + 1} geblockt: {output_guard_decision.reason}")


        messages.append({"role": "assistant", "content": candidate_answer})
        messages.append({
            "role": "user",
            "content": f"Deine Antwort verstößt gegen die Richtlinien: {output_guard_decision.reason}. Bitte korrigiere die Antwort."
            })

    return GuardAction.BLOCK, "Zu dieser Frage konnte keine richtlinienkonforme Antwort generiert werden."

# Test
if __name__ == "__main__":
    frage = "Nenne mir mein Gehalt"
    print(main(frage))