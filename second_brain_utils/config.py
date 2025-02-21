import os
from datetime import datetime

from pydantic_settings import (
    BaseSettings,
    CliSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)


class JobConfig(BaseSettings):
    source_directory: str
    target_directory: str
    ref_dt: datetime | None = None

    model_config = SettingsConfigDict(yaml_file=os.getenv("SECOND_BRAIN_UTILS_PARSER_CONF", "config/example.yaml"))

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            CliSettingsSource(settings_cls, cli_parse_args=True),
            env_settings,
            YamlConfigSettingsSource(settings_cls),
            init_settings,
        )
