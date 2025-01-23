from gdo.base.Util import module_enabled
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_Name import GDT_Name
from gdo.core.GDT_Password import GDT_Password
from gdo.core.GDT_UserType import GDT_UserType
from gdo.form.GDT_Form import GDT_Form
from gdo.form.GDT_Submit import GDT_Submit
from gdo.form.GDT_Validator import GDT_Validator
from gdo.form.MethodForm import MethodForm
from gdo.login.GDT_Login import GDT_Login
from gdo.net.GDT_Url import GDT_Url
from gdo.ui.GDT_Link import GDT_Link


class guest(MethodForm):

    def gdo_trigger(self) -> str:
        return ""

    def gdo_user_type(self) -> str | None:
        return 'ghost'

    def gdo_create_form(self, form: GDT_Form) -> None:
        form.text('md_register_guest')
        form.add_field(GDT_Login('login').tooltip('tt_register_guest').not_null())
        form.add_field(GDT_Validator().validator(form, 'login', self.validate_unique_username))
        if module_enabled('login'):
            form.add_field(GDT_Password('password').not_null())
        form.add_field(GDT_Url('_back_to').internal().hidden())
        super().gdo_create_form(form)

    def validate_unique_username(self, form: GDT_Form, gdt: GDT_Login, user_name: str):
        if self._env_server.get_user_by_name(user_name):
            return gdt.error('err_username_taken')
        return True

    def gdo_submit_button(self) -> GDT_Submit:
        return super().gdo_submit_button().label('btn_as_guest')

    def form_submitted(self):
        username = self.param_val('login')
        displayname = f"~{username}~"
        user = self._env_server.get_or_create_user(displayname, displayname, GDT_UserType.GUEST)
        if module_enabled('login'):
            from gdo.login.module_login import module_login
            module_login.instance().set_password_for(user, self.param_val('password'))
        user.authenticate(self._env_session)
        back_to = self.param_val('_back_to')
        if back_to:
            link = GDT_Link().text('link_back_to').href(back_to).render()
            self.msg('msg_guest_created_back', (displayname, link))
        else:
            self.msg('msg_guest_created', (displayname,))
        return self.empty()
