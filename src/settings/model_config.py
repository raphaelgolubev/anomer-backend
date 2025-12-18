from pydantic_settings import SettingsConfigDict


class ModelConfig:
    """
    Определяет значения по умолчанию.
    Значения можно переопределять внутри наследника `BaseSettings`:
    ```python
    class ExampleSettings(BaseSettings):
        ...
        model_config = ModelConfig(env_prefix="EXAMPLE_", env_file="example.dev.env")
    ```

    Возвращает экземпляр `pydantic_settings.SettingsConfigDict` 
    """

    def __new__(cls, *args, **kwargs) -> SettingsConfigDict: # type: ignore
        config = SettingsConfigDict(
            extra="ignore",
            validate_default=False,
            case_sensitive=False,
            env_ignore_empty=True,
            env_file_encoding="utf-8",
            env_file=".env",
        )
        config.update(**kwargs) # type: ignore
        return config