import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gibson.command.BaseCommand import BaseCommand
from gibson.core.Colors import argument, command, hint, subcommand
from gibson.db.TableExceptions import TableExceptions


class Build(BaseCommand):
    def __build_datastore(self):
        self.configuration.display_project()

        db = create_engine(self.configuration.project.datastore.uri)
        session = sessionmaker(autocommit=False, autoflush=False, bind=db)()
        table_exceptions = TableExceptions().universal()

        self.conversation.type("Connected to datastore...\n")

        try:
            if self.configuration.project.datastore.type == "mysql":
                table_exceptions = TableExceptions().mysql()
                session.execute("set foreign_key_checks = 0")
                self.conversation.type("  foreign key checks have been disabled\n")

            tables = session.execute("show tables").all()
            if len(tables) > 0:
                self.conversation.type("  dropping existing entities\n")

                for table in tables:
                    if table not in table_exceptions:
                        self.conversation.type(f"    {table[0]}\n", delay=0.002)
                        session.execute(f"drop table if exists {table[0]}")

            self.conversation.type("  building entities\n")

            for entity in self.memory.entities:
                self.conversation.type(f"    {entity['name']}\n", delay=0.002)
                session.execute(entity["definition"])
        finally:
            if self.configuration.project.datastore.type == "mysql":
                session.execute("set foreign_key_checks = 1")
                self.conversation.type("  foreign key checks have been enabled\n")

        self.conversation.newline()

    def execute(self):
        if len(sys.argv) != 3 or sys.argv[2] != "datastore":
            self.usage()

        self.configuration.ensure_project()

        if self.memory.entities is None or len(self.memory.entities) == 0:
            self.no_entities()

        self.__build_datastore()

    def no_entities(self):
        self.configuration.display_project()
        self.conversation.type(
            "Ahhh man. I would love to but there aren't any entities.\n"
        )
        self.conversation.newline()
        exit(1)

    def usage(self):
        self.configuration.display_project()
        datastore_uri = (
            self.configuration.project.datastore.uri
            if self.configuration.project
            else ""
        )
        self.conversation.type(
            f"usage: {command(self.configuration.command)} {subcommand('build')} {argument('datastore')} {hint('build the datastore')} {datastore_uri}\n"
        )
        self.conversation.newline()
        exit(1)
