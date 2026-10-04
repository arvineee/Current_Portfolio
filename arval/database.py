"""SQLite connection helper, schema creation and the key/value settings table."""
import json
import sqlite3
from contextlib import contextmanager

import content

_db_path = None

SCHEMA = '''
CREATE TABLE IF NOT EXISTS projects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT    NOT NULL,
    tags        TEXT    NOT NULL DEFAULT '[]',
    url         TEXT    NOT NULL DEFAULT '#',
    github      TEXT    NOT NULL DEFAULT '',
    featured    INTEGER NOT NULL DEFAULT 0,
    sort_order  INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS visitors (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp  TEXT    NOT NULL,
    path       TEXT    NOT NULL DEFAULT '/',
    ip         TEXT    NOT NULL DEFAULT '',
    country    TEXT    NOT NULL DEFAULT 'Unknown',
    city       TEXT    NOT NULL DEFAULT '',
    device     TEXT    NOT NULL DEFAULT 'desktop',
    browser    TEXT    NOT NULL DEFAULT 'Unknown',
    os         TEXT    NOT NULL DEFAULT 'Unknown',
    referrer   TEXT    NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS orders (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    ref            TEXT    NOT NULL UNIQUE,
    plan_index     INTEGER NOT NULL,
    plan_name      TEXT    NOT NULL,
    list_price     INTEGER NOT NULL,
    amount         INTEGER NOT NULL,
    offer_title    TEXT    NOT NULL DEFAULT '',
    customer_name  TEXT    NOT NULL,
    email          TEXT    NOT NULL,
    phone          TEXT    NOT NULL,
    status         TEXT    NOT NULL DEFAULT 'pending',
    invoice_id     TEXT    NOT NULL DEFAULT '',
    checkout_id    TEXT    NOT NULL DEFAULT '',
    provider_state TEXT    NOT NULL DEFAULT '',
    failure_reason TEXT    NOT NULL DEFAULT '',
    created_at     TEXT    NOT NULL,
    paid_at        TEXT    NOT NULL DEFAULT ''
);
'''


@contextmanager
def connect():
    """Yield a connection that commits on success and always closes."""
    conn = sqlite3.connect(_db_path, timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(db_path):
    """Create tables (idempotent) and seed projects from content.py on first run."""
    global _db_path
    _db_path = db_path
    with connect() as conn:
        conn.executescript(SCHEMA)
        if conn.execute('SELECT COUNT(*) FROM projects').fetchone()[0] == 0:
            for i, p in enumerate(content.PROJECTS):
                conn.execute(
                    'INSERT INTO projects (title,description,tags,url,github,featured,sort_order) '
                    'VALUES (?,?,?,?,?,?,?)',
                    (p['title'], p['description'], json.dumps(p.get('tags', [])),
                     p.get('url', '#'), p.get('github', ''), 1 if p.get('featured') else 0, i))


# ── key/value settings ────────────────────────────────────────────────────────
def get_setting(key, default=None):
    with connect() as conn:
        row = conn.execute('SELECT value FROM settings WHERE key=?', (key,)).fetchone()
    return row['value'] if row else default


def set_setting(key, value):
    with connect() as conn:
        conn.execute(
            'INSERT INTO settings (key, value) VALUES (?, ?) '
            'ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key, value))
