import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from src.utils.settings import settings
from src.utils.db import Base

# Import all models explicitly to register them with Base.metadata before migrations
from src.user.models import UserModel 
from src.rag.models import DocumentModel, ChatHistoryModel 

# Initialize Alembic Config
config = context.config

# Setup Python Logging natively via Alembic's ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.env")

# Bind Database URL securely from Pydantic Settings (not hardcoded in ini)
config.set_main_option("sqlalchemy.url", settings.DB_CONNECTION)

# Set the metadata target for autogenerate support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    This configures the context with just a URL and not an Engine.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()
        logger.info("Offline migrations executed successfully.")

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    In this scenario we create a standard SQLAlchemy Engine.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True,          # Essential for detecting column type modifications
            compare_server_default=True # Essential for detecting default value modifications
        )

        with context.begin_transaction():
            context.run_migrations()
            logger.info("Online migrations executed successfully.")

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
