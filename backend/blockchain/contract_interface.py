import json
import os
from pathlib import Path
from dotenv import load_dotenv
from web3 import Web3
from .web3_client import w3, account

load_dotenv()

# Load compiled contract ABI and bytecode
CONTRACT_ABI_PATH = Path(__file__).parent / "PollutionRegistry_abi.json"
CONTRACT_BYTECODE_PATH = Path(__file__).parent / "PollutionRegistry_bytecode.txt"

if not CONTRACT_ABI_PATH.is_file():
    raise FileNotFoundError('Contract ABI file not found. Run the deployment script to generate it.')

with open(CONTRACT_ABI_PATH) as f:
    contract_abi = json.load(f)

# Load contract address from env
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
if not CONTRACT_ADDRESS:
    raise EnvironmentError('CONTRACT_ADDRESS not set in environment variables.')

# Create contract instance
contract = w3.eth.contract(address=Web3.toChecksumAddress(CONTRACT_ADDRESS), abi=contract_abi)

def log_report(report_hash: str) -> int:
    """Send a transaction to log a new pollution report hash.
    Returns the newly created report ID.
    """
    if not report_hash.startswith('0x'):
        raise ValueError('report_hash must be a hex string starting with 0x')
    txn = contract.functions.logReport(Web3.toBytes(hexstr=report_hash)).buildTransaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 200000,
        'gasPrice': w3.toWei('5', 'gwei')
    })
    signed_txn = account.sign_transaction(txn)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # The contract returns the reportId, which we can fetch from the event
    logs = contract.events.ReportLogged().processReceipt(receipt)
    if not logs:
        raise RuntimeError('No ReportLogged event found')
    return logs[0]['args']['reportId'], tx_hash.hex()

def verify_report(report_id: int) -> None:
    """Verify a report by its ID."""
    txn = contract.functions.verifyReport(report_id).buildTransaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 150000,
        'gasPrice': w3.toWei('5', 'gwei')
    })
    signed_txn = account.sign_transaction(txn)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return

def get_report(report_id: int):
    """Read‑only call to fetch report details."""
    return contract.functions.getReport(report_id).call()

def report_exists(report_hash: str):
    """Check if a report hash already exists on‑chain."""
    return contract.functions.reportHashExists(Web3.toBytes(hexstr=report_hash)).call()
