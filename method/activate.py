from gdo.base.Application import Application
from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.Util import module_enabled
from gdo.core.GDT_Object import GDT_Object
from gdo.core.GDT_Token import GDT_Token
from gdo.core.connector.Web import Web
from gdo.register.GDO_UserActivation import GDO_UserActivation
from gdo.register.module_register import module_register


class activate(Method):

    def gdo_trigger(self) -> str:
        return ""

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_Object('id').table(GDO_UserActivation.table()),
            GDT_Token('token').not_null(),
        ]

    def gdo_execute(self) -> GDT:
        token = self.param_val('token')
        activation = self.param_value('id')
        if activation.gdo_hash() != token:
            return self.err('err_token')
        return self.activate(activation)

    def activate(self, activation: GDO_UserActivation):
        username = activation.gdo_val('ua_username')
        user = Web.get_server().create_user(username)
        self.msg('msg_activated')
        if module_enabled('mail'):
            from gdo.mail.module_mail import module_mail
            mail = activation.gdo_val('ua_email')
            if mail:
                module_mail.instance().set_email_for(user, mail)
                module_mail.instance().set_mail_confirmed_for(user)
        if module_enabled('login'):
            from gdo.login.module_login import module_login
            module_login.instance().set_password_hash_for(user, activation.gdo_val('ua_password'))
            if module_register.instance().cfg_signup_login():
                from gdo.login.method.form import form
                form().env_copy(self).login_success(user, False)
        Application.EVENTS.publish('user_activated', user, activation)
        return self.empty()
