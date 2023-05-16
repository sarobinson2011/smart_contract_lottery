#   entrance_fee = $50
#   eth_price = $1800 (ish)
#
#   entrance_fee(eth) = 50/1800 = 0.027 eth
#   0.027 eth = 27000000000000000 wei

from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    # assert lottery.getEntranceFee() > Web3.toWei(0.025, "ether")
    # assert lottery.getEntranceFee() < Web3.toWei(0.029, "ether")
