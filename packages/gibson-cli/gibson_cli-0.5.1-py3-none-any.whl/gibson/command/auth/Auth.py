import sys

from gibson.command.auth.Login import Login
from gibson.command.auth.Logout import Logout
from gibson.command.BaseCommand import BaseCommand
from gibson.core.Colors import argument, command, hint, subcommand


class Auth(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()
        elif sys.argv[2] == "login":
            Login(self.configuration).execute()
        elif sys.argv[2] == "logout":
            Logout(self.configuration).execute()
        else:
            self.usage()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {command(self.configuration.command)} {subcommand('auth')} {argument('login')} {hint('login to Gibson')}\n"
        )
        self.conversation.type(
            f"   or: {command(self.configuration.command)} {subcommand('auth')} {argument('logout')} {hint('logout of Gibson')}\n"
        )
        self.conversation.newline()
        exit(1)
