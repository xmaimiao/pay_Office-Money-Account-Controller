from common.do_config import config
from common.context import replace,Context
class Setting:
    def get_approveid(self,get_section,get_option,set_section,set_option,data):
        for i in data:
            if i['title'] == config.get(get_section, get_option):
                config.set(set_section, set_option, i['id'])
    def get_accountid(self,get_section,get_option,data):
        for i in data:
            if i['name'] == config.get(get_section, get_option):
                setattr(Context, 'accountid', i['id'])