import unittest
from ddt import ddt,data
from common.do_excel import Doexcel
from common.do_http import Dohttp
from common import contants
from common.context import replace,Context
from common.do_config import config
from common.gave_id import gettype
@ddt
class TestGetpre(unittest.TestCase):
    unit = unittest.TestCase()                                               #PermissionError錯誤一定是文件沒關閉
    do_excel = Doexcel(contants.case_dir, 'get_pre ')
    cases = do_excel.read_excel()

    @classmethod                                            #不定義為類方法 就會每次執行一次用例都調用此方法實例化對象，session就不同了，注意是setUpClass
    def setUpClass(cls):
        cls.dohttp = Dohttp()

    @data(*cases)
    def test_getpre(self,case):

        case.url = replace(case.url)  # 若存在寫在配置文件中的賬號和密碼、項目名，就必須通過replace函數去拿到正則表達式匹配的值
        if case.data:
            case.data = replace(case.data)
        case.headers = replace(case.headers)
        resp =self.dohttp.dohttp(json=case.json,data=case.data,url=case.url,method=case.method,headers=case.headers)
        print("響應結果：{}".format(resp))
        actual = resp.json()['success']
        print("測試結果：{}".format(actual))
        print("傳入的data：{}".format(case.data))
        print("傳入的headers：{}".format(case.headers))
        print("傳入的url：{}".format(case.url))
        print("傳入的title：{}".format(case.title))
        print("打印token：{}".format(getattr(Context, 'token')))

        try:
            self.unit.assertEqual(case.expect,actual)
            self.do_excel.write_excel(case.id+1,actual,'PASS')
        except AssertionError as e:
            msg = resp.json()['errorMsg']
            print("報錯信息：{}".format(msg))
            self.do_excel.write_excel(case.id+1,actual,'FALSE')
            raise e                                            #沒有寫這個只會顯示用例執行次數，寫之後控制台顯示有誤信息

        if  case.title == "獲取授權碼" and resp.json()['model']['accessToken']:
            setattr(Context,'token',resp.json()['model']['accessToken'])
            config.set('api','token',resp.json()['model']['accessToken'])
            print("打印token：{}".format(getattr(Context,'token')))
        elif  case.title == "获取开户结算银行、帐户、户名信息" :
            data= resp.json()['data']
            config.set('api','bankAccountName',data[0]['bankAccountName'])
            config.set('api','bankAccount',data[0]['bankAccount'])
            config.set('api','bankName',data[0]['bankName'])
        else:
            id = gettype(case.title,resp.json()['data'])
            print(id)
            print("打印{0}：{1}".format(id[0],config.get('api', id[0])))

    @classmethod
    def tearDownClass(cls):
        cls.dohttp.close()


