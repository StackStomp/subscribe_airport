import cmd

from config_def import SubscriptionConfig, InboundConfig, ClientConfig
from generator_ss import SsGenerator
from subscriber_ss import SsSubscriber


class Shell(cmd.Cmd):
    prompt = ">"

    def __init__(self):
        super().__init__()
        self.sub_config = SubscriptionConfig(None)
        self.inbound = InboundConfig("127.0.0.1", 1024, "socks5")
        self.client = ClientConfig("shadowsocks")
        self.outbounds = []

    def do_exit(self, _):
        """exit"""
        print("Bye")
        return True

    def _show_outbounds(self):
        print("Subscription items:")
        for idx, outbound in enumerate(self.outbounds):
            print("Index {}: {}".format(idx, outbound))

    def do_show(self, _):
        """show current config"""
        print("{}\n{}\nClient: {}".format(self.sub_config, self.inbound, self.client))
        if len(self.outbounds) > 0:
            self._show_outbounds()

    def do_sub(self, arg):
        """Subscript a url"""
        self.sub_config.sub_url = arg
        self.outbounds = SsSubscriber(arg).pull()
        self._show_outbounds()

    def do_client(self, arg):
        """set output config file of the target client type, current support shadowsocks"""
        support_clients = {"shadowsocks"}
        if arg not in support_clients:
            print("ERROR: only support {}".format(support_clients))
            return
        self.client.client_type = arg

    def do_gen_ss(self, arg):
        """generate config file for sslocal(shadowsocks).
arg format: <subscription-item-index> </path/to/config/file.json>.
You can see all indexes using command: show"""
        if len(self.outbounds) == 0:
            print("ERROR: no outbounds found, pull subscription url first")
            return
        index, path = arg.split()
        index = int(index)
        SsGenerator(self.inbound, self.outbounds[index]).generate(path)


if __name__ == "__main__":
    Shell().cmdloop()
