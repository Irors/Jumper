from core.other import wallet_reader, add_logger, sleep_module, interface
from data.settings import Config, JumperBridgeSettings, Maker
from jumper import Jumper


class Client:
    def __init__(self, private_key, network_from, network_to, _logger):
        self.private_key = private_key
        self.network_from = network_from
        self.network_to = network_to
        self.settings = JumperBridgeSettings()
        self.config = Config()
        self.logger = _logger


def set_up():
    return JumperBridgeSettings(), Config(), add_logger(), Maker()


def start_module(_client):
    jumper = Jumper(client=_client, logger=client.logger, settings=client.settings, config=_client.config, maker=maker)

    interface(
        _len=_len,
        network_from=pre_settings.network_from,
        network_to=pre_settings.network_to,
        config=pre_config,
        token_from=jumper.get_symbol(client.settings.fromTokenAddress),
        token_to=jumper.get_symbol(client.settings.toTokenAddress)
    )

    jumper.pre_bridge()
    jumper.bridge()


if __name__ == "__main__":
    pre_settings, pre_config, logger, maker = set_up()
    accounts, _len = wallet_reader(shuffle=pre_config.shuffle_wallet)


    clients = [Client(private_key=private_key,
                      network_from=pre_settings.network_from,
                      network_to=pre_settings.network_to,
                      _logger=logger) for private_key in accounts]

    for client in clients:
        try:
            start_module(_client=client)
            sleep_module(config=pre_config)

            with open(rf'data\result\success.txt', 'a+') as file:
                datas = [i.strip() for i in file]
                if datas.count(client.private_key) == 0:
                    file.write(f'{client.private_key}\n')

        except Exception as err:
            with open(rf'data\result\failure.txt', 'a+') as file:
                datas = [i.strip() for i in file]
                if datas.count(client.private_key) == 0:
                    file.write(f'{client.private_key}\n')
            logger.error(err)
