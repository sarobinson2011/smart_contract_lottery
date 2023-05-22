from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_NETWORKS,
    get_account,
    get_contract,
    fund_with_link,
)
from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest


def test_get_entrance_fee():

    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip()

    #  Arrange
    lottery = deploy_lottery()
    # Act
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    #  Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip()
    lottery = deploy_lottery()
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    # Act
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Assert
    assert lottery.players(0) == account


def test_can_end_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Act
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    # Assert
    assert lottery.lottery_state() == 2


""" Final unit test  -->  start from 8:01:06 """


def test_can_pick_winner_correctly():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]

    # -->  simulate a dummy response back from Chainlink node
    STATIC_RNG = 779
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )

    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    #  779 % 3 = 1  -->  so  --> account(1)
    assert lottery.recentWinner() == get_account(index=2)
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery
