from gdo.base.Application import Application
from gdo.base.Util import module_enabled
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_Name import GDT_Name
from gdo.core.GDT_Secret import GDT_Secret
from gdo.form.GDT_Form import GDT_Form
from gdo.form.GDT_Submit import GDT_Submit
from gdo.form.GDT_Validator import GDT_Validator
from gdo.mail.GDT_Email import GDT_Email
from gdo.register.module_register import module_register
from gdo.register.method.form import form


class irc(form):

    def gdo_trigger(self) -> str:
        return 'register'

    def gdo_connectors(self) -> str:
        return 'irc'

    def gdo_needs_authentication(self) -> bool:
        return False

    def gdo_has_permission(self, user: 'GDO_User'):
        if user._authenticated:
            return False
        return True

    def gdo_create_form(self, form: GDT_Form) -> None:
        # form.add_field(GDT_Name('username').writable(False).hidden(True).initial(self._env_user.get_name()))
        form.add_field(GDT_Secret('password').not_null())
        # form.add_field(GDT_Validator().validator(form, 'username', self.validate_unique_name))
        if module_enabled('mail'):
            form.add_field(GDT_Email('email').not_null(module_register.instance().cfg_signup_mail()))
        # Application.EVENTS.publish('build_signup_form', form)
        form.actions().add_field(GDT_Submit().calling(self.form_submitted).default_button())

    def form_submitted(self):
        username = self._env_user.get_name()
        return self.register(username)
