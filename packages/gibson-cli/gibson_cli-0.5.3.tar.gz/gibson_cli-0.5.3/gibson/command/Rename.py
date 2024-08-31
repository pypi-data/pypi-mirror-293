import sys

import gibson.core.Colors as Colors
from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.command.rewrite.Rewrite import Rewrite


class Rename(BaseCommand):
    def execute(self):
        if len(sys.argv) != 4:
            self.usage()

        self.configuration.ensure_project()
        self.configuration.display_project()

        if self.memory.recall_entity(sys.argv[2]) is None:
            self.conversation.type(
                f'Nothing renamed, did not find entity named "{sys.argv[2]}".\n'
            )
            self.conversation.newline()
            return self

        if self.memory.recall_entity(sys.argv[3]) is not None:
            self.conversation.type(
                f'Cannot rename to "{sys.argv[3]}" because that entity already exists.\n'
            )
            self.conversation.newline()
            return self

        cli = Cli(self.configuration)

        last = self.memory.recall_last()
        if last is not None:
            response = cli.modeler_entity_rename(
                self.configuration.project.modeler.version,
                last["entities"],
                sys.argv[2],
                sys.argv[3],
            )

            self.memory.remember_last({"entities": response["entities"]})

        stored = self.memory.recall_entities()
        if stored is not None:
            response = cli.modeler_entity_rename(
                self.configuration.project.modeler.version,
                stored,
                sys.argv[2],
                sys.argv[3],
            )

            self.memory.remember_entities(response["entities"])

        self.conversation.type(f"[Renamed] {sys.argv[2]} -> {sys.argv[3]}\n")
        self.conversation.newline()

        Rewrite(self.configuration, header="Refactoring").write()

        self.conversation.newline()

        return self

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command)} {Colors.subcommand('rename')} {Colors.argument('[current]')} {Colors.input('[new]')} {Colors.hint('rename an entity')}\n"
        )
        self.conversation.newline()
        exit(1)
