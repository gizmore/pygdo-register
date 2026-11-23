"""Validate registration return targets before sending a Location header."""
from urllib.parse import urlsplit

from gdo.base.Application import Application


def safe_return_path(value):
    if not isinstance(value, str) or not value or any(ord(c) < 32 or ord(c) == 127 for c in value) or '\\' in value:
        return None
    try:
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc:
            if parsed.scheme not in ('http', 'https') or parsed.username or parsed.password:
                return None
            if parsed.hostname != Application.config('core.domain'):
                return None
            # Same host, but do not redirect to an arbitrary service on that host.
            if parsed.port not in (None, int(Application.config('core.port') or (443 if parsed.scheme == 'https' else 80))):
                return None
        elif not value.startswith('/') or value.startswith('//'):
            return None
        path = parsed.path or '/'
        if not path.startswith('/') or path.startswith('//'):
            return None
        return path + (('?' + parsed.query) if parsed.query else '') + (('#' + parsed.fragment) if parsed.fragment else '')
    except (ValueError, TypeError):
        return None
