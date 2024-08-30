import typer

from sonarcloud_report.generate_sonarcloud_project_report import (
    generate_sonarcloud_project_report_file,
)
from sonarcloud_report.tools import must_get_env_var
from sonarcloud_report.__init__ import __version__


cli = typer.Typer()


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
):
    if ctx.invoked_subcommand is None:
        generate_report()


@cli.command()
def generate_report():
    typer.echo("SonarCloud report generation started")
    generate_sonarcloud_project_report_file(
        project_name=must_get_env_var("CI_PROJECT_NAME"),
        commit_id=must_get_env_var("CI_COMMIT_SHA"),
        sonar_token=must_get_env_var("SONAR_TOKEN"),
    )
    typer.echo("SonarCloud report generation finished")
