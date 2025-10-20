from utilidades import *
import bitcoinlib

def getFulcrumQuery(method,data):
    try:
        if method == 'getTx':
            return {
                "method": "blockchain.transaction.get",
                "params": [data, False],
                "id": 0
            }
        elif method == 'getBalance':
            return { #Data debera ser una direccion
                "method": "blockchain.scripthash.get_balance",
                "params": [addr2scripthash(data)],
                "id": 0
            }
        elif method == 'firstUse':
            return { #Data debera ser una direccion
                "method": "blockchain.scripthash.get_first_use",
                "params": [addr2scripthash(data)],
                "id": 0
            }
        elif method == 'getHistory':
            return { #Data debera ser una direccion
                "method": "blockchain.scripthash.get_history",
                "params": [addr2scripthash(data),0,-1],
                "id": 0
            }
        elif method == 'blockFromTx':
            return { #Data debera ser una transacción
                "method": "blockchain.transaction.get_height",
                "params": [data],
                "id": 0
            }
        else:
            return {}

    except bitcoinlib.encoding.EncodingError as e:
        return {}

async def get_balance(address: str):
    """Devuelve el balance asociado a una dirección."""
    try:
        return await consultaFulcrum(getFulcrumIp(), getFulcrumPort(), getFulcrumQuery("getBalance", address))
    except Exception as e:
        return {"error": str(e)}

async def get_first_use(address: str):
    """Devuelve la primera transacción donde se utilizó una dirección."""
    try:
        return await consultaFulcrum(getFulcrumIp(), getFulcrumPort(), getFulcrumQuery("firstUse", address))
    except Exception as e:
        return {"error": str(e)}

async def get_history(address: str):
    """Devuelve el historial completo de transacciones asociadas a una dirección."""
    try:
        return await consultaFulcrum(getFulcrumIp(), getFulcrumPort(), getFulcrumQuery("getHistory", address))
    except Exception as e:
        return {"error": str(e)}

async def block_from_tx(txid: str):
    """Devuelve la altura del bloque donde se encuentra una transacción."""
    try:
        return await consultaFulcrum(getFulcrumIp(), getFulcrumPort(), getFulcrumQuery("blockFromTx", txid))
    except Exception as e:
        return {"error": str(e)}