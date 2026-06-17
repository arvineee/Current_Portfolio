import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'projects.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables and seed projects from config if empty."""
    conn = get_db()

    # Projects table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            description TEXT    NOT NULL,
            tags        TEXT    NOT NULL DEFAULT '[]',
            url         TEXT    NOT NULL DEFAULT '#',
            github      TEXT    NOT NULL DEFAULT '',
            featured    INTEGER NOT NULL DEFAULT 0,
            sort_order  INTEGER NOT NULL DEFAULT 0
        )
    ''')

    # Visitors table
    conn.execute('''
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
        )
    ''')
    conn.commit()

    # Seed projects from config once
    count = conn.execute('SELECT COUNT(*) FROM projects').fetchone()[0]
    if count == 0:
        try:
            import config
            for i, p in enumerate(config.PROJECTS):
                conn.execute(
                    'INSERT INTO projects (title,description,tags,url,github,featured,sort_order) '
                    'VALUES (?,?,?,?,?,?,?)',
                    (p['title'], p['description'], json.dumps(p.get('tags', [])),
                     p.get('url', '#'), p.get('github', ''),
                     1 if p.get('featured') else 0, i)
                )
            conn.commit()
        except Exception:
            pass
    conn.close()


# ── PROJECTS CRUD ─────────────────────────────────────────────────────────────

def get_all_projects():
    conn = get_db()
    rows = conn.execute('SELECT * FROM projects ORDER BY sort_order ASC, id ASC').fetchall()
    conn.close()
    return [_proj(r) for r in rows]


def get_project(pid):
    conn = get_db()
    row = conn.execute('SELECT * FROM projects WHERE id=?', (pid,)).fetchone()
    conn.close()
    return _proj(row) if row else None


def create_project(title, description, tags, url, github, featured, sort_order=0):
    conn = get_db()
    cur = conn.execute(
        'INSERT INTO projects (title,description,tags,url,github,featured,sort_order) VALUES (?,?,?,?,?,?,?)',
        (title, description, json.dumps(tags), url, github, 1 if featured else 0, sort_order)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def update_project(pid, title, description, tags, url, github, featured, sort_order):
    conn = get_db()
    conn.execute(
        'UPDATE projects SET title=?,description=?,tags=?,url=?,github=?,featured=?,sort_order=? WHERE id=?',
        (title, description, json.dumps(tags), url, github, 1 if featured else 0, sort_order, pid)
    )
    conn.commit()
    conn.close()


def delete_project(pid):
    conn = get_db()
    conn.execute('DELETE FROM projects WHERE id=?', (pid,))
    conn.commit()
    conn.close()


def _proj(row):
    d = dict(row)
    d['tags'] = json.loads(d.get('tags', '[]'))
    d['featured'] = bool(d.get('featured', 0))
    return d


# ── VISITOR TRACKING ──────────────────────────────────────────────────────────

def log_visitor(path, ip, country, city, device, browser, os_name, referrer):
    from datetime import datetime, timezone
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db()
    conn.execute(
        'INSERT INTO visitors (timestamp,path,ip,country,city,device,browser,os,referrer) '
        'VALUES (?,?,?,?,?,?,?,?,?)',
        (ts, path, ip, country, city, device, browser, os_name, referrer)
    )
    conn.commit()
    conn.close()


def get_analytics(days=30):
    """Return all analytics data for the last N days."""
    conn = get_db()

    # Total visitors
    total = conn.execute(
        "SELECT COUNT(*) FROM visitors WHERE timestamp >= datetime('now', ?)",
        (f'-{days} days',)
    ).fetchone()[0]

    # Unique IPs
    unique = conn.execute(
        "SELECT COUNT(DISTINCT ip) FROM visitors WHERE timestamp >= datetime('now', ?)",
        (f'-{days} days',)
    ).fetchone()[0]

    # Page views breakdown
    pages = conn.execute(
        "SELECT path, COUNT(*) as cnt FROM visitors "
        "WHERE timestamp >= datetime('now', ?) "
        "GROUP BY path ORDER BY cnt DESC LIMIT 10",
        (f'-{days} days',)
    ).fetchall()

    # Top countries
    countries = conn.execute(
        "SELECT country, COUNT(*) as cnt FROM visitors "
        "WHERE timestamp >= datetime('now', ?) "
        "GROUP BY country ORDER BY cnt DESC LIMIT 10",
        (f'-{days} days',)
    ).fetchall()

    # Devices
    devices = conn.execute(
        "SELECT device, COUNT(*) as cnt FROM visitors "
        "WHERE timestamp >= datetime('now', ?) "
        "GROUP BY device ORDER BY cnt DESC",
        (f'-{days} days',)
    ).fetchall()

    # Browsers
    browsers = conn.execute(
        "SELECT browser, COUNT(*) as cnt FROM visitors "
        "WHERE timestamp >= datetime('now', ?) "
        "GROUP BY browser ORDER BY cnt DESC LIMIT 8",
        (f'-{days} days',)
    ).fetchall()

    # Top referrers
    referrers = conn.execute(
        "SELECT referrer, COUNT(*) as cnt FROM visitors "
        "WHERE timestamp >= datetime('now', ?) AND referrer != '' "
        "GROUP BY referrer ORDER BY cnt DESC LIMIT 10",
        (f'-{days} days',)
    ).fetchall()

    # Daily visits for chart (last 14 days)
    daily = conn.execute(
        "SELECT date(timestamp) as day, COUNT(*) as cnt FROM visitors "
        "WHERE timestamp >= datetime('now', '-14 days') "
        "GROUP BY day ORDER BY day ASC"
    ).fetchall()

    # Recent visitors (last 20)
    recent = conn.execute(
        "SELECT timestamp, path, country, city, device, browser, os, referrer "
        "FROM visitors ORDER BY id DESC LIMIT 20"
    ).fetchall()

    conn.close()
    return {
        'total': total,
        'unique': unique,
        'pages': [dict(r) for r in pages],
        'countries': [dict(r) for r in countries],
        'devices': [dict(r) for r in devices],
        'browsers': [dict(r) for r in browsers],
        'referrers': [dict(r) for r in referrers],
        'daily': [dict(r) for r in daily],
        'recent': [dict(r) for r in recent],
    }

