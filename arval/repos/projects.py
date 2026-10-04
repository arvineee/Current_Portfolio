"""Portfolio projects CRUD."""
import json

from arval.database import connect


def _row(r):
    d = dict(r)
    d['tags'] = json.loads(d.get('tags') or '[]')
    d['featured'] = bool(d.get('featured'))
    return d


def all_projects():
    with connect() as conn:
        rows = conn.execute('SELECT * FROM projects ORDER BY sort_order ASC, id ASC').fetchall()
    return [_row(r) for r in rows]


def get(pid):
    with connect() as conn:
        row = conn.execute('SELECT * FROM projects WHERE id=?', (pid,)).fetchone()
    return _row(row) if row else None


def create(title, description, tags, url, github, featured, sort_order=0):
    with connect() as conn:
        cur = conn.execute(
            'INSERT INTO projects (title,description,tags,url,github,featured,sort_order) '
            'VALUES (?,?,?,?,?,?,?)',
            (title, description, json.dumps(tags), url, github, int(featured), sort_order))
        return cur.lastrowid


def update(pid, title, description, tags, url, github, featured, sort_order):
    with connect() as conn:
        conn.execute(
            'UPDATE projects SET title=?,description=?,tags=?,url=?,github=?,featured=?,sort_order=? '
            'WHERE id=?',
            (title, description, json.dumps(tags), url, github, int(featured), sort_order, pid))


def delete(pid):
    with connect() as conn:
        conn.execute('DELETE FROM projects WHERE id=?', (pid,))
