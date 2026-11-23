import unittest
from unittest.mock import MagicMock, patch

from gdo.base.Application import Application
from gdo.base.Render import Mode
from gdo.base.WithPermissionCheck import WithPermissionCheck
from gdo.register.method.form import form
from gdo.register.method.guest import guest


class RegisterFormPermissionsTest(unittest.TestCase):
    def setUp(self):
        Application.mode(Mode.render_html)
        WithPermissionCheck.CACHE.pop(form, None)
        WithPermissionCheck.CACHE.pop(guest, None)

    def test_guest_signup_accepts_unauthenticated_ghost(self):
        method = guest()
        method._env_channel = None
        user = MagicMock()
        user.is_authenticated.return_value = False
        user.is_system.return_value = False
        user.get_user_type.return_value = 'ghost'
        with patch.object(guest, 'allows_connector', return_value=True), \
             patch.object(guest, '_disabled_in_server', return_value=False):
            self.assertTrue(method.has_permission(user, display_error=False))
        self.assertFalse(method.gdo_needs_authentication())

    def test_guest_signup_rejects_member(self):
        method = guest()
        user = MagicMock()
        user.is_authenticated.return_value = True
        user.get_user_type.return_value = 'member'
        self.assertFalse(method.has_permission(user, display_error=False))

    def test_signup_is_for_unauthenticated_ghosts(self):
        method = form()
        method._env_channel = None
        user = MagicMock()
        user.is_authenticated.return_value = False
        user.is_system.return_value = False
        user.get_user_type.return_value = 'ghost'
        with patch.object(form, 'allows_connector', return_value=True), \
             patch.object(form, '_disabled_in_server', return_value=False):
            self.assertTrue(method.has_permission(user, display_error=False))
        self.assertFalse(method.gdo_needs_authentication())
        self.assertEqual('ghost', method.gdo_user_type())

    def test_signup_rejects_member(self):
        method = form()
        user = MagicMock()
        user.is_authenticated.return_value = True
        user.get_user_type.return_value = 'member'
        self.assertFalse(method.has_permission(user, display_error=False))


if __name__ == '__main__':
    unittest.main()
