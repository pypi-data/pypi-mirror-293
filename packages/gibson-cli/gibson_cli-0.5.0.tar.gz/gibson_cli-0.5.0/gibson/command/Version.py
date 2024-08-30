import requests

from gibson.command.BaseCommand import BaseCommand
from gibson.conf.Version import Version as VersionConf
from gibson.core.Colors import Color, colorize, command, option, subcommand


class Version(BaseCommand):
    def execute(self):
        try:
            r = requests.get("https://pypi.org/pypi/gibson-cli/json")
            latest_version = r.json()["info"]["version"]
        except:
            latest_version = VersionConf.num

        if latest_version != VersionConf.num:
            self.conversation.type(
                f"A new version of {command(self.configuration.command)} is available: {colorize(latest_version, Color.CYAN)}\n"
            )
            self.conversation.type(
                f"You are currently using version: {colorize(VersionConf.num, Color.VIOLET)}\n"
            )
            self.conversation.type(
                f"Please update to the latest version by running: {command('pip3')} {subcommand('install')} {option('--upgrade')} gibson-cli\n"
            )
        else:
            self.conversation.type(
                f"Nice! You are using the latest version of {command(self.configuration.command)}: {colorize(VersionConf.num, Color.CYAN)}\n"
            )

        self.conversation.newline()
        return True
