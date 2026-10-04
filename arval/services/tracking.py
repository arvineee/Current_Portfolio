"""Visitor tracking: parse the request and log the visit (skips bots, admin, static)."""
import json
import urllib.request
from functools import lru_cache

from flask import request

from arval.repos import visitors

BOT_MARKERS = ('bot', 'crawler', 'spider', 'curl', 'wget', 'python-requests')


def parse_user_agent(ua):
    """Return (device, browser, os) strings from a User-Agent."""
    ul = (ua or '').lower()

    if any(x in ul for x in ('mobile', 'android', 'iphone')):
        device = 'mobile'
    elif 'tablet' in ul or 'ipad' in ul:
        device = 'tablet'
    else:
        device = 'desktop'

    if 'edg' in ul:
        browser = 'Edge'
    elif 'opr' in ul or 'opera' in ul:
        browser = 'Opera'
    elif 'chrome' in ul:
        browser = 'Chrome'
    elif 'firefox' in ul:
        browser = 'Firefox'
    elif 'safari' in ul:
        browser = 'Safari'
    else:
        browser = 'Other'

    if 'windows' in ul:
        os_name = 'Windows'
    elif 'android' in ul:
        os_name = 'Android'
    elif 'iphone' in ul or 'ipad' in ul:
        os_name = 'iOS'
    elif 'mac' in ul:
        os_name = 'macOS'
    elif 'linux' in ul:
        os_name = 'Linux'
    else:
        os_name = 'Other'
    return device, browser, os_name


@lru_cache(maxsize=2048)
def _lookup_location(ip):
    """(country, city) via ip-api.com's free tier. Cached per IP so repeat visits cost nothing."""
    if not ip or ip.startswith(('127.', '10.', '192.168.')) or ip == '::1':
        return 'Unknown', ''
    try:
        with urllib.request.urlopen(
                f'http://ip-api.com/json/{ip}?fields=country,city,status', timeout=2) as resp:
            data = json.loads(resp.read())
        if data.get('status') == 'success':
            return data.get('country', 'Unknown'), data.get('city', '')
    except Exception:
        pass
    return 'Unknown', ''


def real_ip():
    """Client IP behind PythonAnywhere's proxy."""
    return (request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
            or request.headers.get('X-Real-IP', '')
            or request.remote_addr or '')


def track_visit():
    if request.path.startswith(('/admin', '/static')):
        return
    ua = request.headers.get('User-Agent', '')
    if any(b in ua.lower() for b in BOT_MARKERS):
        return
    ip = real_ip()
    referrer = request.referrer or ''
    if referrer and request.host in referrer:      # ignore internal navigation
        referrer = ''
    country, city = _lookup_location(ip)
    device, browser, os_name = parse_user_agent(ua)
    visitors.log(request.path, ip, country, city, device, browser, os_name, referrer)
