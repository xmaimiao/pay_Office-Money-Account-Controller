from common.do_config import config
def gettype(title,data):
    if title == "獲取部門id":
        conf_data = eval(config.get('api','groups'))
        option = "groupsid"
        ids=getid(conf_data,data,option)

    elif title=="獲取教師id":
        conf_data = eval(config.get('api', 'teachers'))
        option = "teachersid"
        ids=getid(conf_data, data, option)
    else:
        option = None
        ids=None
    return option, ids

def getid(conf_data,data,option):
    ids = []
    for i in conf_data:
        for j in data:
            if i == j['name']:
                id = j['id']
                ids.append(id)
    config.set('api', option, str(ids))
    return ids

def getaccountname(data):
    for i in data:
        if i["id"] == config.get('setting','accountid'):
          return i["name"]
