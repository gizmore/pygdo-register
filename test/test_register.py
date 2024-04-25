import os
import unittest

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdotest.TestUtil import reinstall_module, web_plug


class RegisterTest(unittest.TestCase):

    def setUp(self):
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        loader = ModuleLoader.instance()
        loader.load_modules_db(True)
        loader.init_modules()
        reinstall_module('register')
        return self

    def test_01_signup_sidebar_hook(self):
        out = web_plug('register.form.html').exec()
        self.assertIn('Sign-Up', out, 'Register module did not hook right sidebar')


if __name__ == '__main__':
    unittest.main()
