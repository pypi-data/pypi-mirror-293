import re
import sys

from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.core.Colors import command, hint, input, subcommand


class Module(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()

        self.configuration.ensure_project()
        if not re.search("^[a-z0-9]+$", sys.argv[2]):
            self.configuration.display_project()
            self.conversation.type("[module name] should only contain ^[a-z0-9]+$.\n\n")
            return True

        cli = Cli(self.configuration)

        response = cli.modeler_module(
            self.configuration.project.modeler.version,
            self.configuration.project.description,
            sys.argv[2],
        )

        self.memory.remember_last(response)

        for entity in response["entities"]:
            print(entity["definition"])
            self.conversation.newline()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {command(self.configuration.command)} {subcommand('module')} {input('[module name]')} {hint('create a new module for this project')}\n"
        )
        self.conversation.newline()
        exit(1)
