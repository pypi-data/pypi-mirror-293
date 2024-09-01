import unittest
from upinfopy import UpinfoPy

class TestUpinfoPy(unittest.TestCase):
    def setUp(self):
        UpinfoPy.pcid = ""  # 重置静态变量

    def test_to_url_encode_default_values(self):
        up_info = UpinfoPy()
        url_encoded = up_info.to_url_encode()
        self.assertEqual("sid=", url_encoded)

    def test_to_url_encode_with_custom_values(self):
        UpinfoPy.pcid = "PC123"
        up_info = UpinfoPy()
        up_info.uname = "testuser"
        up_info.cid = "cidguest"
        up_info.bcid = "cidvps"
        up_info.sid = "session123"
        up_info.cache = "cache123"
        up_info.mid = "custom_mid"
        up_info.order = "name"
        up_info.desc = 1
        up_info.getnumber = 50
        up_info.getstart = 10
        up_info.midpk = 12345
        up_info.set_par("param1", "param2")
        up_info.cols = ["col1", "col2"]

        url_encoded = up_info.to_url_encode()
        expected = "sid=session123&uname=testuser&bcid=28401227-bd00-a20f-c561-ddf0def881d9&cache=cache123&mid=custom_mid&pcid=PC123&order=name%20desc&getnumber=50&getstart=10&midpk=12345&pars=%5B%22param1%22%2C%20%22param2%22%5D&cols=%5B%22col1%22%2C%20%22col2%22%5D"
        self.assertEqual(expected, url_encoded)

    def test_cid_handling(self):
        up_info = UpinfoPy()
        up_info.cid = "cidmy"
        url_encoded = up_info.to_url_encode()
        self.assertIn("cid=d4856531-e9d3-20f3-4c22-fe3c65fb009c", url_encoded)

    def test_bcid_handling(self):
        up_info = UpinfoPy()
        up_info.bcid = "cidguest"
        url_encoded = up_info.to_url_encode()
        self.assertIn("bcid=GUEST000-8888-8888-8888-GUEST00GUEST", url_encoded)

    def test_pars_encoding_v22(self):
        up_info = UpinfoPy()
        up_info.v = 22
        up_info.set_par("param1", "param2")
        url_encoded = up_info.to_url_encode()
        self.assertIn("pars=", url_encoded)
        # 这里可以添加更具体的断言来检查编码后的参数格式

    def test_pars_encoding_default(self):
        up_info = UpinfoPy()
        up_info.set_par("param1", "param2")
        url_encoded = up_info.to_url_encode()
        self.assertIn("pars=%5B%22param1%22%2C%20%22param2%22%5D", url_encoded)

if __name__ == '__main__':
    unittest.main()