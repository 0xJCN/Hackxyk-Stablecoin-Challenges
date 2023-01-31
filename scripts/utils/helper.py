from ape import chain
import subprocess

MAX_UINT256 = 2**256 - 1
w3 = chain.provider.web3

balance_call = "balanceOf(address)(uint256)"
transfer_call = "transfer(address,uint256)(bool)"


def fork(block_number):
    chain.provider.reset_fork(block_number)


def get_storage(account, slot):
    return chain.provider.get_storage_at(account, slot).hex()


def set_balance(account, amount):
    chain.set_balance(account, amount)


def time_travel(time_in_seconds):
    time = chain.pending_timestamp + time_in_seconds
    chain.mine(1, time)


def get_balance(account):
    return chain.provider.get_balance(account)


def get_code(account):
    return chain.provider.get_code(w3.toChecksumAddress(account)).hex()


def get_timestamp():
    return chain.pending_timestamp


def get_block():
    return chain.blocks[-1].number


def send_tx(recipient, calldata):
    w3.eth.default_account = w3.eth.accounts[0]
    tx = w3.eth.send_transaction(dict(to=recipient, data=calldata))
    return w3.eth.wait_for_transaction_receipt(tx)


def impersonate(account):
    subprocess.run(
        ["cast", "rpc", "anvil_impersonateAccount", f"{account}"],
        capture_output=True,
    )


def balance_of(token, owner):
    return int(
        subprocess.run(
            ["cast", "call", f"{token}", f"{balance_call}", f"{owner}"],
            capture_output=True,
            text=True,
        ).stdout[:-1]
    )


def transfer_from(token, sender, to, amount):
    subprocess.run(
        [
            "cast",
            "send",
            f"{token}",
            "--from",
            f"{sender}",
            f"{transfer_call}",
            f"{to}",
            f"{amount}",
        ],
        capture_output=True,
    )
