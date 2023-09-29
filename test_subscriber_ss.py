import base64
import unittest
from unittest.mock import patch
import requests
import subscriber_ss
import base64

kuromis_resp_plain = """ss://{0}@1hi34it5.baidu.com:10000#%F0%9F%87%AD%F0%9F%87%B0%20Hong%20Kong%2001
ss://{0}@1hi34it5.baidu.com:20000#%F0%9F%87%B8%F0%9F%87%AC%20Singapore%2001
ss://{0}@1hi34it5.baidu.com:30000#%F0%9F%87%B8%F0%9F%87%AC%20Singapore%2002
ss://{0}@bontqmct.baidu.com:40000#%F0%9F%87%AF%F0%9F%87%B5%20Japan%2001
ss://{0}@bontqmct.baidu.com:50000#%F0%9F%87%AF%F0%9F%87%B5%20Japan%2002
""".format(base64.b64encode(b'aes-128-gcm:CJK6EAzfeOYyRL2CZHgpp').decode('utf-8'))
kuromis_resp = base64.b64encode(kuromis_resp_plain.encode('utf-8'))

jms_resp_plain = """ss://{}#JMS-924089@85ab6u.q0v15eaa9.com:10001
ss://{}#JMS-924089@85ab7u.q0v15eaa9.com:20001
vmess://{}
vmess://{}""".format(base64.b64encode(b'aes-256-gcm:DasHEwGu3x1br936@10.0.0.2:10001').replace(b'=', b''),
                     base64.b64encode(b'aes-256-gcm:DasHEwGu3x1br936@10.0.0.3:20001').replace(b'=', b''),
                     base64.b64encode(b'{"ps":"JMS-924089@85ab8u.google.com:30001","port":"30001","id":"e72e19e6-0735-476a-a463-688d2151698b","aid":0,"net":"tcp","type":"none","tls":"none","add":"10.1.1.1"}').replace('=', ''),
                     base64.b64encode(b'{"ps":"JMS-924090@85ab9u.google.com:40001","port":"40001","id":"2cf3c153-7bc7-4428-b9af-96b50c4bc5a3","aid":0,"net":"tcp","type":"none","tls":"none","add":"10.1.1.2"}').replace('=', ''))
justmysocks_resp = base64.b64encode(jms_resp_plain.encode('utf-8'))


class SsSubscriberTestCase(unittest.TestCase):
    @patch.object(requests, 'get')
    def test_kuromis(self, mockget):
        mockresp = unittest.mock.Mock()
        mockget.return_value = mockresp
        mockresp.text = kuromis_resp

        sub = subscriber_ss.SsSubscriber("/url/to/kuromis/sub")
        result = sub.pull()
        self.assertEqual(len(result), 5)

        self.assertEqual(result[0].alg, 'aes-128-gcm')
        self.assertEqual(result[0].password, 'CJK6EAzfeOYyRL2CZHgpp')
        self.assertEqual(result[0].url, '1hi34it5.baidu.com')
        self.assertEqual(result[0].port, 10000)
        self.assertTrue('Hong Kong' in result[0].desc)

        self.assertEqual(result[1].alg, 'aes-128-gcm')
        self.assertEqual(result[1].password, 'CJK6EAzfeOYyRL2CZHgpp')
        self.assertEqual(result[1].url, '1hi34it5.baidu.com')
        self.assertEqual(result[1].port, 20000)
        self.assertTrue('Singapore' in result[1].desc)

        self.assertEqual(result[2].alg, 'aes-128-gcm')
        self.assertEqual(result[2].password, 'CJK6EAzfeOYyRL2CZHgpp')
        self.assertEqual(result[2].url, '1hi34it5.baidu.com')
        self.assertEqual(result[2].port, 30000)
        self.assertTrue('Singapore' in result[2].desc)

        self.assertEqual(result[3].alg, 'aes-128-gcm')
        self.assertEqual(result[3].password, 'CJK6EAzfeOYyRL2CZHgpp')
        self.assertEqual(result[3].url, 'bontqmct.baidu.com')
        self.assertEqual(result[3].port, 40000)
        self.assertTrue('Japan' in result[3].desc)

        self.assertEqual(result[4].alg, 'aes-128-gcm')
        self.assertEqual(result[4].password, 'CJK6EAzfeOYyRL2CZHgpp')
        self.assertEqual(result[4].url, 'bontqmct.baidu.com')
        self.assertEqual(result[4].port, 50000)
        self.assertTrue('Japan' in result[4].desc)


if __name__ == '__main__':
    unittest.main()
