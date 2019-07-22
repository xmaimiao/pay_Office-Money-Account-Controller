import unittest
from ddt import ddt,data
from common.do_excel import Doexcel
from common.do_http import Dohttp
from common import contants
from common.context import replace
from common.do_config import config
from common.get_name import OAname
from common.get_approverid import GetApprover
from common.setting import Setting
from common.gave_id_stutas import getstatus
@ddt
class TestSetting(unittest.TestCase):
    unit = unittest.TestCase()                                               #PermissionError錯誤一定是文件沒關閉
    do_excel = Doexcel(contants.case_dir, 'setting')
    cases = do_excel.read_excel()
    oaname = OAname()
    GetApprover()
    setting = Setting()

    @classmethod                                            #不定義為類方法 就會每次執行一次用例都調用此方法實例化對象，session就不同了，注意是setUpClass
    def setUpClass(cls):
        cls.dohttp = Dohttp()

    @data(*cases)
    def test_setting(self,case):

        case.url = replace(case.url)  # 若存在寫在配置文件中的賬號和密碼、項目名，就必須通過replace函數去拿到正則表達式匹配的值

        if case.data:
            case.data = replace(case.data)
        if case.title =="賬戶業務開戶" and case.json.find("OAname"):
            self.oaname.replace_name(case.title)
            case.json=replace(case.json)
        elif case.json and "审批" or "設置賬戶" in case.title:
            case.json = replace(case.json)
        print("傳入的json：{}".format(case.json))
        case.headers = replace(case.headers)
        resp =self.dohttp.dohttp(json=case.json,data=case.data,url=case.url,method=case.method,headers=case.headers)
        actual = resp.json()['success']
        print("測試結果：{}".format(actual))
        print("傳入的json：{}".format(case.json))
        print("傳入的url：{}".format(case.url))
        print("傳入的title：{}".format(case.title))
        msg = resp.json()['errorMsg']
        print("報錯信息：{}".format(msg))
        self.do_excel.write_excel(case.id + 1, actual, 'FALSE', msg)

        try:
            self.unit.assertEqual(case.expect,actual)
            self.do_excel.write_excel(case.id+1,actual,'PASS')
            if "驗證賬戶" in case.title:
                print(type(config.get("setting","status").upper()))
                print(getstatus(resp.json()['data']))
                self.unit.assertEqual(config.get("setting","status").upper(),getstatus(resp.json()['data']))

        except AssertionError as e:
            print("粗錯了！")
            raise e                                            #沒有寫這個只會顯示用例執行次數，寫之後控制台顯示有誤信息

        if  case.title == "獲取授權碼" and resp.json()['model']['accessToken']:
            config.set('api','token',resp.json()['model']['accessToken'])
        elif case.title== "獲取賬戶id" :
            self.setting.get_accountid('api','oaname',resp.json()['data'])
        elif case.title== "獲取approveid":
            self.setting.get_approveid('api', 'oaname', 'edit_ap', 'approveid', resp.json()['data'])



    @classmethod
    def tearDownClass(cls):
        cls.dohttp.close()

