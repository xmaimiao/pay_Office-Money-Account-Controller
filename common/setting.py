from common.do_config import config
class Setting:
    def get_account_approveid(self,get_section,get_option,set_section,set_option,data):
        for i in data:
            if i['name'] == config.get(get_section, get_option):
                config.set(set_section, set_option, i['id'])