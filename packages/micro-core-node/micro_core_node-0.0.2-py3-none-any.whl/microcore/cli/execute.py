import typer
from microcore.cli.commands import create_node, dockerize

app = typer.Typer()

app.command()(create_node.create_project)

if __name__ == "__main__":
    app()
