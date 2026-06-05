# alembic/env.py
"""
Alembic environment configuration.

Key integrations:
1. Reads DATABASE_URL from the app's Settings (which reads from .env).
2. Sets target_metadata to Base.metadata so autogenerate works.
3. Overrides the sqlalchemy.url in alembic.ini so you only manage the
   database URL in one place (.env), not two places.
"""

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ── Make the project root importable ─────────────────────────────────────────
# Adds the project root (one level above alembic/) to sys.path so that
# `from app.xxx import yyy` imports work when running `alembic` commands.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ── Import application settings and ALL models ────────────────────────────────
# Importing `settings` gives us the DATABASE_URL from .env.
# Importing `app.models` triggers all model registrations on Base.metadata —
# this is what makes autogenerate detect the tables.
from app.core.config import settings   # noqa: E402
import app.models                      # noqa: E402  — registers all ORM models
from app.models.base import Base       # noqa: E402

# ── Alembic Config object ─────────────────────────────────────────────────────
config = context.config

# Set up Python logging as defined in alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ── Override the DB URL from .env (single source of truth) ───────────────────
# This replaces the placeholder `sqlalchemy.url` in alembic.ini at runtime.
# Alembic uses a synchronous URL; asyncpg is NOT supported here.
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# ── Tell Alembic which metadata to compare against ───────────────────────────
# This is what enables `alembic revision --autogenerate` to diff your models
# vs the current database schema and generate the migration script for you.
target_metadata = Base.metadata


# ── Offline migration mode ────────────────────────────────────────────────────
def run_migrations_offline() -> None:
    """
    Run migrations without a live database connection.
    Generates raw SQL that can be applied manually.
    Useful for auditing or applying migrations in restricted environments.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ── Online migration mode ─────────────────────────────────────────────────────
def run_migrations_online() -> None:
    """
    Run migrations with a live database connection.
    This is the default mode used when you run `alembic upgrade head`.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # Don't pool connections during migrations
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,      # Detect column type changes
            compare_server_default=True,  # Detect server_default changes
        )

        with context.begin_transaction():
            context.run_migrations()


# ── Entry point ───────────────────────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
