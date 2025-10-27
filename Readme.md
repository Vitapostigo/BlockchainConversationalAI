# Bitcoin Self Hosted MCP Endpoint Server

![Blockchain](https://img.shields.io/badge/Blockchain-Bitcoin-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-Python-green) ![Docker](https://img.shields.io/badge/Docker-Containers-blue)

Este proyecto es un **servidor MCP (Multi-Tool Communication Protocol) basado en FastAPI** que expone endpoints para interactuar con la **blockchain de Bitcoin** y con un nodo Fulcrum. Está diseñado para ser utilizado como backend para herramientas y sistemas que necesiten consultar información sobre transacciones, bloques, mempool y balances de manera estructurada y segura.
Para consultas, se puede importar en: https://mcp.vitadeb.com/docs. Actualmente sin contraseña.
---

## 📌 Objetivo del proyecto

El servidor actúa como un **expositor de endpoints MCP**:

- Proporciona acceso a información de **Bitcoin Mainnet** a través de un nodo RPC.
- Consulta información histórica y balances de direcciones usando un **nodo Fulcrum**.
- Exposición de endpoints claros y documentados para herramientas de análisis de blockchain.
- Integración lista para **Docker**, con configuración de credenciales mediante variables de entorno.

## ⚙️ Configuración de credenciales

Todas las credenciales sensibles deben almacenarse en un archivo `.env` **fuera del repositorio**:
Para consultar la estructura se proporciona .env.example.

Para generarlas, usar: https://github.com/bitcoin/bitcoin/blob/master/share/rpcauth/rpcauth.py

---

## 🐳 Despliegue completo con Docker Compose

El entorno completo puede levantarse fácilmente con **Docker Compose**, lo que permite ejecutar:

- Un nodo **Bitcoin Core** (Mainnet)
- Un nodo **Fulcrum**
- El servidor **MCP** basado en FastAPI (contenedor `mcpserver`)

Este archivo `docker-compose.yml` **está incluido en el repositorio** y está diseñado para trabajar con una red Docker compartida (`mcp_network`).

---

### 📦 Estructura del proyecto

.
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
├── requirements.txt
└── app/
├── mcpServer.py
└── ...


### ⚙️ Configuración previa

1. **Crear la red compartida** (solo la primera vez):

   ```bash
   docker network create mcp_network


🚀 Levantar el entorno
Para construir y ejecutar todos los servicios:

Descargar el Dockerfile.
Construir el contenedor con: docker build --no-cache -t mcpserver-app .


🧩 Servicios incluidos
🪙 Bitcoin Mainnet
Ejecuta un nodo completo de Bitcoin con txindex habilitado, permitiendo consultas RPC desde los demás servicios.

⚡ Fulcrum
Nodo indexador de alto rendimiento compatible con Electrum, conectado internamente al nodo Bitcoin.

🤖 MCP Server
Servidor FastAPI que expone endpoints para interactuar con la blockchain a través de Bitcoin Core y Fulcrum.

🌐 Acceso a la API
Una vez levantado el stack y los nodos estén sincronizados, se puede acceder a la documentación interactiva de la API:

👉 http://localhost:13333/docs

🧠 Notas adicionales
Los volúmenes locales definidos en docker-compose.yml son rutas genéricas (./data/...), puedes cambiarlas según tu entorno.

La red mcp_network permite comunicación interna entre contenedores sin exponer puertos RPC públicamente.

El servidor MCP es accesible solo a través del puerto 13333.

El modo --reload está pensado para desarrollo. En producción puede eliminarse o cambiarse a --workers N.

🔹 Endpoints disponibles

El servidor expone endpoints MCP que pueden ser consumidos por herramientas o sistemas automatizados.

/BitcoinGetBlockchainInfo	GET	Información general del blockchain (altura, dificultad, headers, etc.).

/BitcoinGetP2PNodeInfo	GET	Estado del nodo Bitcoin, versión, conexiones, protocolos.

/BitcoinGetBlockHashByHeight	POST	Hash de un bloque por altura (height).

/BitcoinGetMempoolInfo	GET	Información sobre la mempool activa de transacciones.

/BitcoinGetChainTxStats	POST	Estadísticas de transacciones en un rango de bloques (nblocks, blockhash).

/BitcoinEstimateSmartFee	GET	Estimación de fee por KB para confirmación rápida.

/BitcoinGetBlock	POST	Información de un bloque específico y sus transacciones (blockhash).

/BitcoinGetTransaction	POST	Información completa de una transacción (txid).

/BitcoinGetBalance	POST	Devuelve el balance de una dirección Bitcoin (address).

/BitcoinGetAddressFirstUse	POST	Primera transacción asociada a una dirección (address).

/BitcoinGetHistory	POST	Historial completo de transacciones de una dirección (address).

/BitcoinGetBlockFromTransaction	POST	Altura del bloque que contiene una transacción (txid).

Se usará como parte de un stack que levantará varios proyecto creando una red para las comunicaciones. Por tanto el --network host es temporal.

Para otros ver más de mis proyectos visita: https://vitadeb.com/
