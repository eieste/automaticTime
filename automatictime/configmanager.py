# -*- coding: utf-8 -*-
from pathlib import Path

import marshmallow as ma
from piny import MarshmallowValidator, StrictMatcher, YamlLoader
from piny.validators import LoadedData
import pkg_resources

from automatictime.exceptions import ConfigError

# -*- coding: utf-8 -*-

# Could be any dot-separated package/module name or a "Requirement"
resource_package = __name__


class CustomMarshmallowValidator(MarshmallowValidator):

    def load(self, data: LoadedData, **params):
        try:
            return self.schema(**self.schema_params).load(data, **params)
        except Exception as e:
            raise ma.ValidationError(origin=e, reason=str(e))


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
    max_day_work_hours = ma.fields.Float(required=True)


class DurationSchema(ma.Schema):
    start = ma.fields.String()
    end = ma.fields.String()


class DaySchema(ma.Schema):
    work = ma.fields.Nested(DurationSchema)
    pause = ma.fields.Nested(DurationSchema)


class HoursSchema(ma.Schema):
    monday = ma.fields.Nested(DaySchema, allow_none=True)
    tuesday = ma.fields.Nested(DaySchema, allow_none=True)
    wednesday = ma.fields.Nested(DaySchema, allow_none=True)
    thursday = ma.fields.Nested(DaySchema, allow_none=True)
    friday = ma.fields.Nested(DaySchema, allow_none=True)
    saturday = ma.fields.Nested(DaySchema, allow_none=True)
    sunday = ma.fields.Nested(DaySchema, allow_none=True)


class ConfigSchema(ma.Schema):
    version = ma.fields.Integer(required=True)
    mocoapp = ma.fields.Nested(MocoAppSchema)
    log = ma.fields.Nested(LogSchema)
    true_time = ma.fields.Nested(TrueTimeSchema)
    contract = ma.fields.Nested(ContractSchema)
    hours = ma.fields.Nested(HoursSchema)


class ConfigManager:

    CURRENT_CONFIG_VERSION = 1

    def __init__(self, config_file=None):
        self.config_file = config_file
        self.config = {}
        self.load_config()

    @staticmethod
    def generate(file):
        if file.exists():
            raise ConfigError("ConfigManager file already exists. Cant generate a new one")

        resource_path = '/'.join(('templates', 'config.yml'))  # Do not use os.path.join()

        with file.open("wb") as fobj:
            template = pkg_resources.resource_stream(resource_package, resource_path)
            fobj.write(template.read())

    def load_config(self):
        self.config = YamlLoader(
            path=self.config_file.resolve(), matcher=StrictMatcher, validator=CustomMarshmallowValidator, schema=ConfigSchema).load()
        if self.config.get("version") != 1:
            raise ConfigError("Unsupported config version")

    def update_by_args(self, options):
        self.config["log"]["level"] = options.log_level
