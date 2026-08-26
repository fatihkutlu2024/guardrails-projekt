# Evaluation & Reflexion

Die vollständigen Testergebnisse und tabellarischen Auswertungen beider Testläufe (ungeschützt vs. geschützt) sind in **`tests/test_results.md`** dokumentiert.

---

## 1. Vergleich: Ungeschützte Baseline vs. Guardrail-System

Beim Testen des ungeschützten Core-LLMs (`gpt-4o-mini` nur mit System-Prompt) und dem Vergleich mit der Guardrail-Pipeline fallen zentrale Unterschiede auf:

* **Fehlende Maschinenlesbarkeit ohne Guards:** Das ungeschützte Modell verweigert bei manchen Verstößen zwar die Antwort als Freitext, liefert dem Backend aber keinen verlässlichen Status. Das System kann so nicht programmatisch entscheiden, ob ein Verstoß vorliegt.
* **Token-Verschwendung im ungeschützten Zustand:** Bei Datenabfragen oder Jailbreak-Versuchen formuliert das ungeschützte Modell oft lange Entschuldigungen und Erklärungen. Der `Input Guard` hingegen fängt unzulässige Prompts sofort vorab ab und spart dadurch Rechenzeit und API-Tokens. Im Falle einer angebundenen Datenbank, würde vorher auch kein Aufruf dieser stattfinden und somit Ressourcen (RAG-Prozess) sparen.
* **Erfolgreiche Erkennung mit Guards:** Alle 9 unzulässigen Angriffs- und Fehlbedienungsszenarien (Datenlecks, rechtliche Zusagen, Jailbreaks) wurden zuverlässig mit `BLOCK` gestoppt.

### Warum 100 % Erfolgsquote ohne Guardrail trotzdem problemantisch ist

Beim Baseline-Test hat auch das ungeschützte Modell alle 11 Anfragen inhaltlich passend beantwortet bzw. abgelehnt. Das liegt vor allem am guten internen Sicherheits-Alignment von `gpt-4o-mini` sowie dem bereits detaillierten System-Prompt. 

Trotzdem zeigt dieser Vergleich deutlich, warum man sich in Produktion **nicht allein auf den System-Prompt verlassen darf**:

* **Unzuverlässiger Freitext statt programmatischer Kontrolle:** 
  Das ungeschützte Modell antwortet als reiner Freitext (z. B. *„Es tut mir leid, aber ich kann keine Gehälter nennen...“*). Im Code gibt es dabei keinen sauberen Bool/Enum-Wert (`BLOCK` oder `PASS`). Ein Backend kann diesen Freitext nicht zuverlässig abfangen, protokollieren oder in automatisierten Sicherheits-Pipelines weiterverarbeiten.
* **Keine Garantie bei raffinierten Angriffen:** 
  Dass der System-Prompt bei diesen 11 Basistests gehalten hat, ist kein Sicherheitsnachweis. Bei mehrstufigen Jailbreaks könnten reine System-Prompts schneller einbrechen.
* **Unnötige Token-Kosten bei Angriffen:** 
  Das ungeschützte Modell generiert bei jeder böswilligen Anfrage eine ausführliche, höfliche Entschuldigung. Der `Input Guard` hingegen fängt die Anfrage deterministisch vor dem eigentlichen Hauptmodell ab und spart teure Tokens für die Textgenerierung.
* **Fehlendes Sicherheitsnetz für Modell-Halluzinationen (Output Guard):** 
  Sollte das Core-LLM doch einmal halluzinieren und vertrauliche Daten erfinden oder falsche Zusagen treffen, gibt es ohne Output-Guard keine zweite Instanz, die die Antwort vor der Auslieferung an den Nutzer abfängt und korrigiert (Re-Ask).

---

## 3. Kritische Reflexion & Grenzen des Systems

Trotz des 11/11-Testerfolgs gibt es konzeptionelle Grenzen, die für einen echten Produktiveinsatz beachtet werden müssen:

* **Kontextlosigkeit (Single-Turn):** Aktuell wird jeder Prompt isoliert bewertet. Angriffe, die über mehrere Chat-Nachrichten hinweg aufgebaut werden (z. B. sukzessives Ausfragen), erfordern für die Zukunft eine Validierung des gesamten Session-Kontexts.
* **Statische Testsuite:** 11 Testfälle bieten eine solide Basis für den Prototyp, decken aber nicht jeden Edge Case ab. In Produktion müsste die Tests weiter erweitert werden.