from brownie import interface


def main():
    link_token_address = "0x779877A7B0D9E8603169DdbD7836e478b4624789"
    account_address = "0x78FD9b0150bd25741661E753878aC2C62a9c55b3"

    link_token = interface.LinkTokenInterface(link_token_address)
    balance = link_token.balanceOf(account_address)

    print(f"\nLINK token balance: {balance}\n")
