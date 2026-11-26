from gdo.core.GDT_Object import GDT_Object
from gdo.form.MethodForm import MethodForm
from gdo.register.GDO_UserActivation import GDO_UserActivation
from gdo.register.method.activate import activate
from gdo.ui.GDT_Error import GDT_Error


class admin_activate_form(MethodForm):
    """Confirm and activate one pending registration through a CSRF-protected form."""

    def gdo_connectors(self):
        return 'web'

    def gdo_user_permission(self):
        return 'admin'

    def gdo_create_form(self, form):
        form.add_field(GDT_Object('id').table(GDO_UserActivation.table()).not_null())
        super().gdo_create_form(form)

    async def form_submitted(self):
        activation = self.param_value('id')
        activation_id = activation.get_id()
        result = await activate().env_copy(self).activate(activation, admin=True)
        if isinstance(result, GDT_Error):
            return result
        return self.reply('msg_admin_activation_done', (activation_id,))
