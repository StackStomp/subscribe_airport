import cmd
from typing import IO

from config_def import SubscriptionConfig, InboundConfig, ClientConfig


class Shell(cmd.Cmd):
    prompt = ">"

    def __init__(self):
        super().__init__()
        self.sub_config = SubscriptionConfig(None)
        self.inbound = InboundConfig("127.0.0.1", 1024, "socks5")
        self.client = ClientConfig("shadowsocks")

    def do_exit(self, _):
        """exit"""
        print("Bye")
        return True

    def do_show(self, _):
        """show current config"""
        print("{}\n{}\nClient: {}".format(self.sub_config, self.inbound, self.client))

    def do_sub(self, arg):
        """add a url subscription"""
        self.sub_config.sub_url = arg

    def do_client(self, arg):
        """set output config file of the target client type, current support shadowsocks"""
        support_clients = {"shadowsocks"}
        if arg not in support_clients:
            print("ERROR: only support {}".format(support_clients))
            return
        self.client.client_type = arg


if __name__ == "__main__":
    Shell().cmdloop()
