import unittest
from ddt import ddt,data
from common.do_excel import Doexcel
from common.do_http import Dohttp
from common import contants
from common.context import replace
from common.do_config import config
@ddt
class TestSetapprove(unittest.TestCase):
    unit = unittest.TestCase()
    do_excel = Doexcel(contants.case_dir, 'set_approve')
    cases = do_excel.read_excel()

    @classmethod
    def setUpClass(cls):
        cls.dohttp = Dohttp()

    @data(*cases)
    def test_setapprove(self,case):

        case.url = replace(case.url)
        if case.data:
            case.data = replace(case.data)
        elif case.json:
            case.json=replace(case.json)
        case.headers = replace(case.headers)
        resp =self.dohttp.dohttp(json=case.json,data=case.data,url=case.url,method=case.method,headers=case.headers)
        actual = resp.json()['success']
        print("傳入的data：{}".format(case.data))
        print("傳入的url：{}".format(case.url))
        print("傳入的title：{}".format(case.title))

        try:
            self.unit.assertEqual(case.expect,actual)
            self.do_excel.write_excel(case.id+1,actual,'PASS')
        except AssertionError as e:
            msg = resp.json()['errorMsg']
            print("報錯信息：{}".format(msg))
            self.do_excel.write_excel(case.id+1,actual,'FALSE')
            raise e

        if  case.title == "獲取授權碼" and resp.json()['model']['accessToken']:
            config.set('api','token',resp.json()['model']['accessToken'])
        elif  case.title == "驗證審批組已修改":
            actual_approver= resp.json()['model']['approvalUsers'][0]
            expect_approver = eval(config.get('edit_ap', 'GroupOption'))["approvalUserOptions"][0]
            try:
                self.unit.assertEqual(expect_approver["userId"], actual_approver["userId"])
            except AssertionError as e:
                print("修改審批組不成功！")
                raise e
        elif  case.title == "驗證審批類型已修改":
            actual_groupId =resp.json()['model']['approvalFlows'][0]
            expect_approver = eval(config.get('edit_ap', 'CategoryOption'))["approvalFlowOptions"][0]
            try:
                self.unit.assertEqual(expect_approver["userId"], actual_groupId["groupId"])
            except AssertionError as e:
                print("修改審批類別不成功！")
                raise e

    @classmethod
    def tearDownClass(cls):
        cls.dohttp.close()


