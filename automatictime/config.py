# -*- coding: utf-8 -*-
from pathlib import Path

import marshmallow as ma
from piny import MarshmallowValidator, StrictMatcher, YamlLoader
import pkg_resources
# -*- coding: utf-8 -*-
import yaml

from automatictime.exceptions import ConfigError

# Could be any dot-separated package/module name or a "Requirement"
resource_package = __name__


class LogSchema(ma.Schema):
    level = ma.fields.String(required=True, default="INFO")
    file = ma.fields.String(default=Path.home().joinpath("Documents/automatictime/application.log"))

    def validate_level(self, value):
        if value not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ma.ValidationError("Invalid log-level. Please use DEBUG, INFO, WARNING, ERROR, CRITICAL")

    def validate_file(self, value):
        if not Path(value).is_file():
            raise ma.ValidationError("Invalid log-file path")


class TrueTimeSchema(ma.Schema):
    file = ma.fields.String()


class MocoAppSchema(ma.Schema):
    api_url = ma.fields.String(required=True)
    api_key = ma.fields.String(required=True)


class ContractSchema(ma.Schema):
    week_work_hours = ma.fields.Float(required=True)


class DurationSchema(ma.Schema):
    start = ma.fields.String()
    end = ma.fields.String()


class DaySchema(ma.Schema):
    work = ma.fields.Nested(DurationSchema)
    pause = ma.fields.Nested(DurationSchema)


class HoursSchema(ma.Schema):
    monday = ma.fields.Nested(DaySchema)
    tuesday = ma.fields.Nested(DaySchema)
    wednesday = ma.fields.Nested(DaySchema)
    thursday = ma.fields.Nested(DaySchema)
    friday = ma.fields.Nested(DaySchema)
    saturday = ma.fields.Nested(DaySchema)
    sunday = ma.fields.Nested(DaySchema)


class ConfigSchema(ma.Schema):
    mocoapp = ma.fields.Nested(MocoAppSchema)
    log = ma.fields.Nested(LogSchema)
    true_time = ma.fields.Nested(TrueTimeSchema)
    contract = ma.fields.Nested(ContractSchema)
    hours = ma.fields.Nested(HoursSchema)


class Config:

    CURRENT_CONFIG_VERSION = 1

    def __init__(self, config_file=None):
        self.config_file = config_file
        self.config = {}
        self.load_config()

    @staticmethod
    def generate(file):
        if file.exists():
            raise ConfigError("Config file already exists. Cant generate a new one")

        resource_path = '/'.join(('templates', 'config.yml'))  # Do not use os.path.join()

        with file.open("wb") as fobj:
            template = pkg_resources.resource_stream(resource_package, resource_path)
            fobj.write(template.read())

    def load_config(self):
        with self.config_file.open() as fobj:
            config_data = yaml.load(fobj)
            config_version = config_data.get("version")
            if config_version == Config.CURRENT_CONFIG_VERSION:
                self.config = YamlLoader(
                    path=self.config_file.resolve(),
                    matcher=StrictMatcher,
                    validator=MarshmallowValidator,
                    schema=ConfigSchema,
                    strict=True).load(many=False)
            else:
                raise ConfigError(f"Wrong Config Version. Required is {Config.CURRENT_CONFIG_VERSION}")
