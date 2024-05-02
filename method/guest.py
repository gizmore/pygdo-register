from gdo.core.GDT_Name import GDT_Name
from gdo.core.GDT_Password import GDT_Password
from gdo.form.GDT_Form import GDT_Form
from gdo.form.MethodForm import MethodForm


class guest(MethodForm):

    def gdo_create_form(self, form: GDT_Form) -> None:
        form.text('md_register_guest')
        form.add_field(
            GDT_Name('login').not_null(),
            GDT_Password('password').not_null(),
        )
        super().gdo_create_form(form)
