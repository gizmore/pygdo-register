import os
import unittest

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.core.GDO_User import GDO_User
from gdo.core.connector.Web import Web
from gdotest.TestUtil import reinstall_module, web_plug, WebPlug


class RegisterTest(unittest.TestCase):

    def setUp(self):
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        loader = ModuleLoader.instance()
        loader.load_modules_db(True)
        loader.init_modules()
        reinstall_module('register')
        WebPlug.COOKIES = {}
        return self

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


if __name__ == '__main__':
    unittest.main()
