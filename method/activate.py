from gdo.base.Application import Application
from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.Util import module_enabled
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_Object import GDT_Object
from gdo.core.GDT_Token import GDT_Token
from gdo.register.GDO_UserActivation import GDO_UserActivation
from gdo.register.module_register import module_register


class activate(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return "activate"

    def gdo_needs_authentication(self) -> bool:
        return False

    def gdo_has_permission(self, user: 'GDO_User'):
        return not user._authenticated

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_Object('id').table(GDO_UserActivation.table()).not_null(),
            GDT_Token('token').not_null(),
        ]

    async def gdo_execute(self) -> GDT:
        token = self.param_val('token')
        activation = self.param_value('id')
        if activation.gdo_hash() != token:
            return self.err('err_token')
        return await self.activate(activation)

    async def activate(self, activation: GDO_UserActivation, admin: bool = False):
        data = activation.gdo_value('ua_data') or {}
        if user_id := data.get('mail_change_user'):
            return await self.activate_mail_change(activation, user_id)
        username = activation.gdo_val('ua_username')
        server = activation.gdo_value('ua_server')
        user = await server.get_or_create_user(username)
        self.msg('msg_activated')
        if module_enabled('mail'):
            from gdo.mail.module_mail import module_mail
            mail = activation.gdo_val('ua_email')
            if mail:
                module_mail.instance().set_email_for(user, mail)
        if module_enabled('login'):
            from gdo.login.module_login import module_login
            module_login.instance().set_password_hash_for(user, activation.gdo_val('ua_password'))
            if not admin and module_register.instance().cfg_signup_login():
                from gdo.login.method.form import form
                await form().env_copy(self).login_success(user, False)
        await Application.EVENTS.publish('user_activated', user, activation)
        activation.delete()
        if Application.IS_HTTP and not admin:
            from gdo.register.return_path import safe_return_path
            from gdo.net.GDT_Redirect import GDT_Redirect
            if back_to := safe_return_path(data.get('_back_to')):
                return GDT_Redirect().href(back_to)
        return self.empty()

    async def activate_mail_change(self, activation: GDO_UserActivation, user_id: str):
        """Finish an address change after the new mailbox confirmed it."""
        user = GDO_User.table().get_by_id(user_id)
        if not user:
            return self.err('err_activation_user')
        if module_enabled('mail'):
            from gdo.mail.module_mail import module_mail
            module_mail.instance().set_email_for(user, activation.gdo_val('ua_email'), True)
        activation.delete()
        return self.msg('msg_mail_changed')
