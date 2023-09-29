from subscriber_ss import Shadowsocks
import json


class SsGenerator:
    def __init__(self, inbound, ss_service: Shadowsocks):
        self._inbound = inbound
        self._ss_outbound = ss_service
        self._user_ip = False

    def generate(self, path):
        config = {
            "server": self._ss_outbound.ip if self._user_ip else self._ss_outbound.url,
            "server_port": self._ss_outbound.port,
            "local_address": self._inbound.ip,
            "local_port": self._inbound.port,
            "password": self._ss_outbound.password,
            "timeout": 300,
            "method": self._ss_outbound.alg,
            "fast_open": False
        }
        with open(path, 'w') as f:
            json.dump(config, f)
