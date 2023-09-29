import base64
import requests
import re
from urllib.parse import unquote_plus


class Shadowsocks:
    def __init__(self):
        self.type = "ss"


class SsSubscriber:
    def __init__(self, url):
        self._url = url

    def pull(self):
        results = []
        resp = requests.get(self._url).text
        links = base64.b64decode(resp).decode('utf-8').split('\n')
        for link in links:
            if len(link) == 0:
                continue
            proto, detail = link.split('://')
            if proto == 'ss':
                results.append(SsSubscriber._parse_ss(detail))
                continue
            raise Exception("unsupport protocol " + proto)
        return results

    @staticmethod
    def _parse_ss(link):
        ss = Shadowsocks()

        elements = re.split(r'[@:#]', link)
        # alg:pwd[@ip:port]
        to_parse = base64.b64decode(elements[0] + '=' * (-len(elements[0]) % 4)).decode('utf-8')
        sub_ele = re.split(r'[:@]', to_parse)
        if len(sub_ele) == 2:
            ss.alg = sub_ele[0]
            ss.password = sub_ele[1]
        elif len(sub_ele) == 4:
            ss.alg = sub_ele[0]
            ss.password = sub_ele[1]
            SsSubscriber._parse_url_or_ip(sub_ele[2], ss)
            ss.port = sub_ele[3]
        else:
            raise Exception("Unexpected alg field " + elements[0])

        m_desc = re.compile(r'#(?P<desc>[^@:#]+)').search(link)
        if m_desc is not None:
            ss.desc = unquote_plus(m_desc.group('desc'))

        m_url_and_port = re.compile(r'@(?P<url>[^@:#]+):(?P<port>\d+)').search(link)
        if m_url_and_port is not None:
            ss.port = int(m_url_and_port.group('port'))
            SsSubscriber._parse_url_or_ip(m_url_and_port.group('url'), ss)

        return ss

    @staticmethod
    def _parse_url_or_ip(maybe_url, ss):
        r_ipv4 = re.compile(r'^\d+(\.\d+){3}$')
        m_ipv4 = r_ipv4.match(maybe_url)
        if m_ipv4 is not None:
            ss.ip = maybe_url
        else:
            ss.url = maybe_url
