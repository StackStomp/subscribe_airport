
class SubscriptionConfig:
    def __init__(self, sub_url):
        self.sub_url = sub_url

    def __str__(self):
        return f"Subscription URL: {self.sub_url}"


class InboundConfig:
    def __init__(self, ip, port, proxy):
        self.ip = ip
        self.port = port
        self.proxy = proxy

    def __str__(self):
        return f"Inbound ip: {self.ip}, port: {self.port}, type: {self.proxy}"


class ClientConfig:
    def __init__(self, client_type):
        self.client_type = client_type

    def __str__(self):
        return f"Client type: {self.client_type}"
