import typer
import os


__DEFAULT_NAME = "node_1"
__DEFAULT_PATH = "."


class BaseTyper(typer.Typer):
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs, name="node-admin")


app = BaseTyper()
