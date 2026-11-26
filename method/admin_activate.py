from gdo.base.Method import Method
from gdo.core.GDT_Object import GDT_Object
from gdo.register.GDO_UserActivation import GDO_UserActivation
from gdo.register.method.activate import activate
from gdo.ui.GDT_Error import GDT_Error


class admin_activate(Method):
    """Activate a pending registration without logging in as that user."""

    def gdo_needs_authentication(self):
        return True

    def gdo_user_permission(self):
        return 'admin'

    def gdo_connectors(self):
        # Avoid a state-changing GET and exposure of activation IDs in URLs.
        return 'bash'

    def gdo_parameters(self):
        return [GDT_Object('id').table(GDO_UserActivation.table()).not_null().positional()]

    async def gdo_execute(self):
        activation = self.param_value('id')
        activation_id = activation.get_id()
        result = await activate().env_copy(self).activate(activation, admin=True)
        if isinstance(result, GDT_Error):
            return result
        return self.reply('msg_admin_activation_done', (activation_id,))
