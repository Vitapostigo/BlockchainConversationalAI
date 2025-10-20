import requests
from utilidades import getMainnetClient
from bitcoinrpc.authproxy import AuthServiceProxy

########################################INFORMACION DE LA BLOCKCHAIN########################################
# Información del estado de la cadena: altura, dificultad, headers, validación.  Como es muy extenso, la info que se le proporciona 
# a tools esta en utilidades.descripcionGetInfo()
def infoBlockchain():
    try:                        return AuthServiceProxy(getMainnetClient()).getblockchaininfo()
    except Exception as e:      return f"Error de conexión: {str(e)}"
########################################INFORMACION DE LA BLOCKCHAIN########################################
###########################################INFORMACION DE LA RED############################################
# Versión del nodo, conexiones, protocolos.
def infoRed():
    try:                        return AuthServiceProxy(getMainnetClient()).getnetworkinfo()
    except Exception as e:      return f"Error de conexión: {str(e)}"
###########################################INFORMACION DE LA RED############################################
###########################################INFORMACION DE BLOQUE############################################
# Obtiene el hash de un bloque dado su número.                                                              #REQUIERE PARAMETRO
def getblockhash(height: int = None):
    """
    Obtiene el hash de un bloque dado su altura.
    - height: Altura del bloque (obligatorio)
    """
    if height is None:
        return "Error: debes proporcionar la altura del bloque (height)."
    
    try:
        client = AuthServiceProxy(getMainnetClient())
        return client.getblockhash(height)
    except Exception as e:
        return f"Error de conexión o bloque no encontrado: {str(e)}"
###########################################INFORMACION DE BLOQUE############################################
#########################################INFORMACION DE LA MEMPOOL##########################################
# Info general de la mempool
def mempoolinfo():
    try:                        return AuthServiceProxy(getMainnetClient()).getmempoolinfo()
    except Exception as e:      return "Error de conexión"
#########################################INFORMACION DE LA MEMPOOL##########################################
#####################################ESTADISTICAS DE LAS TRANSACCIONES######################################
# Estadísticas de transacciones por conjuntos de bloques
def getchaintxstats(nblocks: int = None, blockhash: str = None):
    """
    Estadísticas de transacciones por bloques.
    - nblocks: Número de bloques a analizar (opcional)
    - blockhash: Hash del bloque a partir del cual contar (opcional)
    Si no se proporciona ninguno, devuelve estadísticas generales.
    """
    try:
        client = AuthServiceProxy(getMainnetClient())
        # Si se proporcionan parámetros
        if nblocks is not None and blockhash is not None:
            return client.getchaintxstats(nblocks, blockhash)
        elif nblocks is not None:
            return client.getchaintxstats(nblocks)
        elif blockhash is not None:
            # La API no acepta solo blockhash, debemos poner nblocks = 1 por defecto
            return client.getchaintxstats(1, blockhash)
        else:
            # Si no hay parámetros, devuelve estadísticas generales
            return client.getchaintxstats()
    except Exception as e:
        return f"Error de conexión o parámetros incorrectos: {str(e)}"
#####################################ESTADISTICAS DE LAS TRANSACCIONES######################################
##########################################INFORMACION DE LAS FEES###########################################
# Estimacion de cual seria la fee por kb a pagar para mandar una transaccion a la blockchain
def estimatesmartfee():
    try:                        return AuthServiceProxy(getMainnetClient()).estimatesmartfee(5, "economical")
    except Exception as e:      return f"Error de conexión: {str(e)}"
##########################################INFORMACION DE LAS FEES###########################################
#########################################INFORMACION DE UN BLOQUE###########################################
# Info general de la mempool
def bloqueInfo(blockhash: str):
    try:                        return AuthServiceProxy(getMainnetClient()).getblock(blockhash,1)
    except Exception as e:      return f"Error de conexión: {str(e)}"
#########################################INFORMACION DE UN BLOQUE###########################################
##########################################INFORMACION DE UNA TX#############################################
#########AUXILIAR PARA AYUDAR A TX, REUTLIZANDO CODIGO DE: https://github.com/Vitapostigo/BotBTCTelegram/blob/main/Utiles/funciones.py#########
def precioPorBTC(num):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()

    valorEnDols = (data['bitcoin']['usd']) * num
    precio = "{:.2f}".format(valorEnDols)

    return precio

####################################################################################################################
def textoMultisig(dirsConvencionales,dirsMultisig):
    textoRetorno = ""
    if len(dirsConvencionales) != 0:
        textoRetorno = "Direcciones no multisig:\n"
        for i in range(0, len(dirsConvencionales), 2):
            textoRetorno += dirsConvencionales[i] + " ha recibido: " + str(dirsConvencionales[i+1]) + "\n"

    #Direcciones multisig:
    textoRetorno = "Direcciones multisig:\n"
    for i in range(0, len(dirsMultisig), 2):
        multiSigActual = dirsMultisig[i].split()
        textoRetorno += f"La una multisig {multiSigActual[0]}/{multiSigActual[len(multiSigActual)-2]} ha recibido: {str(dirsMultisig[i+1])}\n"
        textoRetorno += "Y está compuesta por las siguientes claves públicas:\n"
        for j in range(1, len(multiSigActual)-2, 1):
            textoRetorno += multiSigActual[j] + "\n"

    return textoRetorno
####################################################################################################################
def check_multisig(transaction):
    for output in transaction['vout']:
        script_asm = output['scriptPubKey']['asm']
        if 'OP_CHECKMULTISIG' in script_asm:
            return True
    return False
####################################################################################################################
def printInputsFromList(list):
    retorno = ""
    for address in list:
        retorno += f"{address}\n"
    return retorno
####################################################################################################################
def outputFormat(list):
    retorno = ""
    for salida in list:
        #Caso OP_RETURN
        if salida[0] == 'OP_RETURN':
            if len(salida[0].split()) == 1:
                datosHex = salida[1]
            else:
                datosHex = salida[1].split()[1]
            retorno += f"Dirección: OP_RETURN, datos escritos en hex: {datosHex}\n"
            try:
                asciival = bytearray.fromhex(datosHex).decode()
                retorno += f"Valor en ASCII: {asciival}\n"
            except UnicodeDecodeError:
                retorno += "El cual no tiene representación ASCII\n"
        else:
            #Caso dirección standard
            retorno += f"Dirección: {salida[0]} recibió: {salida[1]} BTC\n"
        
    return retorno
##########################################################
def infoExtra (tx,jsonTx):
    try:
        #Revisar, a veces va a varias direcciones y hay que calcular la ultima...
        if "coinbase" in jsonTx["vin"][0]:
            id = jsonTx["txid"]
            recompensa = float(jsonTx["vout"][0]["value"])
            direccion_minero = jsonTx["vout"][0]["scriptPubKey"].get("address", "Desconocida")
            bloque_id = jsonTx.get("blockhash", "Desconocido")
            return (
                f"La transacción con id: {id} es una transacción de tipo coinbase.\n"
                f"Corresponde a la minería de un bloque con una recompensa de {recompensa:.8f} BTC que en este momento tienen un valor de: {precioPorBTC(recompensa)}\n"
                f"El beneficiario (minero) es: {direccion_minero}\n"
                f"ID del bloque minado: {bloque_id}"
            )
        # Obtener los inputs
        dirsEntrada = []
        for vin in jsonTx["vin"]:
            prev_tx = AuthServiceProxy(getMainnetClient()).getrawtransaction(vin["txid"], True)
            vout = prev_tx["vout"][vin["vout"]]
            dirsEntrada.append(vout["scriptPubKey"]["address"])

        if not check_multisig(jsonTx):  # En caso de que sea una transacción sin salida multisig procesamos aquí
            dirsSalidaSaldo = []
            for vout in jsonTx['vout']:
                ###Si tenemos un OP_RETURN los campos cambian, tratamos de forma diferente.
                if 'OP_RETURN' in vout['scriptPubKey']['asm']:
                    # Si es OP_RETURN, extraemos los datos
                    data = vout['scriptPubKey']['asm'].split(' ', 1)[1] if len(vout['scriptPubKey']['asm'].split(' ', 1)) > 1 else "No data"
                    dirsSalidaSaldo.append(("OP_RETURN", data))
                else:
                    # Si no es OP_RETURN, procesamos como antes
                    dirsSalidaSaldo.append((vout['scriptPubKey'].get('address', 'Desconocida'), float(vout['value'])))
    
            suma_total = sum(valor for _, valor in dirsSalidaSaldo if isinstance(valor, float))
            return f"En la transacción con id: {tx}\nha habido un movimiento de fondos por valor de: {suma_total} BTC, valorado en: {precioPorBTC(suma_total)} actualmente.\nHa sido enviada por las siguientes direccion/es:\n{printInputsFromList(dirsEntrada)}y la/s salida/s son:\n{outputFormat(dirsSalidaSaldo)}"

        else:#Tratar el procesamiento de la multisig
            dirsConvencionales = []
            dirsMultisig = []
            suma_total = 0
            #Direcciones normales
            for output in jsonTx.get('vout', []):
                address = output.get('scriptPubKey', {}).get('address')
                if address:
                    dirsConvencionales.append(address)
                    dirsConvencionales.append(output.get('value'))        #<addr1> <value1> <addr2> <value2> ... <addrn> <valuen>
                    suma_total += output.get('value')

            #Multisig
            for output in jsonTx['vout']:
                script_asm = output['scriptPubKey']['asm']
                if 'OP_CHECKMULTISIG' in script_asm:
                    dirsMultisig.append(script_asm)
                    dirsMultisig.append(output.get('value'))
                    suma_total += output.get('value')

            return f"En la transacción con id: {tx}\nse han movido fondos por valor de: {suma_total} BTC, valorado en: {precioPorBTC(suma_total)} actualmente.\nHa sido enviada por las siguientes direccion/es:\n{printInputsFromList(dirsEntrada)}Y la/s salida/s se estructuran de la siguiente manera:\n" + textoMultisig(dirsConvencionales,dirsMultisig)      
    except Exception as excp:
        return "Error en la información extra, interpretar solo la información del json"
    
#########AUXILIAR PARA AYUDAR A TX, REUTLIZANDO CODIGO DE: https://github.com/Vitapostigo/BotBTCTelegram/blob/main/Utiles/funciones.py#########
def infoTransaccion(txid: str): 
    """Devuelve la transacción completa dado su txid."""
    try:
        respuesta = AuthServiceProxy(getMainnetClient()).getrawtransaction(txid, True)
        extra = infoExtra(txid,respuesta)
        return f"Respuesta nodo: {str(respuesta)} Información extra: {extra}"
        
    except Exception as e:
        return {"error": str(e)}
##########################################INFORMACION DE UNA TX#############################################