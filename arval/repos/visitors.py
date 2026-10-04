"""Visitor log + analytics queries."""
from datetime import datetime, timezone

from arval.database import connect


def log(path, ip, country, city, device, browser, os_name, referrer):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    with connect() as conn:
        conn.execute(
            'INSERT INTO visitors (timestamp,path,ip,country,city,device,browser,os,referrer) '
            'VALUES (?,?,?,?,?,?,?,?,?)',
            (ts, path, ip, country, city, device, browser, os_name, referrer))


def _top(conn, column, since, limit=None, where=''):
    """Group visitors by one of our own column names (never user input) and count."""
    sql = (f"SELECT {column}, COUNT(*) AS cnt FROM visitors "
           f"WHERE timestamp >= datetime('now', ?) {where} "
           f"GROUP BY {column} ORDER BY cnt DESC")
    if limit:
        sql += f' LIMIT {int(limit)}'
    return [dict(r) for r in conn.execute(sql, (since,)).fetchall()]


def analytics(days=30):
    since = f'-{days} days'
    with connect() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM visitors WHERE timestamp >= datetime('now', ?)", (since,)).fetchone()[0]
        unique = conn.execute(
            "SELECT COUNT(DISTINCT ip) FROM visitors WHERE timestamp >= datetime('now', ?)",
            (since,)).fetchone()[0]
        daily = conn.execute(
            "SELECT date(timestamp) AS day, COUNT(*) AS cnt FROM visitors "
            "WHERE timestamp >= datetime('now', '-14 days') GROUP BY day ORDER BY day ASC").fetchall()
        recent = conn.execute(
            'SELECT timestamp, path, country, city, device, browser, os, referrer '
            'FROM visitors ORDER BY id DESC LIMIT 20').fetchall()
        return {
            'total': total,
            'unique': unique,
            'pages': _top(conn, 'path', since, 10),
            'countries': _top(conn, 'country', since, 10),
            'devices': _top(conn, 'device', since),
            'browsers': _top(conn, 'browser', since, 8),
            'referrers': _top(conn, 'referrer', since, 10, "AND referrer != ''"),
            'daily': [dict(r) for r in daily],
            'recent': [dict(r) for r in recent],
        }
