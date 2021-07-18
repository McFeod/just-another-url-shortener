from pydantic import BaseSettings, Field


class DBSettings(BaseSettings):
    host: str
    user: str
    name: str
    password: str
    port: int

    def prepare_db_url(self, driver: str) -> str:
        return f'postgresql+{driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'

    @property
    def dsn(self) -> str:
        return self.prepare_db_url('asyncpg')

    @property
    def alembic_dsn(self) -> str:
        return self.prepare_db_url('psycopg2')
    
    class Config:
        env_prefix = 'db_'


class AppSettings(BaseSettings):
    preferred_slug_length: int = Field(gt=1, le=12)
    short_domain: str


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()


settings = Settings()
