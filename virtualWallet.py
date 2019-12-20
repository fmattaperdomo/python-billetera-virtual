import requests
import sys
from datetime import datetime

#inicialización
_ENDPOINT = "https://api.binance.com"
usuarioLogin="1"
monedas = ()
#inicialización del inventario de la moneda
inventarios = {
    "1":{'BTC':{"cantidad":100,"precio":10},'BCC':{"cantidad":100,"precio":1},'LTC':{"cantidad":100,"precio":1},'ETH':{"cantidad":100,"precio":1},'ETC':{"cantidad":100,"precio":1},'XRP':{"cantidad":100,"precio":1}},
    "2":{'BTC':{"cantidad":200,"precio":20},'BCC':{"cantidad":100,"precio":1},'LTC':{"cantidad":100,"precio":1},'ETH':{"cantidad":100,"precio":1},'ETC':{"cantidad":100,"precio":1},'XRP':{"cantidad":100,"precio":1}},
    "3":{'BTC':{"cantidad":300,"precio":30},'BCC':{"cantidad":100,"precio":1},'LTC':{"cantidad":100,"precio":1},'ETH':{"cantidad":100,"precio":1},'ETC':{"cantidad":100,"precio":1},'XRP':{"cantidad":100,"precio":1}},
    "4":{'BTC':{"cantidad":400,"precio":40},'BCC':{"cantidad":100,"precio":1},'LTC':{"cantidad":100,"precio":1},'ETH':{"cantidad":100,"precio":1},'ETC':{"cantidad":100,"precio":1},'XRP':{"cantidad":100,"precio":1}},
    "5":{'BTC':{"cantidad":500,"precio":50},'BCC':{"cantidad":100,"precio":1},'LTC':{"cantidad":100,"precio":1},'ETH':{"cantidad":100,"precio":1},'ETC':{"cantidad":100,"precio":1},'XRP':{"cantidad":100,"precio":1}}
}

def esmoneda(cripto):
    return cripto in monedas

def esnumero(valor):
    return valor.replace('.','',1).isdigit()

def esusuario(usuario):
    return inventarios.get(usuario)

def _url(api):
    return _ENDPOINT+api

def get_price(cripto):
    return requests.get(_url("/api/v3/ticker/price?symbol="+cripto))

def llenadoMonedas():
    data=[]
    monedas_list=[]
    data=requests.get("https://api.coinmarketcap.com/v2/listings/").json()

    for cripto in data["data"]:
        monedas_list.append(cripto["symbol"])

    global monedas
    monedas=tuple(monedas_list)

def actualizarInventario(usuarioDestino,moneda,cantidad,precio,usuarioOrigen):
    inventarios.get(usuarioDestino)[moneda]['cantidad'] = inventarios.get(usuarioDestino)[moneda]['cantidad'] + cantidad
    inventarios.get(usuarioDestino)[moneda]['precio'] = precio
    inventarios.get(usuarioOrigen)[moneda]['cantidad'] = inventarios.get(usuarioOrigen)[moneda]['cantidad'] - cantidad
    inventarios.get(usuarioDestino)[moneda]['precio'] = precio
    
def continuarPrograma():
    continuar=""
    while continuar != "s":
        continuar = str(input("Desea continuar? (s/n):  ")).lower()
        if continuar == 'n':
            sys.exit()
    menu()

def registrarHistorico(moneda,transaccion,usuario,cantidad,precio):
    archivo=open('historicos.txt','a')
    ahora = datetime.now()
    valor = float(cantidad)*float(precio)
    fecha = str(ahora.strftime("%d de %B de %Y"))
    archivo.write(fecha+"|"+moneda+"|"+transaccion+"|"+ usuario + "|" + str(cantidad) + "|" + str(valor) + "\n")
    archivo.close()

def recibirMoneda():
    print('***********************************************')
    print('*****  R E C I B I R   M O N E D A        *****')
    print('***********************************************')
    moneda=""
    while not esmoneda(moneda):
        moneda = str(input("Ingrese la moneda a recibir ['BTC','BCC','LTC','ETH','ETC','XRP'] :  "))
    valor=""
    while not esnumero(valor):    
        valor = str(input("Ingrese la cantidad de la moneda " + moneda + " a recibir :  "))
    cantidad = float(valor)
    usuario="" 
    while not esusuario(usuario):    
        usuario = str(input("Ingrese el código de usuario: "))
        if usuario == usuarioLogin:
            print("No se puede recibir a si mismo :  " + usuarioLogin)
            usuario=""
    data = get_price(moneda+"USDT").json()
    precio = data["price"]
    actualizarInventario(usuarioLogin,moneda,cantidad,precio,usuario)
    registrarHistorico(moneda,"Recibir Moneda",usuario,cantidad,precio)
    continuarPrograma()

def mostrarHistorico():    
    print('******************************************************************************************************')
    print('*****                        M O S T R A R   H I S T O R I C O S                                 *****')
    print('******************************************************************************************************')
    archivo=open('historicos.txt','r')
    texto = archivo.read()
    archivo.close()
    lineas = texto.splitlines()
    terminos = texto.split("|")
    print("FECHA\t\t\t" + "MONEDA\t" + "TRANSACCION\t\t" + "USUARIO\t\t" + "CANTIDAD\tMONTO")
    for linea in lineas:
        termino = linea.split("|")
        print(termino[0] + "\t" + termino[1] + "\t" + termino[2]+ "\t\t" + termino[3] + "\t\t" + termino[4]+ "\t\t" + termino[4])
    continuarPrograma()
    
def transferirMoneda():
    print('***********************************************')
    print('*****  T R A N S F E R I R  M O N E D A  *****')
    print('***********************************************')
    moneda=""
    while not esmoneda(moneda):
        moneda = str(input("Ingrese la moneda a recibir ['BTC','BCC','LTC','ETH','ETC','XRP'] :  "))
    valor=""
    while not esnumero(valor):    
        valor = str(input("Ingrese la cantidad de la moneda " + moneda + " a recibir :  "))
    cantidad = float(valor)
    usuario="" 
    while not esusuario(usuario):    
        usuario = str(input("Ingrese el código del usuario a transferir: "))
        if usuario == usuarioLogin:
            print("No se puede transferir a si mismo :  " + usuarioLogin)
            usuario=""
    data = get_price(moneda+"USDT").json()
    precio = data["price"]
    actualizarInventario(usuario,moneda,cantidad,precio,usuarioLogin)
    registrarHistorico(moneda,"Transferir Moneda",usuario,cantidad,precio)
    continuarPrograma()

def balancePorMoneda():
    print('*********************************************************************')
    print('*****        B A L A N C E     P O R      M O N E D A           *****')
    print('*********************************************************************')
    moneda=""
    monto=0.0
    cantidad=0.0
    while not esmoneda(moneda):
        moneda = str(input("Ingrese la moneda a recibir ['BTC','BCC','LTC','ETH','ETC','XRP'] :  "))
    print("Moneda\t\t\tCantidad\t\t\tMonto")  
    for elemento in inventarios:
        if moneda in inventarios.get(elemento).keys():
            cantidad += inventarios.get(elemento)[moneda]['cantidad']
            monto += float(inventarios.get(elemento)[moneda]['cantidad']) * float(inventarios.get(elemento)[moneda]['precio'])
    print(moneda + "\t\t\t" + str(cantidad) + "\t\t\t\t" + str(monto))    
    continuarPrograma()

def balanceGeneral():
    print('*********************************************************************')
    print('*****            B A L A N C E     G E N E R A L                *****')
    print('*********************************************************************')
    print("Moneda\t\t\tCantidad\t\t\tMonto")  
    diccionario={}
    for elemento in inventarios:
        monto=0.0
        cantidad=0.0

        for moneda in inventarios.get(elemento).keys(): 
            cantidad = inventarios.get(elemento)[moneda]['cantidad']
            monto = float(inventarios.get(elemento)[moneda]['cantidad']) * float(inventarios.get(elemento)[moneda]['precio'])
            if moneda in diccionario.keys():
                diccionario[moneda]["cantidad"]=diccionario[moneda]["cantidad"] + cantidad
                diccionario[moneda]["monto"]=diccionario[moneda]["monto"] + monto
            else:
                diccionario[moneda]={"cantidad":cantidad,"monto":monto}
    
    for elemento in diccionario :
        print(elemento + "\t\t\t" + str(diccionario.get(elemento)["cantidad"]) + "\t\t\t\t" + str(diccionario.get(elemento)["monto"]))
    continuarPrograma()



def menu():
    print('***********************************************')
    print('*****     V I R T U A L   W A L L E T     *****')
    print('***********************************************')
    print('*** <1> Recibir cantidad                    ***')
    print('*** <2> Transferir monto                    ***')
    print('*** <3> Mostrar balance x Moneda            ***')
    print('*** <4> Mostrar balance General             ***')
    print('*** <5> Mostrar Históricos de transacciones ***')
    print('*** <6> Salir                               ***')
    print('***********************************************')
    opcion=6
    while opcion > 0 or opcion < 7:
        try:
            opcion = int(input("Escoge una opción: "))
        except ValueError:
            print("Opción invalida.  Por favor seleccionar del 1 al 6.")
            opcion = 6
            continue
        if opcion == 1:
            recibirMoneda()
        elif opcion == 2:
            transferirMoneda()
        elif opcion == 3:
            balancePorMoneda()
        elif opcion == 4:
            balanceGeneral()
        elif opcion == 5:
            mostrarHistorico()
        else:
            sys.exit()

def run():
    #Poblar las monedas existentes
    llenadoMonedas()
    # llamado al menu
    menu()

if __name__ == '__main__':
    run()
