from gdo.core.GDT_Name import GDT_Name
from gdo.form.GDT_Form import GDT_Form
from gdo.form.MethodForm import MethodForm


class form(MethodForm):

    def gdo_create_form(self, form: GDT_Form) -> None:
        form.add_field(GDT_Name('login').not_null())
        super().gdo_create_form(form)