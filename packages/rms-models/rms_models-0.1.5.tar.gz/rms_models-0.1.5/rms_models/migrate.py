# rms_models/migrate.py
from alembic.config import Config
from alembic import command
import sys

def run_migrations():
    if len(sys.argv) != 2:
        print("Usage: run-migrations <connection_string>")
        sys.exit(1)
    
    connection_string = sys.argv[1]
    
    # Инициализируем конфигурацию Alembic
    alembic_cfg = Config("rms_models/migrations/alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", connection_string)
    
    # Запускаем миграции
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_migrations()
