from alembic.config import Config
from alembic import command
import os
import sys


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


def main():
    if len(sys.argv) != 2:
        print("Usage: poetry run run-migrations <connection_string>")
        sys.exit(1)
    
    connection_string = sys.argv[1]
    run_migrations(connection_string)

