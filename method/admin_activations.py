from gdo.register.GDO_UserActivation import GDO_UserActivation
from gdo.table.MethodQueryTable import MethodQueryTable
from gdo.ui.GDT_Link import GDT_Link
from gdo.base.util.href import href


class ActivationAction(GDT_Link):
    def is_filterable(self):
        return False

    def is_orderable(self):
        return False


class admin_activations(MethodQueryTable):
    """List pending activations without exposing credentials or tokens."""

    def gdo_needs_authentication(self):
        return True

    def gdo_user_permission(self):
        return 'admin'

    def gdo_table(self):
        return GDO_UserActivation.table()

    def gdo_table_headers(self):
        columns = self.gdo_table().columns()
        return [columns[name] for name in ('ua_id', 'ua_username', 'ua_server', 'ua_created')] + [
            ActivationAction('activation_action').label('mt_register_admin_activate')]

    def render_activation_action(self, field, activation):
        return (GDT_Link().href(href('register', 'admin_activate_form', f'&id={activation.get_id()}'))
                .text('mt_register_admin_activate').icon('check').render_html())

    def gdo_table_query(self):
        return self.gdo_table().select().only_select('ua_id,ua_username,ua_server,ua_created')

    def gdo_order_default(self):
        return 'ua_id ASC'

    def render_gdo(self, gdo, mode):
        if mode.name == 'render_json':
            return super().render_gdo(gdo, mode)
        return f"{gdo.get_id()}-{gdo.gdo_val('ua_username')}"
