import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

# Load RPC URL and private key from environment variables
RPC_URL = os.getenv('BLOCKCHAIN_RPC_URL')
PRIVATE_KEY = os.getenv('BLOCKCHAIN_PRIVATE_KEY')

if not RPC_URL:
    raise EnvironmentError('BLOCKCHAIN_RPC_URL not set in environment')

# Initialize Web3 instance
w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.isConnected():
    raise ConnectionError(f'Unable to connect to blockchain at {RPC_URL}')

# Account object for signing transactions
account = w3.eth.account.from_key(PRIVATE_KEY)
