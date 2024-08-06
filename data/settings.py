from .network import *


class Config:
    sleep = [22, 66]
    gas_price_multiplier = 2
    gas_limit_multiplier = 2
    shuffle_wallet = True
    if_the_minimum_account_balance_is_more_than = 0.001  # Если баланс аккаунта меньше указанного числа, то вывод средств выполнятся не будет


class JumperBridgeSettings:
    """
    Chain
    тут перечислены только часто используемые сети
    Chain #42161 Arbitrum

    Chain #42170 Arbitrum Nova

    Chain #8453 Base

    Chain #81457 Blast

    Chain #1 Ethereum

    Chain #59144 Linea

    Chain #10 Optimism

    Chain #534352 Scroll

    Chain #324 zkSync Era
    """

    network_from = OptimismRPC
    network_to = ArbitrumRPC

    fromTokenAddress = '0x4200000000000000000000000000000000000006'
    toTokenAddress = '0x0000000000000000000000000000000000000000'

    amount_percentage = [100, 100]


class Maker:
    address = {
        'Scroll': '0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE',
        'BNB Chain': '0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE',
        'Optimism': '0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE',
        'Arbitrum': '0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE',

        'Arbitrum Nova': '0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE',
        'Polygon': '0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE',
        'Avalanche': '0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE',
        'Ethereum': '0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE',

        'zkSync': '0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE',
        'Linea': '0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE',
        'Base': '0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE',
    }
