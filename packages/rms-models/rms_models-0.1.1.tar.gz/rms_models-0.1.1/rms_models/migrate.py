from alembic.config import Config
from alembic import command
import os


def run_migrations(connection_string: str):
    # Путь к конфигурации Alembic в вашей библиотеке
    alembic_cfg_path = os.path.join(
        os.path.dirname(__file__), "migrations", "alembic.ini"
    )

    # Настройка Alembic с использованием указанного connection_string
    alembic_cfg = Config(alembic_cfg_path)
    alembic_cfg.set_main_option("sqlalchemy.url", connection_string)

    # Применяем миграции
    command.upgrade(alembic_cfg, "head")
