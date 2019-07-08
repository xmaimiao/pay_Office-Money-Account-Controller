import time
import re
from common.do_config import config
class OAname:
    # def get_name(self):
    def __init__(self):
        now_time = time.strftime('%Y-%m-%d')
        name = now_time  + '澳科大-學費收款1'
        if now_time not in config.get('api','oaname'):
            config.set('api','oaname',name)

    def replace_name(self,title):
        before_code = re.match('^2.*款(\d+)$', config.get('api','oaname'),re.S).group(1)
        print(before_code)
        if title == '戶名唯一性校驗':
            name = config.get('api','oaname')
        else:
            name = config.get('api','oaname')[:18] + str(int(before_code) + 1)
            config.set('api', 'oaname', name)
        return name

if __name__ == '__main__':
    user =OAname()
    print(user.replace_name('驗證其他'))