from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.core.GDT_Bool import GDT_Bool
from gdo.ui.GDT_Link import GDT_Link


class module_register(GDO_Module):

    def __init__(self):
        super().__init__()
        self._priority = 85

    def gdo_classes(self):
        return [
        ]

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_Bool('signup_mail_required').initial('1'),
            GDT_Bool('signup_autologin').initial('1'),
        ]

    def cfg_signup_mail(self) -> bool:
        return self.get_config_value('signup_mail_required')

    def cfg_signup_login(self) -> bool:
        return self.get_config_value('signup_autologin')

    def gdo_init_sidebar(self, page):
        page._right_bar.add_field(GDT_Link().href(self.href('form')).text('module_register'))
