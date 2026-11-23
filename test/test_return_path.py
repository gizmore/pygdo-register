import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from gdo.register.return_path import safe_return_path
from gdo.register.method.guest import guest


class ReturnPathTest(unittest.TestCase):
    def test_local_paths_and_same_origin_urls(self):
        with patch('gdo.register.return_path.Application.config', side_effect=lambda key: {'core.domain': 'example.org', 'core.port': 443}.get(key)):
            self.assertEqual('/forum.html?a=1', safe_return_path('/forum.html?a=1'))
            self.assertEqual('/forum.html?a=1', safe_return_path('https://example.org/forum.html?a=1'))
            for value in ('//evil.example/path', 'https://evil.example/', 'https://example.org:444/',
                          'https://example.org@evil.example/', '/\\evil.example/', '/ok\r\nLocation: /bad'):
                self.assertIsNone(safe_return_path(value), value)


class GuestReturnTest(unittest.IsolatedAsyncioTestCase):
    async def test_guest_redirects_after_authentication(self):
        method = guest.__new__(guest)
        method.param_val = MagicMock(side_effect=lambda name: {'login': 'visitor', '_back_to': '/forum.html'}[name])
        method._env_server = MagicMock()
        user = MagicMock()
        user.authenticate = AsyncMock()
        method._env_server.get_or_create_user = AsyncMock(return_value=user)
        method._env_session = MagicMock()
        method.msg = MagicMock()
        redirect = MagicMock()
        redirect.href.return_value = redirect
        with patch('gdo.register.method.guest.module_enabled', return_value=False), \
             patch('gdo.register.method.guest.GDT_Redirect', return_value=redirect):
            self.assertIs(redirect, await method.form_submitted())
        user.authenticate.assert_awaited_once_with(method._env_session)
        redirect.href.assert_called_once_with('/forum.html')
