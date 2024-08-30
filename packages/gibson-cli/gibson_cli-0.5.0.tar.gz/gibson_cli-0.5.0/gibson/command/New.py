import sys

from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.core.Colors import argument, command, hint, subcommand


class New(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()

        if sys.argv[2] != "project":
            self.usage()

        self.conversation.new_project(self.configuration)
        project_name = self.conversation.prompt_project()
        if project_name in self.configuration.settings:
            self.conversation.project_already_exists(project_name)
            exit(1)

        project_description = self.conversation.prompt_description(project_name)

        self.configuration.set_project_env(project_name)
        self.configuration.append_project_to_conf(project_name, project_description)

        self.conversation.configure_new_project(self.configuration)

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {command(self.configuration.command)} {subcommand('new')} {argument('project')} {hint('create a new project')}\n"
        )
        self.conversation.newline()
        exit(1)
