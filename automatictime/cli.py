# -*- coding: utf-8 -*-
import argparse
import logging
from pathlib import Path

from automatictime.configmanager import ConfigManager
from automatictime.exceptions import ConfigError
from automatictime.http import HttpSession
from automatictime.projects import list_projects

log = logging.getLogger("automaticTime")


class Command:

    def __init__(self, parser=None):
        self.parser = parser
        if parser is None:
            self.parser = argparse.ArgumentParser()

    def add_arguments(self, parser=None):
        if parser is None:
            parser = self.parser
        parser.add_argument("-g", "--generate-config", action="store_true")
        parser.add_argument("-c", "--config-file", type=Path, default=Path.home().joinpath(".automatictime"))
        parser.add_argument('--raw', help='RAW JSON Response', action="store_true")
        parser.add_argument('--log-level', type=str, default='INFO')

        subparsers = parser.add_subparsers(dest='command')

        projects_parser = subparsers.add_parser('projects', help='List all available Projects')

        start_parser = subparsers.add_parser('start', help='Startzeitpunkt ermitteln und Setzen')
        end_parser = subparsers.add_parser('stop', help='Endzeitpunkt ermitteln und setzen')
        pause_parser = subparsers.add_parser('pause', help='Pause setzen')
        fix_pause_cmd = subparsers.add_parser('fix-pause', help='Beheben von fehlenden Pausenzeiten')
        fix_overtime_cmd = subparsers.add_parser('fix-overtime', help='Beheben von Überstunden')

        self.add_projects_arguments(projects_parser)
        self.add_start_arguments(start_parser)
        self.add_end_arguments(end_parser)
        self.add_pause_arguments(pause_parser)
        self.add_fix_pause_arguments(fix_pause_cmd)
        self.add_fix_overtime_arguments(fix_overtime_cmd)

    def add_projects_arguments(self, parser=None):
        if parser is None:
            parser = self.parser
        parser.add_argument('--list', help='List all Projects', action="store_true")
        parser.add_argument('--filter', help='JSON Filter Expression')

    def add_start_arguments(self, parser=None):
        if parser is None:
            parser = self.parser
        parser.add_argument('--time', type=str, help='Startzeitpunkt (HH:MM)')
        parser.add_argument('--date', type=str, help='Startdatum (YYYY-MM-DD)')

    def add_end_arguments(self, parser=None):
        if parser is None:
            parser = self.parser
        parser.add_argument('--time', type=str, help='Endzeitpunkt (HH:MM)')
        parser.add_argument('--date', type=str, help='Enddatum (YYYY-MM-DD)')

    def add_pause_arguments(self, parser=None):
        if parser is None:
            parser = self.parser
        parser.add_argument('--time', type=str, help='Pausenzeitpunkt (HH:MM)')
        parser.add_argument('--date', type=str, help='Pausendatum (YYYY-MM-DD)')

    def add_fix_pause_arguments(self, parser=None):
        if parser is None:
            parser = self.parser
        parser.add_argument('--date', type=str, help='Startdatum (YYYY-MM-DD)')
        parser.add_argument('--duration', type=int, help='Pausenzeit (Minuten)')
        parser.add_argument('--time-slot', type=str, help="Zeitslot in der eine Pause genommen werden kann. (11:00-14:30)")

    def add_fix_overtime_arguments(self, parser=None):
        if parser is None:
            parser = self.parser
        parser.add_argument('--date', type=str, help='Startdatum (YYYY-MM-DD)')
        parser.add_argument('--day-distribution', help='Erlaube verteilung der Überstunden auf die Nachfolgenden wochentage')

    def parse(self, parser=None):
        if parser is None:
            parser = self.parser
        return parser.parse_args()

    def handle(self, options):

        if options.log_level:
            logging.basicConfig(level=getattr(logging, options.log_level))

        if options.config_file.exists() and options.generate_config:
            log.error("ConfigManager file already exists")
            raise ConfigError("ConfigManager file already exists")

        elif options.generate_config and not options.config_file.exists():
            ConfigManager.generate(options.config_file)
            return

        if not options.config_file.is_file():
            log.error("ConfigManager file not found")
            raise ConfigError("ConfigManager file not found")

        config_mgr = ConfigManager(options.config_file)
        config_mgr.update_by_args(options)

        http = HttpSession("mocoapp", config_mgr.config, options)

        if options.command == "projects":
            list_projects(config_mgr.config, options, http)


if __name__ == "__main__":
    cmd = Command()
    cmd.add_arguments()
    options = cmd.parse()
    cmd.handle(options)
