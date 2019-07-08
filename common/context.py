import re
from common.do_config import config
import configparser

class Context:
    token =None

def replace(data):
    p='#(.*?)#'
    while re.search(p,data):
        data_new = re.search(p,data).group(1)
        try:
            try:
                da = config.get('api', data_new)
            except Exception as e:
                da = config.get('edit_ap', data_new)
        except configparser.NoOptionError as e:
            if hasattr(Context,data_new):
                da = str(getattr(Context,data_new))
            else:
                print("找不到参数信息！")
                raise e
        data = re.sub(p,da,data,count=1)  #查找替換，count查找替換的次數
    return data

if __name__ == '__main__':
    get = getattr(Context,'loan_id')
    print(get)