from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    # Bot token var
    bot_token: SecretStr
    # Group ID var
    group_id: SecretStr

    # Config file name and encoding
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

config = Settings()
