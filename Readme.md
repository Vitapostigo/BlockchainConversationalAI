# Blockchain Conversational AI - MCP Endpoint Server

![Blockchain](https://img.shields.io/badge/Blockchain-Bitcoin-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-Python-green) ![Docker](https://img.shields.io/badge/Docker-Containers-blue)

Este proyecto es un **servidor MCP (Multi-Tool Communication Protocol) basado en FastAPI** que expone endpoints para interactuar con la **blockchain de Bitcoin** y con un nodo Fulcrum. Está diseñado para ser utilizado como backend para herramientas y sistemas que necesiten consultar información sobre transacciones, bloques, mempool y balances de manera estructurada y segura.

---

## 📌 Objetivo del proyecto

El servidor actúa como un **expositor de endpoints MCP**:

- Proporciona acceso a información de **Bitcoin Mainnet** a través de un nodo RPC.
- Consulta información histórica y balances de direcciones usando un **nodo Fulcrum**.
- Exposición de endpoints claros y documentados para herramientas de análisis de blockchain.
- Integración lista para **Docker**, con configuración de credenciales mediante variables de entorno.

## ⚙️ Configuración de credenciales

Todas las credenciales sensibles deben almacenarse en un archivo `.env` **fuera del repositorio**:

,env
# Nodo Bitcoin RPC
MAINNET_USER=mainnet
MAINNET_PASS=TU_PASSWORD
MAINNET_HOST=localhost
MAINNET_PORT=8332

Para generarlas, usar: https://github.com/bitcoin/bitcoin/blob/master/share/rpcauth/rpcauth.py

🔹 Endpoints disponibles

El servidor expone endpoints MCP que pueden ser consumidos por herramientas o sistemas automatizados.
Endpoints de nodo Bitcoin
Endpoint	Método	Descripción
/BitcoinGetBlockchainInfo	GET	Información general del blockchain (altura, dificultad, headers, etc.).
/BitcoinGetP2PNodeInfo	GET	Estado del nodo Bitcoin, versión, conexiones, protocolos.
/BitcoinGetBlockHashByHeight	POST	Hash de un bloque por altura (height).
/BitcoinGetMempoolInfo	GET	Información sobre la mempool activa de transacciones.
/BitcoinGetChainTxStats	POST	Estadísticas de transacciones en un rango de bloques (nblocks, blockhash).
/BitcoinEstimateSmartFee	GET	Estimación de fee por KB para confirmación rápida.
/BitcoinGetBlock	POST	Información de un bloque específico y sus transacciones (blockhash).
/BitcoinGetTransaction	POST	Información completa de una transacción (txid).
Endpoints de nodo Fulcrum
Endpoint	Método	Descripción
/BitcoinGetBalance	POST	Devuelve el balance de una dirección Bitcoin (address).
/BitcoinGetAddressFirstUse	POST	Primera transacción asociada a una dirección (address).
/BitcoinGetHistory	POST	Historial completo de transacciones de una dirección (address).
/BitcoinGetBlockFromTransaction	POST	Altura del bloque que contiene una transacción (txid).

Para construir el contenedor:
docker build --no-cache -t mcpserver-app .

Para lanzarlo:
docker run -d --rm --name mcpserver --env-file .env --network host mcpserver-app

Se usará como parte de un stack que levantará varios proyecto creando una red para las comunicaciones. Por tanto el --network host es temporal.