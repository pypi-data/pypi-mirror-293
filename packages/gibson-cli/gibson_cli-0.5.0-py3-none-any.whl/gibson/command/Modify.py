import sys

from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.core.Colors import argument, command, hint, input, subcommand


class Modify(BaseCommand):
    def execute(self):
        if len(sys.argv) < 4:
            self.usage()

        self.configuration.ensure_project()
        entity = self.memory.recall_entity(sys.argv[2])
        if entity is None:
            self.conversation.not_sure_no_entity(
                self.configuration.project.name, sys.argv[2]
            )
            exit(1)

        cli = Cli(self.configuration)

        response = cli.modeler_entity_modify(
            self.configuration.project.modeler.version,
            self.configuration.project.description,
            entity,
            " ".join(sys.argv[3:]),
        )

        self.memory.remember_last(response)

        print(response["entities"][0]["definition"])

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {command(self.configuration.command)} {subcommand('modify')} {argument('[entity name]')} {input('[instructions]')} {hint('modify an entity with natural language instructions')}\n"
        )
        self.conversation.newline()
        exit(1)
