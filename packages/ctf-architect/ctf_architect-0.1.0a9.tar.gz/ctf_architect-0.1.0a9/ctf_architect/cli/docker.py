from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Confirm

from ctf_architect.core.challenge import is_challenge_repo
from ctf_architect.core.compose import create_compose_files, get_compose_file

console = Console()


docker_app = typer.Typer()


@docker_app.callback()
def callback():
    """
    Commands to manage challenge services in the CTF repo.
    """
    console.print(
        ':warning: [bold]WARNING:[/bold] The "docker" command has been replaced with the "compose" command and will be removed in a future version.',
        style="bright_yellow",
    )


@docker_app.command("generate")
def docker_generate(
    force: bool = typer.Option(
        False, "--force", "-f", help="Force generation of docker compose file."
    ),
):
    """
    Generate compose files for all challenges.
    """

    if not is_challenge_repo():
        console.print(
            "Not a valid challenge repo. Are you in the right directory?",
            style="bright_red",
        )
        return

    if not force and get_compose_file(Path.cwd()):
        if not Confirm.ask(
            "This will overwrite the current compose file. Do you want to continue?"
        ):
            return

    try:
        create_compose_files()
    except Exception as e:
        console.print_exception(show_locals=True)
        console.print(
            f"An error occurred while generating the compose files: {e}",
            style="bright_red",
        )
        return
    else:
        console.print("Compose files generated successfully!", style="bright_green")
