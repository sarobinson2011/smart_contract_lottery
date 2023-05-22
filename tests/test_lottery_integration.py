import pytest, time
from brownie import network, config
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_NETWORKS,
    fund_with_link,
)
from scripts.deploy_lottery import deploy_lottery


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    print(f"Lottery deployed & started from account: {account} ")
    # first lottery entry
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 1000})
    # second lottery entry
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 1000})
    # fund the lottery deployed contract with LINK tokens
    fund_with_link(lottery)
    # WAIT for Chainlink node to respond to request
    print("\nWaiting for response from Chainlink node...")
    time.sleep(60)
    print(f"New lottery balance (should be zero) is: {lottery.balance()}")
    print(f"{lottery.recentWinner()} is the new winner!")
    # assert lottery.recentWinner() == account
    # assert lottery.balance() == 0
    lottery.endLottery({"from": account})
    # gas_limit = 2000000
    # lottery.endLottery({"from": account, "gasLimit": gas_limit})
