from gdo.base.Application import Application
from gdo.base.GDT import GDT
from gdo.core.GDT_Name import GDT_Name
from gdo.core.GDT_Password import GDT_Password
from gdo.core.connector.Web import Web
from gdo.form.GDT_Form import GDT_Form
from gdo.form.GDT_Validator import GDT_Validator
from gdo.form.MethodForm import MethodForm
from gdo.mail.GDT_Email import GDT_Email
from gdo.register import module_register
from gdo.register.GDO_UserActivation import GDO_UserActivation


class form(MethodForm):

    def gdo_create_form(self, form: GDT_Form) -> None:
        form.add_field(GDT_Name('username').not_null())
        form.add_field(GDT_Password('password').not_null())
        form.add_field(GDT_Validator().validator(form, 'username', self.validate_unique_name))
        if module_register.instance().cfg_signup_mail():
            form.add_field(GDT_Email('email').not_null())
        super().gdo_create_form(form)
        Application.EVENTS.publish('build_signup_form', form)

    def validate_unique_name(self, form: GDT_Form, field: GDT, value: any) -> bool:
        if Web.get_server().get_user_by_name(value):
            return field.error('err_violate_unique')
        return True

    def form_submitted(self):
        mod = module_register.instance()
        username = self.param_val('username')
        password = self.param_val('password')
        email = self.param_val('email')

        activation = GDO_UserActivation.blank({

        })

        if mod.cfg_signup_mail():
            self.send_signup_mail(us)
        else:
            activate().activate(activation)
        Mail.from_bot()