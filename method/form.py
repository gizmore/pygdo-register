import asyncio

from gdo.base.Application import Application
from gdo.base.GDT import GDT
from gdo.base.Trans import t, sitename
from gdo.base.util.href import url
from gdo.core.GDT_Name import GDT_Name
from gdo.core.GDT_Password import GDT_Password
from gdo.core.GDT_Serialize import GDT_Serialize
from gdo.form.GDT_Form import GDT_Form
from gdo.form.GDT_Validator import GDT_Validator
from gdo.form.MethodForm import MethodForm
from gdo.mail.GDT_Email import GDT_Email
from gdo.mail.Mail import Mail
from gdo.register import module_register
from gdo.register.GDO_UserActivation import GDO_UserActivation
from gdo.register.method.activate import activate
from gdo.ui.GDT_Link import GDT_Link


class form(MethodForm):

    @classmethod
    def gdo_trigger(cls) -> str:
        return ""

    def gdo_connectors(self) -> str:
        return "web"

    def gdo_create_form(self, form: GDT_Form) -> None:
        form.add_field(GDT_Name('username').icon('account').not_null())
        form.add_field(GDT_Password('password').not_null())
        form.add_field(GDT_Validator().validator(form, 'username', self.validate_unique_name))
        form.add_field(GDT_Email('email').not_null(module_register.instance().cfg_signup_mail()))
        Application.publish_event('build_signup_form', form)
        super().gdo_create_form(form)

    def validate_unique_name(self, form: GDT_Form, field: GDT, value: any) -> bool:
        if self._env_server.get_user_by_name(value):
            return field.error('err_violate_unique')
        return True

    def form_submitted(self):
        username = self.param_val('username')
        return self.register(username)

    def register(self, username: str):
        mod = module_register.instance()
        password = self.param_val('password')
        email = self.param_val('email')

        known = ('username', 'password', 'email', 'submit', 'csrf')
        data = {}
        for gdt in self.parameters().values():
            key = gdt.get_name()
            if key not in known:
                val = gdt.get_val()
                if val is not None:
                    data[key] = val
        activation = GDO_UserActivation.blank({
            'ua_username': username,
            'ua_server': self._env_server.get_id(),
            'ua_email': email,
            'ua_password': GDT_Password.hash(password),
            'ua_data': GDT_Serialize('ua_data').to_val(data),
        }).insert()

        if mod.cfg_signup_mail():
            self.send_signup_mail(activation)
            self.msg('msg_activation_mail_sent')
            return self.empty()
        else:
            return activate().env_copy(self).activate(activation)

    def send_signup_mail(self, activation: GDO_UserActivation):
        mail = Mail.from_bot()
        mail.subject(t('mails_signup'))
        link = GDT_Link().href(url('register', 'activate', f"&id={activation.get_id()}&token={activation.gdo_hash()}"))
        text_command = f"$activate {activation.get_id()} {activation.gdo_hash()}"
        mail.body(t('mailb_signup', (
            activation.gdo_val('ua_username'),
            sitename(),
            link.render_html(),
            text_command,
        )))
        mail.recipient(activation.gdo_val('ua_email'))
        mail.send()

