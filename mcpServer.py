from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional

import consultasFulcrum
from consultasNodo import *
from utilidades import *

app = FastAPI(title="Server_MCP", version="1.0.1")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ToolCall(BaseModel):
    arguments: Dict[str, Any] = {}

@app.get("/tools")
def list_tools():
    """List the available tools."""
    return {
        "tools": [
            {
                "name": "BitcoinGetBlockchainInfo",
                "description": f"Returns general information about the Bitcoin mainnet Blockchain, including chain name, size in MBs, size in blocks (height), difficulty, etc...",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "BitcoinGetP2PNodeInfo",
                "description": f"Returns information related to the p2p Bitcoin mainnet node server current status.",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "BitcoinGetBlockHashByHeight",
                "description": "Returns the hash of the block at the given height in the Bitcoin mainnet.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "height": {"type": "integer", "description": "Block height."}
                    },
                    "required": ["height"]
                }
            },
            {
                "name": "BitcoinGetMempoolInfo",
                "description": f"Returns details on the active state of the Bitcoin's mainnet transactions memory pool.",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            },
            {
                "name": "BitcoinGetChainTxStats",
                "description": f"Compute statistics about the total number and rate of transactions in Bitcoin's mainnet Blockchain over a time window.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "nblocks": {"type": "integer", "description": "nblocks: Size of the window in number of blocks. Optional, default=one month"},
                        "blockhash": {"type": "string", "description": "blockhash: The hash of the block that ends the window. Optional, default=chain tip"}
                    },
                    "required": []
                }
            },
            {
                "name": "BitcoinEstimateSmartFee",
                "description": f"Estimates the approximate fee per kilobyte needed for a transaction to begin confirmation within conf_target blocks if possible and return the number of blocks for which the estimate is valid.",
                "inputSchema": {"type": "object", "properties": {}, "required": []
                }
                
            },
            {
                "name": "BitcoinGetBlock",
                "description": f"Returns information related to a block in Bitcoin's mainnet and a list of the transactions that block contains.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "blockhash": {"type": "string", "description": "The block hash."}
                    },
                    "required": ["blockhash"]
                }
            },
            {
                "name": "BitcoinGetTransaction",
                "description": f"Returns detailed information about a transaction in the Bitcoin's mainnet. In addition, some extra context may be provided such as the transaction issuer.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "txid": {
                            "type": "string",
                            "description": "Transaction ID (txid) of the transaction to retrieve."
                        }
                    },
                    "required": ["txid"]
                }
            },
            {
                "name": "BitcoinGetBalance",
                "description": "Returns the balance associated with a Bitcoin's mainnet address.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"address": {"type": "string", "description": "Bitcoin's mainnet address."}},
                    "required": ["address"]
                }
            },
            {
                "name": "BitcoinGetAddressFirstUse",
                "description": "Returns the first transaction of the given Bitcoin's mainnet address.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"address": {"type": "string", "description": "Bitcoin's mainnet address."}},
                    "required": ["address"]
                }
            },
            {
                "name": "BitcoinGetHistory",
                "description": "Returns all the transaction made in Bitcoin's mainnet for a given address.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"address": {"type": "string", "description": "Bitcoin's mainnet address."}},
                    "required": ["address"]
                }
            },
            {
                "name": "BitcoinGetBlockFromTransaction",
                "description": "For a given Bitcoin mainnet transaction, returns the block height of the block that contains that transaction.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"txid": {"type": "string", "description": "Transaction id (txid)"}},
                    "required": ["txid"]
                }
            }
        ]
    }
###############################CONSULTAS AL NODO DE BITCOIN##############################
@app.get("/BitcoinGetBlockchainInfo")
def BitcoinGetBlockchainInfo():
    "Returns general information about the Bitcoin mainnet Blockchain, including chain name, size in MBs, size in blocks (height), difficulty, etc..."
    return {"content": [{"type": "text", "text": str(infoBlockchain())}]}

@app.get("/BitcoinGetP2PNodeInfo")
def BitcoinGetP2PNodeInfo():
    "Returns information related to the p2p Bitcoin mainnet node server current status."
    return {"content": [{"type": "text", "text": str(infoRed())}]}

@app.post("/BitcoinGetBlockHashByHeight")
def BitcoinGetBlockHashByHeight(height: Optional[int] = None):
    "Returns the hash of the block at the given height in the Bitcoin mainnet."
    if height is None:
        return {"content": [{"type": "text", "text": "Por favor, proporciona el parámetro 'height' (altura del bloque)"}]}
    
    return {"content": [{"type": "text", "text": str(getblockhash(height))}]}

@app.get("/BitcoinGetMempoolInfo")
def BitcoinGetMempoolInfo():
    "Returns details on the active state of the Bitcoin's mainnet transactions memory pool."
    return {"content": [{"type": "text", "text": str(mempoolinfo())}]}

@app.post("/BitcoinGetChainTxStats")
def BitcoinGetChainTxStats(nblocks: Optional[int] = None, blockhash: Optional[str] = None):
    "Compute statistics about the total number and rate of transactions in Bitcoin's mainnet Blockchain over a time window."
    if nblocks is None and blockhash is None:
        return {"content": [{"type": "text", "text": "Por favor, proporciona al menos uno de los parámetros: 'nblocks' o 'blockhash'"}]}
    
    return {"content": [{"type": "text", "text": str(getchaintxstats(nblocks, blockhash))}]}

@app.get("/BitcoinEstimateSmartFee")
def BitcoinEstimateSmartFee():
    "Estimates the approximate fee per kilobyte needed for a transaction to begin confirmation within conf_target blocks if possible and return the number of blocks for which the estimate is valid."
    return {"content": [{"type": "text", "text": str(estimatesmartfee())}]}

@app.post("/BitcoinGetBlock")
def BitcoinGetBlock(blockhash: Optional[str] = None):
    "Returns information related to a block in Bitcoin's mainnet and a list of the transactions that block contains."
    if  blockhash is None:
        return {"content": [{"type": "text", "text": "Por favor, proporciona el 'blockhash'"}]}
    return {"content": [{"type": "text", "text": str(bloqueInfo(blockhash))}]}

@app.post("/BitcoinGetTransaction")
async def BitcoinGetTransaction(txid: str):
    "Returns detailed information about a transaction in the Bitcoin's mainnet. In addition, some extra context may be provided such as the transaction issuer."
    if not txid:
        return {"content": [{"type": "text", "text": "Por favor proporciona el txid"}]}
    return {"content": [{"type": "json", "json": str(infoTransaccion(txid))}]}
#####################HASTA AQUI LAS CONSULTAS VAN AL NODO DE BITCOIN#####################
###################A PARTIR DE AQUI LAS CONSULTAS FUNCIONAN EN FULCRUM###################
@app.post("/BitcoinGetBalance")
async def BitcoinGetBalance(address: str):
    "Returns the balance associated with a Bitcoin's mainnet address."
    if not address:
        return {"content": [{"type": "text", "text": "Por favor proporciona la dirección"}]}
    retorno = await consultasFulcrum.get_balance(address)
    return {"content": [{"type": "json", "json": str(retorno)}]}

@app.post("/BitcoinGetAddressFirstUse")
async def BitcoinGetAddressFirstUse(address: str):
    "Returns the first transaction of the given Bitcoin's mainnet address."
    if not address:
        return {"content": [{"type": "text", "text": "Por favor proporciona la dirección"}]}
    retorno = await consultasFulcrum.get_first_use(address)
    return {"content": [{"type": "json", "json": str(retorno)}]}

@app.post("/BitcoinGetHistory")
async def BitcoinGetHistory(address: str):
    "Returns all the transaction made in Bitcoin's mainnet for a given address."
    if not address:
        return {"content": [{"type": "text", "text": "Por favor proporciona la dirección"}]}
    retorno = await consultasFulcrum.get_history(address)
    return {"content": [{"type": "json", "json": str(retorno)}]}

@app.post("/BitcoinGetBlockFromTransaction")
async def BitcoinGetBlockFromTransaction(txid: str):
    "For a given Bitcoin mainnet transaction, returns the block height of the block that contains that transaction."
    if not txid:
        return {"content": [{"type": "text", "text": "Por favor proporciona el txid"}]}
    retorno = await consultasFulcrum.block_from_tx(txid)
    return {"content": [{"type": "json", "json": str(retorno)}]}
###################HASTA AQUI LAS CONSULTAS FUNCIONAN EN FULCRUM###################