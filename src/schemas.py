from enum import Enum
from pydantic import BaseModel, Field


class GuardAction(str, Enum):
    PASS = "PASS"
    BLOCK = "BLOCK"


# 1. Für den Input-Guard (Vorab-Prüfung der Frage)
class InputGuardDecision(BaseModel):
    action: GuardAction = Field(description="Entscheidung: PASS (erlaubt) oder BLOCK (verboten)")
    reason: str = Field(default="", description="Kurze Begründung, falls die Frage geblockt wurde (leer bei PASS)")


# 2. Für den Output-Guard (Prüfung der Antwort mit Korrekturhinweis)
class OutputGuardDecision(BaseModel):
    action: GuardAction = Field(description="Entscheidung: PASS (erlaubt) oder BLOCK (verboten)")
    reason: str = Field(default="", description="Konkreter Hinweis, was korrigiert werden muss (leer bei PASS)")