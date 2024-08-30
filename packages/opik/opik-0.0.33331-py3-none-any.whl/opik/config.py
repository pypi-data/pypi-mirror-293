from typing import Tuple, Any, Type, Dict, Literal, Optional

import pydantic_settings

from . import dict_utils

_SESSION_CACHE_DICT: Dict[str, Any] = {}


class CometConfig(pydantic_settings.BaseSettings):
    """
    Initializes every configuration variable with the first
    found value. The order of sources used:
    1. User passed values
    2. _SESSION_CACHE_DICT
    3. Environment variables
    4. Default values

    """

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="comet_")

    url_override: str = "http://localhost:5173/api"
    project_name: str = "Default Project"
    workspace: str = "default"
    api_key: Optional[str] = None
    default_flush_timeout: int = 60
    background_workers: int = 1
    console_logging_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = (
        "INFO"
    )
    file_logging_level: Optional[
        Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    ] = None
    logging_file: str = "comet.log"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[pydantic_settings.BaseSettings],
        init_settings: pydantic_settings.PydanticBaseSettingsSource,
        env_settings: pydantic_settings.PydanticBaseSettingsSource,
        dotenv_settings: pydantic_settings.PydanticBaseSettingsSource,
        file_secret_settings: pydantic_settings.PydanticBaseSettingsSource,
    ) -> Tuple[pydantic_settings.PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            pydantic_settings.InitSettingsSource(
                pydantic_settings.BaseSettings, _SESSION_CACHE_DICT
            ),
            env_settings,
        )


def update_session_config(key: str, value: Any) -> None:
    _SESSION_CACHE_DICT[key] = value


def get_from_user_inputs(**user_inputs: Any) -> CometConfig:
    cleaned_user_inputs = dict_utils.remove_none_from_dict(user_inputs)

    return CometConfig(**cleaned_user_inputs)
