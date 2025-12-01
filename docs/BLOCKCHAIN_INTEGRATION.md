# Blockchain Integration Guide

## Overview
This document explains how to set up and use the blockchain component of the **AQUA Guardian** project. It covers:
- Required environment variables
- Deploying the `PollutionRegistry` smart contract
- Using the FastAPI blockchain endpoints
- Verifying transactions on a testnet explorer

---

## 1. Environment Variables
Create a `.env` file in the project root (or copy the provided template) with the following keys:
```
# Blockchain configuration
BLOCKCHAIN_NETWORK=polygon_mumbai   # or goerli, sepolia, etc.
BLOCKCHAIN_RPC_URL=https://polygon-mumbai.g.alchemy.com/v2/your-api-key
BLOCKCHAIN_PRIVATE_KEY=0xYOUR_PRIVATE_KEY
# After deployment, the script will add CONTRACT_ADDRESS automatically
```
**Important:** Keep the private key secret! Do not commit `.env` to version control.

---

## 2. Deploy the Smart Contract
Run the deployment script to compile and deploy `PollutionRegistry.sol`:
```bash
cd backend/blockchain
python deploy_contract.py
```
The script will:
1. Install Solidity compiler `0.8.19` (if not already installed).
2. Compile the contract and generate `PollutionRegistry_abi.json` and `PollutionRegistry_bytecode.txt`.
3. Deploy the contract to the network defined by `BLOCKCHAIN_RPC_URL`.
4. Append the resulting `CONTRACT_ADDRESS` to your `.env` file.

After a successful run you should see output similar to:
```
Deploying contract... tx hash: 0xabc123...
Contract deployed at address: 0xdef456...
Deployment complete. CONTRACT_ADDRESS added to .env
```
You can verify the deployment on the appropriate testnet explorer (e.g., Polygonscan for Mumbai).

---

## 3. FastAPI Blockchain Endpoints
The backend now includes a new router under `/blockchain`.
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/blockchain/log` | Submit a report hash (`0x...`) to the contract. Returns the on‑chain `report_id`. |
| `POST` | `/blockchain/verify` | Verify a report by its `report_id`. |
| `GET` | `/blockchain/report/{report_id}` | Retrieve report details from the contract. |
| `GET` | `/blockchain/hash_exists/{report_hash}` | Check if a hash already exists on‑chain; returns `{exists, report_id}`. |

All endpoints return JSON and raise `HTTPException` with a clear error message on failure.

---

## 4. Using the Endpoints (Example with `curl`)
```bash
# Log a new report hash
curl -X POST http://localhost:8000/blockchain/log \
  -H "Content-Type: application/json" \
  -d '{"report_hash": "0x1234abcd..."}'

# Verify a report (id = 1)
curl -X POST http://localhost:8000/blockchain/verify \
  -H "Content-Type: application/json" \
  -d '{"report_id": 1}'
```

---

## 5. Troubleshooting
- **Connection errors** – Ensure `BLOCKCHAIN_RPC_URL` points to a reachable node and your internet connection is stable.
- **Insufficient funds** – The deploying account must have testnet ETH/MATIC. Use a faucet for the chosen network.
- **Contract address not set** – After deployment, verify that `CONTRACT_ADDRESS` was appended to `.env`. If not, add it manually.
- **Transaction failures** – Check gas limits and gas price; the script uses `5 gwei` by default, which is sufficient on most testnets.

---

## 6. Next Steps
1. Deploy the contract (see step 2).<br>
2. Update your frontend to call the new blockchain endpoints if you wish to display on‑chain verification status.<br>
3. Consider moving the deployment script to a CI/CD pipeline for automated releases.

---

*Generated on `$(date)`*
