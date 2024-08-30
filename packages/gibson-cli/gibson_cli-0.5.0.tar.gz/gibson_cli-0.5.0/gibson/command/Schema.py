import sys

from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.core.Colors import argument, command, hint, subcommand
from gibson.core.TimeKeeper import TimeKeeper
from gibson.dev.Dev import Dev


class Schema(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()

        self.configuration.ensure_project()
        entity = self.memory.recall_stored_entity(sys.argv[2])
        if entity is None:
            self.conversation.not_sure_no_entity(
                self.configuration.project.name, sys.argv[2]
            )
            exit(1)

        time_keeper = TimeKeeper()

        cli = Cli(self.configuration)
        response = cli.code_schemas([entity["name"]])

        Dev(self.configuration).schema(
            response["code"][0]["entity"]["name"], response["code"][0]["definition"]
        )

        print(response["code"][0]["definition"])
        time_keeper.display()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {command(self.configuration.command)} {subcommand('schema')} {argument('[entity name]')} {hint('write the schema code for an entity')}\n"
        )
        self.conversation.newline()
        exit(1)
