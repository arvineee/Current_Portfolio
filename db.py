import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'projects.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create table and seed from config.PROJECTS if empty."""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT    NOT NULL,
            description TEXT   NOT NULL,
            tags       TEXT    NOT NULL DEFAULT '[]',
            url        TEXT    NOT NULL DEFAULT '#',
            github     TEXT    NOT NULL DEFAULT '',
            featured   INTEGER NOT NULL DEFAULT 0,
            sort_order INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()

    count = conn.execute('SELECT COUNT(*) FROM projects').fetchone()[0]
    if count == 0:
        try:
            import config
            for i, p in enumerate(config.PROJECTS):
                conn.execute(
                    'INSERT INTO projects '
                    '(title, description, tags, url, github, featured, sort_order) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (
                        p['title'],
                        p['description'],
                        json.dumps(p.get('tags', [])),
                        p.get('url', '#'),
                        p.get('github', ''),
                        1 if p.get('featured') else 0,
                        i,
                    )
                )
            conn.commit()
        except Exception:
            pass
    conn.close()


def get_all_projects():
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM projects ORDER BY sort_order ASC, id ASC'
    ).fetchall()
    conn.close()
    return [_to_dict(r) for r in rows]


def get_project(pid):
    conn = get_db()
    row = conn.execute('SELECT * FROM projects WHERE id=?', (pid,)).fetchone()
    conn.close()
    return _to_dict(row) if row else None


def create_project(title, description, tags, url, github, featured, sort_order=0):
    conn = get_db()
    cur = conn.execute(
        'INSERT INTO projects (title,description,tags,url,github,featured,sort_order) '
        'VALUES (?,?,?,?,?,?,?)',
        (title, description, json.dumps(tags), url, github, 1 if featured else 0, sort_order)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def update_project(pid, title, description, tags, url, github, featured, sort_order):
    conn = get_db()
    conn.execute(
        'UPDATE projects SET title=?,description=?,tags=?,url=?,github=?,featured=?,sort_order=? '
        'WHERE id=?',
        (title, description, json.dumps(tags), url, github, 1 if featured else 0, sort_order, pid)
    )
    conn.commit()
    conn.close()


def delete_project(pid):
    conn = get_db()
    conn.execute('DELETE FROM projects WHERE id=?', (pid,))
    conn.commit()
    conn.close()


def _to_dict(row):
    d = dict(row)
    d['tags'] = json.loads(d.get('tags', '[]'))
    d['featured'] = bool(d.get('featured', 0))
    return d

