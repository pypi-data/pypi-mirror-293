from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.core.Colors import argument, arguments, command, hint, subcommand


class Module(BaseCommand):
    def execute(self):
        self.configuration.ensure_project()
        module_name = self.conversation.prompt_module()

        self.conversation.newline()
        self.conversation.type(f"Generating new module: {argument(module_name)}\n")

        cli = Cli(self.configuration)
        response = cli.modeler_module(
            self.configuration.project.modeler.version,
            self.configuration.project.description,
            module_name,
        )

        self.memory.remember_last(response)

        self.conversation.newline()
        self.conversation.type(
            f"The following entities were created in your {argument('last')} memory:\n"
        )

        for entity in response["entities"]:
            self.conversation.newline()
            print(entity["definition"])

        self.conversation.newline()
        self.conversation.type(f"If you want to persist these new entities run:\n")
        self.conversation.type(
            f"{command(self.configuration.command)} {subcommand('merge')}\n"
        )

        self.conversation.newline()
        self.conversation.type(
            f"Afterwards, you can modify any of these entities by running:\n"
        )
        self.conversation.type(
            f"{command(self.configuration.command)} {subcommand('modify')} {argument('[entity name]')} {input('[instructions]')}\n"
        )
