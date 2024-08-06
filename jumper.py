import requests
import random
from core.eth import Web3Client


class Jumper(Web3Client):
    def __init__(self, client, logger, settings, config, maker):
        super().__init__(client=client, network=client.network_from, logger=logger, config=config)
        self.client = client
        self.maker = maker
        self.settings = settings
        self.data = None
        self.value = None
        self.to = None
        self.total_fee = None
        self.symbol_in = None
        self.symbol_out = None
        self.currency_in = None
        self.currency_out = None
        self.currency_out_usd = None
        self.currency_in_usd = None
        self.provider_fee_transaction = None


    def validate_balance(self):
        if self.settings.fromTokenAddress != '0x0000000000000000000000000000000000000000':
            if (int(self.convert_to_wei(self.config.if_the_minimum_account_balance_is_more_than)) >
                    int(self.get_balanceOf(contract=self.get_contract(address=self.settings.fromTokenAddress), validate=True))):
                raise Exception(f'[{self.address}] | Small balance')

            self.check_for_approved(
                token_address=self.settings.fromTokenAddress,
                spender_address=self.to,
                amount_in_wei=0,
                unlimited_approve=True)

            self.value = int(self.get_balanceOf(contract=self.get_contract(address=self.settings.fromTokenAddress), validate=False)
                             *
                             (random.randint(self.settings.amount_percentage[0],
                                             self.settings.amount_percentage[1]) / 100))

        else:
            if (int(self.convert_to_wei(self.config.if_the_minimum_account_balance_is_more_than)) >
                    int(self.web3.eth.get_balance(self.web3.to_checksum_address(self.address)))):
                raise Exception(f'[{self.address}] | Small balance')

            self.value = int(self.get_balance()
                             *
                             (random.randint(self.settings.amount_percentage[0],
                                             self.settings.amount_percentage[1]) / 100))

    def pre_bridge(self):
        self.logger.warning(f'Start Jumper bridge')
        self.to = self.web3.to_checksum_address(self.maker.address[self.client.network_from.name])

        self.validate_balance()
        router, fee = self.check_enabled_bridge()

        self.logger.info(f'Debank: https://debank.com/profile/{self.address}/history 📃')

        self.data = self.gather_data(json_data=router["steps"][0])

        self.total_fee = str(fee)
        self.symbol_in = router["steps"][0]["action"]["fromToken"]["name"]
        self.currency_in = str(float(self.convert_from_wei(int(router["fromAmount"]))))
        self.currency_in_usd = float(self.currency_in) * float(router["fromToken"]["priceUSD"])

        self.logger.info(f'[{self.address}] | make bridge | {self.currency_in[:7]}({self.currency_in_usd}$) {self.symbol_in} | fee: {self.total_fee[:7]}$ 🚀')

    def check_enabled_bridge(self):
        headers = {
            'x-lifi-integrator': 'jumper.exchange',
            'x-lifi-sdk': '3.1.3',
            'x-lifi-widget': '3.2.2',
        }

        json_data = {
            'fromAddress': self.address,
            'fromAmount': str(self.value),
            'fromChainId': self.client.network_from.chain_id,
            'fromTokenAddress': self.settings.fromTokenAddress,
            'toChainId': self.client.network_to.chain_id,
            'toTokenAddress': self.settings.toTokenAddress,
            'options': {
                'integrator': 'jumper.exchange',
                'order': 'CHEAPEST',
                'slippage': 0.005,
                'maxPriceImpact': 0.4,
                'allowSwitchChain': True,
            },
        }

        response = requests.post('https://li.quest/v1/advanced/routes', headers=headers, json=json_data).json()

        if len(response["routes"]) == 0:
            raise Exception(f'[{self.address}] | https://jumper.exchange/ | No router exchange :(')

        router = response["routes"][0]

        network_fee = float(router["gasCostUSD"])
        provider_fee = float(router["steps"][0]["estimate"]["feeCosts"][0]["amountUSD"])
        price_impact_fee = float(router["fromAmountUSD"]) - float(router["toAmountUSD"])
        self.provider_fee_transaction = int(router["steps"][0]["estimate"]["feeCosts"][0]["amount"])

        total_fee = network_fee + provider_fee + price_impact_fee

        return router, total_fee

    @staticmethod
    def gather_data(json_data):
        response = requests.post('https://li.quest/v1/advanced/stepTransaction', json=json_data).json()
        return response["transactionRequest"]["data"]

    def bridge(self):
        transaction = self.prepare_transaction(value=(int(self.value) if self.settings.fromTokenAddress == '0x0000000000000000000000000000000000000000' else self.provider_fee_transaction))
        transaction['data'] = self.data
        transaction['to'] = self.web3.to_checksum_address(self.to)

        submitted_transaction = self.transaction_runner(transaction=transaction)
        if submitted_transaction:
            self.logger.success(
                f'[{self.address}] | {self.network.explorer}tx/{submitted_transaction.hex()} Bridge success ✅')
