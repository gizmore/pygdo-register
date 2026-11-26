import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from gdo.base.Application import Application
from gdo.base.Render import Mode
from gdo.register.method.admin_activate import admin_activate
from gdo.register.method.admin_activations import admin_activations
from gdo.register.method.admin_activate_form import admin_activate_form
from gdo.register.method.activate import activate


class AdminActivationTest(unittest.IsolatedAsyncioTestCase):
    async def test_admin_action_uses_existing_flow_without_login(self):
        Application.mode(Mode.render_cli)
        method = admin_activate()
        item = MagicMock()
        item.get_id.return_value = '7'
        method.param_value = MagicMock(return_value=item)
        method.reply = MagicMock(return_value='done')
        handler = MagicMock()
        handler.env_copy.return_value = handler
        handler.activate = AsyncMock(return_value=None)
        with patch('gdo.register.method.admin_activate.activate', return_value=handler):
            self.assertEqual('done', await method.gdo_execute())
        handler.activate.assert_awaited_once_with(item, admin=True)
        self.assertEqual('admin', method.gdo_user_permission())
        self.assertTrue(method.gdo_needs_authentication())
        self.assertEqual('bash', method.gdo_connectors())

    def test_listing_only_exposes_safe_columns(self):
        method = admin_activations()
        table = MagicMock()
        table.columns.return_value = {name: name for name in ('ua_id', 'ua_username', 'ua_server', 'ua_created')}
        method.gdo_table = MagicMock(return_value=table)
        headers = method.gdo_table_headers()
        self.assertEqual(['ua_id', 'ua_username', 'ua_server', 'ua_created'], headers[:4])
        self.assertFalse(headers[4].is_filterable())
        self.assertFalse(headers[4].is_orderable())
        self.assertEqual('admin', method.gdo_user_permission())
        self.assertTrue(method.gdo_needs_authentication())

    async def test_web_confirmation_uses_admin_activation(self):
        Application.mode(Mode.render_cli)
        method = admin_activate_form()
        item = MagicMock()
        item.get_id.return_value = '7'
        method.param_value = MagicMock(return_value=item)
        method.reply = MagicMock(return_value='done')
        handler = MagicMock()
        handler.env_copy.return_value = handler
        handler.activate = AsyncMock(return_value=None)
        with patch('gdo.register.method.admin_activate_form.activate', return_value=handler):
            self.assertEqual('done', await method.form_submitted())
        handler.activate.assert_awaited_once_with(item, admin=True)
        self.assertTrue(method.gdo_needs_authentication())
        self.assertEqual('admin', method.gdo_user_permission())
        self.assertEqual('web', method.gdo_connectors())

    async def test_admin_activation_does_not_log_in_new_user(self):
        Application.mode(Mode.render_cli)
        method = activate()
        method.msg = MagicMock()
        method.empty = MagicMock(return_value='done')
        item = MagicMock()
        item.gdo_value.side_effect = lambda key: {} if key == 'ua_data' else server
        item.gdo_val.side_effect = lambda key: {'ua_username': 'test', 'ua_password': 'hash'}[key]
        server = MagicMock()
        server.get_or_create_user = AsyncMock(return_value=MagicMock())
        login = MagicMock()
        events = MagicMock()
        events.publish = AsyncMock()
        with patch('gdo.register.method.activate.module_enabled', side_effect=lambda name: name == 'login'), \
             patch('gdo.login.module_login.module_login.instance', return_value=login), \
             patch.object(Application, 'EVENTS', events, create=True), \
             patch.object(Application, 'IS_HTTP', True):
            self.assertEqual('done', await method.activate(item, admin=True))
        login.set_password_hash_for.assert_called_once()
        item.delete.assert_called_once()
