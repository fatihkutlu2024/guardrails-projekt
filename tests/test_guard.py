from src.main import main
from tests.test_cases import HR_TEST_CASES
from rich.console import Console
from rich.table import Table


console = Console()

def run_tests():
    # Formatierte Tabelle anlegen
    table = Table(title="HR Guardrails Test Suite", show_lines=True)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Prompt", style="white")
    table.add_column("Erwartet", justify="center")
    table.add_column("Erhalten", justify="center")
    table.add_column("Status", justify="center")

    passed_count = 0

    for case in HR_TEST_CASES:
        prompt = case["prompt"]
        expected = case["expected_action"]

        action, answer = main(prompt)
        actual = action.value
        print(answer)

        is_passed = (actual == expected)
        if is_passed:
            passed_count += 1
            status_display = "[bold green]PASS[/bold green]"
        else:
            status_display = "[bold red]FAIL[/bold red]"

        table.add_row(
            case["id"],
            prompt if len(prompt) < 60 else prompt[:57] + "...",
            f"[yellow]{expected}[/yellow]",
            f"[yellow]{actual}[/yellow]",
            status_display
        )

    # Tabelle ausgeben
    console.print(table)

    # Zusammenfassungs-Banner
    total = len(HR_TEST_CASES)
    if passed_count == total:
        console.print(f"\n[bold green]✔ Alle {total}/{total} Tests erfolgreich bestanden![/bold green]\n")
    else:
        console.print(f"\n[bold red]✖ {total - passed_count} von {total} Tests fehlgeschlagen.[/bold red]\n")

if __name__ == "__main__":
    run_tests()