from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_user: str
    db_name: str
    db_password: str

    def prepare_db_url(self, driver: str) -> str:
        return f'postgresql+{driver}://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'

    @property
    def db_dsn(self) -> str:
        return self.prepare_db_url('asyncpg')

    @property
    def alembic_dsn(self) -> str:
        return self.prepare_db_url('psycopg2')


settings = Settings()
