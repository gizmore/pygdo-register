from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_String import GDT_String
from gdo.date.GDT_Created import GDT_Created
from gdo.net.GDT_IP import GDT_IP


class GDO_UserActivation(GDO):

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('ua_id'),
            GDT_String('ua_username'),
            GDT_String('ua_email'),
            GDT_IP('ua_ip').use_current(),
            GDT_Created('ua_created'),
        ]
