from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.core import module_core
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_Bool import GDT_Bool
from gdo.form.GDT_Form import GDT_Form
from gdo.register.GDO_UserActivation import GDO_UserActivation
from gdo.ui.GDT_Link import GDT_Link
from gdo.base.GDO import GDO
from gdo.base.Application import Application
from urllib.parse import parse_qs, urlencode, urlsplit


class module_register(GDO_Module):

    def __init__(self):
        super().__init__()
        self._priority = 85

    def gdo_dependencies(self) -> list:
        return [
            'form',
            'login',
        ]

    def gdo_classes(self) -> list[type[GDO]]:
        return [
            GDO_UserActivation,
        ]

    def gdo_admin_links(self) -> list[GDT_Link]:
        return [GDT_Link().href(self.href('admin_activations')).text('mt_register_admin_activations')]

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_Bool('signup_guests').initial('1'),
            GDT_Bool('signup_autologin').initial('1'),
            GDT_Bool('signup_mail_required').initial('1'),
        ]

    def cfg_guest_signup(self) -> bool:
        return self.get_config_value('signup_guests') and module_core.instance().cfg_guest_system()

    def cfg_signup_mail(self) -> bool:
        return self.get_config_value('signup_mail_required')

    def cfg_signup_login(self) -> bool:
        return self.get_config_value('signup_autologin')

    def gdo_init_sidebar(self, page):
        if GDO_User.current().is_ghost():
            from gdo.register.return_path import safe_return_path
            back_to = safe_return_path(Application.current_href())
            append = '&' + urlencode({'_back_to': back_to}) if back_to else ''
            page._right_bar.add_field(GDT_Link().href(self.href('form', append)).text('module_register'))
            if self.cfg_guest_signup():
                page._right_bar.add_field(GDT_Link().href(self.href('guest', append)).text('link_register_guest_sidebar'))

    def gdo_subscribe_events(self):
        if self.cfg_guest_signup():
            self.subscribe('build_signup_form', self.guest_signup_form)

    def guest_signup_form(self, form: GDT_Form):
        from gdo.register.return_path import safe_return_path
        query = parse_qs(urlsplit(Application.current_href()).query)
        back_to = safe_return_path(query.get('_back_to', [None])[0])
        append = '&' + urlencode({'_back_to': back_to}) if back_to else ''
        form.add_field(GDT_Link().href(self.href('guest', append)).text('mt_register_guest'))
