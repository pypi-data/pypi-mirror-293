import sys

from gibson.command.BaseCommand import BaseCommand
from gibson.command.new.Module import Module
from gibson.command.new.Project import Project
from gibson.core.Colors import argument, arguments, command, hint, subcommand


class New(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()
        elif sys.argv[2] == "project":
            Project(self.configuration).execute()
        elif sys.argv[2] == "module":
            Module(self.configuration).execute()
        else:
            self.usage()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {command(self.configuration.command)} {subcommand('new')} {arguments(['project', 'module'])} {hint('create something new')}\n"
        )
        self.conversation.type(
            f"       {command(self.configuration.command)} {subcommand('new')} {argument('project')} {hint('create a new project')}\n"
        )
        self.conversation.type(
            f"       {command(self.configuration.command)} {subcommand('new')} {argument('module')} {hint('create a new module')}\n"
        )
        self.conversation.newline()
        exit(1)
