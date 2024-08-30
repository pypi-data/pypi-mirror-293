"""
Configuration settings for the application.

The configuration is loaded from a TOML file named "config.toml" in the current working directory.
The configuration is stored in a Settings object, which is a subclass of pydantic's BaseSettings.
The Settings object has the following attributes:

- database: a dictionary containing the database connection settings
- server: a dictionary containing the server settings
- auth: a dictionary containing the authentication settings
- cache: a dictionary containing the cache settings
- rate_limiting: a dictionary containing the rate limiting settings
- models: a list of dictionaries containing the model definitions

The Config class is used to configure the Settings object.
"""
import toml
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the application.
    """
    database: dict
    server: dict
    auth: dict
    cache: dict
    rate_limiting: dict
    models: list

    class Config:
        """
        Configuration for the Settings object.
        """
        env_file = ".env"

settings = Settings(**toml.load("config.toml"))

