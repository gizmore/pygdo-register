import os
import unittest

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.core.GDO_User import GDO_User
from gdo.core.connector.Web import Web
from gdo.register.module_register import module_register
from gdotest.TestUtil import reinstall_module, web_plug, WebPlug, GDOTestCase


class RegisterTest(GDOTestCase):

    def setUp(self):
        super().setUp()
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        loader = ModuleLoader.instance()
        reinstall_module('register')
        loader.load_modules_db(True)
        loader.init_modules(True, True)
        WebPlug.COOKIES = {}

    def test_00_welcome_again(self):
        out = web_plug('core.welcome.html').exec()
        self.assertIn('Welcome', out, 'Somethings wrong!')

    def test_01_signup_sidebar_hook(self):
        out = web_plug('register.form.html').exec()
        self.assertIn('Sign-Up', out, 'Register module did not hook right sidebar')

    def test_02_signup_hooked_with_guest_link(self):
        out = web_plug('register.form.html').exec()
        self.assertIn('Continue as Guest', out, 'Register module did not hook register form with guests')

    def test_03_signup_guest_user(self):
        GDO_User.table().delete_where('user_displayname="~AGuest~"')
        out = web_plug('register.guest.html').post({"login": "AGuest", "password": "11111111", "_back_to": "/core.welcome.html", "submit": "1"}).exec()
        user = Web.get_server().get_user_by_name('~AGuest~')
        self.assertIsNotNone(user, "Simple guest signup does not work")
        self.assertIn('from where you came.', out, '_back_to does not work.')

    def test_04_instant_register(self):
        module_register.instance().save_config_val('signup_mail_required', '0')
        out = web_plug('register.form.html?username=petra2&password=11111111&submit=1').exec()
        user = GDO_User.current()
        user.delete()
        self.assertEqual(user.get_name(), 'petra2', 'After Register Not authenticated')
        module_register.instance().save_config_val('signup_mail_required', '1')

    def test_05_register_and_signup(self):
        out = web_plug('register.form.html?username=petra&password=11111111&email=petra@gizmore.org&submit=1').exec()
        self.assertIn('instructions', out, 'Cannot send register mail.')


if __name__ == '__main__':
    unittest.main()
