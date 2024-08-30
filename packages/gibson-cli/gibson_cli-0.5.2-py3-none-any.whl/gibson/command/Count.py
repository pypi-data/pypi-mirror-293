import sys

from gibson.command.BaseCommand import BaseCommand
from gibson.core.Colors import arguments, command, hint, subcommand


class Count(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3 or sys.argv[2] not in ["last", "stored"]:
            self.usage()

        self.configuration.ensure_project()

        if sys.argv[2] == "last":
            count = 0
            if self.memory.last is not None:
                count = len(self.memory.last["entities"])

            print(count)
        elif sys.argv[2] == "stored":
            count = 0
            if self.memory.entities is not None:
                count = len(self.memory.entities)

            print(count)
        else:
            raise NotImplementedError

        return self

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {command(self.configuration.command)} {subcommand('count')} {arguments(['last', 'stored'])} {hint('display the number of entities')}\n"
        )
        self.conversation.newline()
        exit(1)
