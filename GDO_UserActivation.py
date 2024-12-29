from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Password import GDT_Password
from gdo.core.GDT_Serialize import GDT_Serialize
from gdo.core.GDT_Server import GDT_Server
from gdo.core.GDT_String import GDT_String
from gdo.date.GDT_Created import GDT_Created
from gdo.net.GDT_IP import GDT_IP


class GDO_UserActivation(GDO):

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('ua_id'),
            GDT_String('ua_username'),
            GDT_Server('ua_server'),
            GDT_String('ua_email'),
            GDT_Password('ua_password'),
            GDT_IP('ua_ip').use_current(),
            GDT_Serialize('ua_data'),
            GDT_Created('ua_created'),
        ]
