"""
Database migrations. Safe to re-run — each statement uses IF NOT EXISTS / IF EXISTS guards.

Run with:
    uv run python migrate.py
"""

from sqlalchemy import text

from app import app, db

MIGRATIONS = [
    # 001 — add is_active to users (default TRUE so existing rows are active)
    """
    ALTER TABLE users
    ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE
    """,
]

with app.app_context():
    with db.engine.connect() as conn:
        for i, sql in enumerate(MIGRATIONS, start=1):
            conn.execute(text(sql.strip()))
            conn.commit()
            print(f"  [{i:03}] OK")

    print(f"\nMigrations complete ({len(MIGRATIONS)} applied).")
