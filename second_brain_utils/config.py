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
    mask_private_at_export: bool = True
    private_ref_filler: str = "_ref not found_"
    private_section_filler: str = "_section not found_"
    private_section_start: str = "<PRIVATE>"
    private_section_end: str = "</PRIVATE>"
    # These options are currently only passed for the export command
    export_render_md_links: bool = True
    export_pop_properties: list[str] | None = None
    keep_tags: list[str] | None = None
    drop_tags: list[str] | None = None

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
