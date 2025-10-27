from asyncio import sleep
import hashlib
import json
import socket
import requests
from bitcoinlib.transactions import Output
import os
########################################CREDENCIALES NODO########################################
def getMainnetClient():
    user = os.getenv("MAINNET_USER")
    password = os.getenv("MAINNET_PASS")
    host = "bitcoin_mainnet"
    port = "8332"
    address = f"http://{user}:{password}@{host}:{port}"
    print(address)
    return address
########################################CREDENCIALES NODO########################################
#######################################CREDENCIALES FULCRUM######################################
def getFulcrumIp():
    return "fulcrum_mainnet"
def getFulcrumPort():
    return 50001
#######################################CREDENCIALES FULCRUM######################################
#################################################################################################
def precio_bitcoin():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return str(data['bitcoin']['usd'])
#################################################################################################
async def consultaFulcrum(host, port, content, retries=2, delay=1):
    """Consulta un nodo Fulcrum de forma segura con retry y espera dinámica."""
    message = json.dumps(content).encode('utf-8') + b'\n'

    for attempt in range(retries):
        try:
            reader, writer = await asyncio.open_connection(host, port)
            writer.write(message)
            await writer.drain()

            try:
                data = await asyncio.wait_for(reader.read(65536), timeout=5)
            except asyncio.TimeoutError:
                data = b''

            writer.close()
            await writer.wait_closed()

            if data:
                return data.decode()

            print(f"[Intento {attempt+1}] Respuesta vacía, reintentando...")
            await asyncio.sleep(delay)

        except Exception as e:
            print(f"[Intento {attempt+1}] Error: {e}")
            await asyncio.sleep(delay)

    return None
#################################################################################################
def addr2scripthash(address):
    script = Output(0, address).script
    script_bytes = script.serialize()
    hash_value = hashlib.sha256(script_bytes).digest()
    reversed_hash = hash_value[::-1]
    return reversed_hash.hex()
#################################################################################################
def descripcionGetInfo():
    return """{                                         (json object)
        "chain" : "str",                        (string) current network name (main, test, regtest)
        "blocks" : n,                           (numeric) the height of the most-work fully-validated chain. The genesis block has height 0
        "headers" : n,                          (numeric) the current number of headers we have validated
        "bestblockhash" : "str",                (string) the hash of the currently best block
        "difficulty" : n,                       (numeric) the current difficulty
        "mediantime" : n,                       (numeric) median time for the current best block
        "verificationprogress" : n,             (numeric) estimate of verification progress [0..1]
        "initialblockdownload" : true|false,    (boolean) (debug information) estimate of whether this node is in Initial Block Download mode
        "chainwork" : "hex",                    (string) total amount of work in active chain, in hexadecimal
        "size_on_disk" : n,                     (numeric) the estimated size of the block and undo files on disk
        "pruned" : true|false,                  (boolean) if the blocks are subject to pruning
        "pruneheight" : n,                      (numeric) lowest-height complete block stored (only present if pruning is enabled)
        "automatic_pruning" : true|false,       (boolean) whether automatic pruning is enabled (only present if pruning is enabled)
        "prune_target_size" : n,                (numeric) the target size used by pruning (only present if automatic pruning is enabled)
        "softforks" : {                         (json object) status of softforks
            "xxxx" : {                            (json object) name of the softfork
            "type" : "str",                     (string) one of "buried", "bip9"
            "bip9" : {                          (json object) status of bip9 softforks (only for "bip9" type)
                "status" : "str",                 (string) one of "defined", "started", "locked_in", "active", "failed"
                "bit" : n,                        (numeric) the bit (0-28) in the block version field used to signal this softfork (only for "started" status)
                "start_time" : xxx,               (numeric) the minimum median time past of a block at which the bit gains its meaning
                "timeout" : xxx,                  (numeric) the median time past of a block at which the deployment is considered failed if not yet locked in
                "since" : n,                      (numeric) height of the first block to which the status applies
                "statistics" : {                  (json object) numeric statistics about BIP9 signalling for a softfork (only for "started" status)
                "period" : n,                   (numeric) the length in blocks of the BIP9 signalling period
                "threshold" : n,                (numeric) the number of blocks with the version bit set required to activate the feature
                "elapsed" : n,                  (numeric) the number of blocks elapsed since the beginning of the current period
                "count" : n,                    (numeric) the number of blocks with the version bit set in the current period
                "possible" : true|false         (boolean) returns false if there are not enough blocks left in this period to pass activation threshold
                }
            },
            "height" : n,                       (numeric) height of the first block which the rules are or will be enforced (only for "buried" type, or "bip9" type with "active" status)
            "active" : true|false               (boolean) true if the rules are enforced for the mempool and the next block
            },
            ...
        },
        "warnings" : "str"                      (string) any network and blockchain warnings
    }"""
#################################################################################################
def descripcionGetNetwork():
    return """{                            (json object)
            "loaded" : true|false,     (boolean) True if the mempool is fully loaded
            "size" : n,                (numeric) Current tx count
            "bytes" : n,               (numeric) Sum of all virtual transaction sizes as defined in BIP 141. Differs from actual serialized size because witness data is discounted
            "usage" : n,               (numeric) Total memory usage for the mempool
            "maxmempool" : n,          (numeric) Maximum memory usage for the mempool
            "mempoolminfee" : n,       (numeric) Minimum fee rate in BTC/kB for tx to be accepted. Is the maximum of minrelaytxfee and minimum mempool fee
            "minrelaytxfee" : n,       (numeric) Current minimum relay fee for transactions
            "unbroadcastcount" : n     (numeric) Current number of transactions that haven't passed initial broadcast yet
        }"""
#################################################################################################
def descripcionGetMempoolInfo():
    return """{                            (json object)
        "loaded" : true|false,     (boolean) True if the mempool is fully loaded
        "size" : n,                (numeric) Current tx count
        "bytes" : n,               (numeric) Sum of all virtual transaction sizes as defined in BIP 141. Differs from actual serialized size because witness data is discounted
        "usage" : n,               (numeric) Total memory usage for the mempool
        "maxmempool" : n,          (numeric) Maximum memory usage for the mempool
        "mempoolminfee" : n,       (numeric) Minimum fee rate in BTC/kB for tx to be accepted. Is the maximum of minrelaytxfee and minimum mempool fee
        "minrelaytxfee" : n,       (numeric) Current minimum relay fee for transactions
        "unbroadcastcount" : n     (numeric) Current number of transactions that haven't passed initial broadcast yet
    }"""
#################################################################################################
def descripcionGetChainTxStats():
    return """{                                       (json object)
        "time" : xxx,                         (numeric) The timestamp for the final block in the window, expressed in UNIX epoch time
        "txcount" : n,                        (numeric) The total number of transactions in the chain up to that point
        "window_final_block_hash" : "hex",    (string) The hash of the final block in the window
        "window_final_block_height" : n,      (numeric) The height of the final block in the window.
        "window_block_count" : n,             (numeric) Size of the window in number of blocks
        "window_tx_count" : n,                (numeric) The number of transactions in the window. Only returned if "window_block_count" is > 0
        "window_interval" : n,                (numeric) The elapsed time in the window in seconds. Only returned if "window_block_count" is > 0
        "txrate" : n                          (numeric) The average rate of transactions per second in the window. Only returned if "window_interval" is > 0
    }"""
#################################################################################################
def descripcionEstimateSmartFee():
    return """{           (json object)
        "feerate" : n,    (numeric, optional) estimate fee rate in BTC/kB (only present if no errors were encountered)
        "errors" : [      (json array, optional) Errors encountered during processing (if there are any)
            "str",          (string) error
            ...
        ],
        "blocks" : n      (numeric) block number where estimate was found
                            The request target will be clamped between 2 and the highest target
                            fee estimation is able to return based on how long it has been running.
                            An error is returned if not enough transactions and blocks
                            have been observed to make an estimate for any number of blocks.
    }"""
#################################################################################################
def getDescripcionGetBlock():
    return """{                                 (json object)
        "hash" : "hex",                 (string) the block hash (same as provided)
        "confirmations" : n,            (numeric) The number of confirmations, or -1 if the block is not on the main chain
        "size" : n,                     (numeric) The block size
        "strippedsize" : n,             (numeric) The block size excluding witness data
        "weight" : n,                   (numeric) The block weight as defined in BIP 141
        "height" : n,                   (numeric) The block height or index
        "version" : n,                  (numeric) The block version
        "versionHex" : "hex",           (string) The block version formatted in hexadecimal
        "merkleroot" : "hex",           (string) The merkle root
        "tx" : [                        (json array) The transaction ids
            "hex",                        (string) The transaction id
            ...
        ],
        "time" : xxx,                   (numeric) The block time expressed in UNIX epoch time
        "mediantime" : xxx,             (numeric) The median block time expressed in UNIX epoch time
        "nonce" : n,                    (numeric) The nonce
        "bits" : "hex",                 (string) The bits
        "difficulty" : n,               (numeric) The difficulty
        "chainwork" : "hex",            (string) Expected number of hashes required to produce the chain up to this block (in hex)
        "nTx" : n,                      (numeric) The number of transactions in the block
        "previousblockhash" : "hex",    (string) The hash of the previous block
        "nextblockhash" : "hex"         (string) The hash of the next block
    }"""
#################################################################################################
def getDescripcionGetTx ():
    return""" {                            (json object)
        "in_active_chain" : true|false,    (boolean) Whether specified block is in the active chain or not (only present with explicit "blockhash" argument)
        "hex" : "hex",                     (string) The serialized, hex-encoded data for 'txid'
        "txid" : "hex",                    (string) The transaction id (same as provided)
        "hash" : "hex",                    (string) The transaction hash (differs from txid for witness transactions)
        "size" : n,                        (numeric) The serialized transaction size
        "vsize" : n,                       (numeric) The virtual transaction size (differs from size for witness transactions)
        "weight" : n,                      (numeric) The transaction's weight (between vsize*4-3 and vsize*4)
        "version" : n,                     (numeric) The version
        "locktime" : xxx,                  (numeric) The lock time
        "vin" : [                          (json array)
            {                              (json object)
            "txid" : "hex",                (string) The transaction id
            "vout" : n,                    (numeric) The output number
            "scriptSig" : {                (json object) The script
                "asm" : "str",             (string) asm
                "hex" : "hex"              (string) hex
            },
            "sequence" : n,                (numeric) The script sequence number
            "txinwitness" : [              (json array)
                "hex",                     (string) hex-encoded witness data (if any)
                ...
            ]
            },
            ...
        ],
        "vout" : [                         (json array)
            {                              (json object)
            "value" : n,                   (numeric) The value in BTC
            "n" : n,                       (numeric) index
            "scriptPubKey" : {             (json object)
                "asm" : "str",             (string) the asm
                "hex" : "str",             (string) the hex
                "reqSigs" : n,             (numeric) The required sigs
                "type" : "str",            (string) The type, eg 'pubkeyhash'
                "addresses" : [            (json array)
                "str",                     (string) bitcoin address
                ...
                ]
            }
            },
            ...
        ],
        "blockhash" : "hex",               (string) the block hash
        "confirmations" : n,               (numeric) The confirmations
        "blocktime" : xxx,                 (numeric) The block time expressed in UNIX epoch time
        "time" : n                         (numeric) Same as "blocktime"
    }"""
