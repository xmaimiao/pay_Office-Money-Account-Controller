import unittest
from ddt import ddt,data
from common.do_excel import Doexcel
from common.do_http import Dohttp
from common import contants
from common.context import replace,Context
from common.do_config import config
from common.get_name import OAname
@ddt
class TestGetaccount(unittest.TestCase):
    unit = unittest.TestCase()                                               #PermissionError錯誤一定是文件沒關閉
    do_excel = Doexcel(contants.case_dir, 'get_account')
    cases = do_excel.read_excel()
    oaname = OAname()

    @classmethod                                            #不定義為類方法 就會每次執行一次用例都調用此方法實例化對象，session就不同了，注意是setUpClass
    def setUpClass(cls):
        cls.dohttp = Dohttp()

    @data(*cases)
    def test_getaccount(self,case):

        case.url = replace(case.url)  # 若存在寫在配置文件中的賬號和密碼、項目名，就必須通過replace函數去拿到正則表達式匹配的值

        if case.data:
            case.data = replace(case.data)
        elif case.json.find("OAname"):
            self.oaname.replace_name(case.title)
            case.json=replace(case.json)
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
        except AssertionError as e:
            print("粗錯了！")
            raise e
        if  case.title == "獲取授權碼" and resp.json()['model']['accessToken']:
            config.set('api','token',resp.json()['model']['accessToken'])
            print("打印token：{}".format(getattr(Context,'token')))

    @classmethod
    def tearDownClass(cls):
        cls.dohttp.close()

