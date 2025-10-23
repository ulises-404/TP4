import clase
import pickle
import os


# R4.1-------------------------------------------------------------

def mayor_monto_por_moneda(envios):
    matriz_montos = [[0] * 5 for _ in range(5)]
    matriz_envios = [[0] * 5 for _ in range(5)]
    monto_mayor = 0
    for envio in envios:
        moneda_origen = envio.obtener_codigo_moneda_origen()
        moneda_destino = envio.obtener_codigo_moneda_destino()
        monto_b, _ = monto_base(envio.monto_nominal, envio.algoritmo_comision)
        monto_f = monto_final(monto_b, envio.algoritmo_impositivo)
        f = moneda_origen - 1
        c = moneda_destino - 1
        if monto_f > matriz_montos[f][c]:
            matriz_montos[f][c] = monto_f
            matriz_envios[f][c] = envio

    return matriz_envios


def mostrar_matriz(matriz_envios):
    monedas = ["","ARS","USD","EUR","GBP","JPY"]

    for f in range(5):
        for c in range(5):
            print("Origen ",monedas[f + 1],"Destino ",monedas[c + 1]," :",matriz_envios[f][c].codigo)



# R4.1-------------------------------------------------------------





#Busqueda binaria r3.1/r3.2
def busqueda_binaria(idd, v):
    n = len(v)
    izq, der = 0, n
    while izq <= der:
        c = (izq + der) // 2
        if v[c].identificacion_destinatario == idd:
            return c
        else:
            if idd > v[c].identificacion_destinatario:
                der = c - 1
            else:
                izq = c + 1

    return -1


def insercion_ordenada(v, x): #insercion ordenada
    n = len(v)
    pos = n
    izq, der = 0, n-1
    while izq <= der:
        c = (izq + der) // 2
        if v[c].identificacion_destinatario == x.identificacion_destinatario:
            pos = c
            break
        else:
            if x.identificacion_destinatario > v[c].identificacion_destinatario:
                der = c - 1
            else:
                izq = c + 1
    if izq > der:
        pos = izq
    v[pos:pos] = [x]


def cargar_envios():
    v = []
    archivo = open("envios.csv", "r")
    for linea in archivo:
        if linea.strip() != "":
            envio = clase.generar_envio(linea)
            insercion_ordenada(v, envio)
    archivo.close()

    i = int(input("Ingrese índice: "))

    if 0 <= i < len(v):
        print("r1.1:", v[i].obtener_identificador_pago())

    else:
        r1_indice = len(v) - 1
        print("r1.1:", v[r1_indice].obtener_identificador_pago())


    # R1.2-------------------------------------------------------------
    if (i % 2) != 0: # Si el indice es impar...

        indice_r2 = (i * 3) + 1
        if 0 <= indice_r2 < len(v):
            print("r1.2:", v[indice_r2].obtener_identificador_pago())

        else:

            # Fuera de rango - indice impar . . .
            indice_r2 = len(v) - 1
            print("r1.2:", v[indice_r2].obtener_identificador_pago())

    elif (i % 2) == 0: #Indice par...
        indice_r2 = i // 2
        if 0 <= indice_r2 < len(v):
            print("r1.2:", v[indice_r2].obtener_identificador_pago())

        else: # Fuera de rango - indice par . . .
            indice_r2 = len(v) - 1
            print("r1.2:", v[indice_r2].obtener_identificador_pago())
    # ----------------------------------------------------------------

    return v


# r2.1
def gen_binario_matriz(v, nombre):
    if not v:
        print("Debe cargar primero los envíos (opción 1).")
        return

    c = ac = 0

    for envio in v:
        _, comision = monto_base(envio.monto_nominal, envio.algoritmo_comision)
        c += 1
        ac += comision

    promedio = 0
    if c != 0:
        promedio = ac // c

    archivo = open(nombre, "wb")
    for envio in v:
        _, comision = monto_base(envio.monto_nominal, envio.algoritmo_comision)
        if comision > promedio:
            pickle.dump(envio, archivo)
    archivo.close()


def mostrar_archivo_bin(nombre):
    archivo = open(nombre, "rb")
    tamanio = os.path.getsize(nombre)
    while archivo.tell() < tamanio:
        envio = pickle.load(archivo)
        print(envio)
    archivo.close()


# ------------------------R3.1/3.2-----------------------------------
def buscar_envio(v):
    idd = input("Ingresa una identificacion de destinatario a buscar: ")
    r = busqueda_binaria(idd, v)

    if r != -1:
        print("r3.1: ", v[r].monto_nominal)
        incremento = v[r].monto_nominal * 1.17
        v[r].monto_nominal = round(incremento, -2)
        print("r3.2: ", v[r].monto_nominal)

    else:
        print("r3.1: ", 0)
        print("r3.2: ", 0)


# --------------DEL TP3---------------------------


def monto_final(monto_base, alg_imp):
    monto_final = 0
    impuesto = 0

    if alg_imp == 1:
        if monto_base <= 300000:
            impuesto = 0
        elif monto_base > 300000:
            excedente = monto_base - 300000
            impuesto = (25 / 100) * excedente

        monto_final = monto_base - impuesto

    elif alg_imp == 2:
        if monto_base < 50000:
            impuesto = 50
        elif monto_base >= 50000:
            impuesto = 100

        monto_final = monto_base - impuesto

    elif alg_imp == 3:
        impuesto = (3 / 100) * monto_base
        monto_final = monto_base - impuesto

    return monto_final


def monto_base(monto_nominal, alg_comision):
    monto_base = 0
    comision = 0
    if alg_comision == 1:
        comision = (9 / 100) * monto_nominal
        monto_base = monto_nominal - comision
    elif alg_comision == 2:
        if monto_nominal < 50000:
                comision = 0
        elif 50000 <= monto_nominal < 80000:
                comision = (5 / 100) * monto_nominal
        elif monto_nominal >= 80000:
                comision = (7.8 / 100) * monto_nominal
        monto_base = monto_nominal - comision
    elif alg_comision == 3:
        monto_fijo = 100
        if monto_nominal > 25000:
            comision = (6 / 100) * monto_nominal
            comision += monto_fijo
        else:
            comision = monto_fijo

        monto_base = monto_nominal - comision
    elif alg_comision == 4:
        if monto_nominal <= 100000:
            comision = 500
        elif monto_nominal > 100000:
            comision = 1000

        monto_base = monto_nominal - comision
    elif alg_comision == 5:
        if monto_nominal < 500000:
            comision = 0
        elif monto_nominal >= 500000:
            comision = (7 / 100) * monto_nominal

        if comision > 50000:
            comision = 50000

        monto_base = monto_nominal - comision
    return monto_base, comision


def pasaje_desde_csv(linea):

    partes1 = linea[0].split("|")
    mod_origen = int(partes1[0])
    mod_pago = int(partes1[1])
    id_pago = partes1[2]

    identificacion = linea[1].strip()
    nombre = linea[2].strip()
    tasa = float(linea[3])
    monto = int(linea[4])
    alg_comision = int(linea[5])
    alg_impositivo = int(linea[6])

    envio = clase.Envio(mod_origen, mod_pago, id_pago, identificacion, nombre, tasa, monto, alg_comision, alg_impositivo)

    return envio


def principal():
    v = []
    op = -1
    nombre = "envios_filtrados.dat"
    while op != 0:
        print("1. Cargar envíos")
        print("2. Mostrar listado")
        print("3. Buscar")
        print("4. Mayores")
        print("0. Salir")
        op = int(input("Ingrese opción: "))

        if op == 1:
            v = cargar_envios()
        elif op == 2:
            gen_binario_matriz(v, nombre)
            mostrar_archivo_bin(nombre)
        elif op == 3:
            buscar_envio(v)
        elif op == 4:
            matriz_envios = mayor_monto_por_moneda(v)
            mostrar_matriz(matriz_envios)

        elif op == 0:
            print("Programa finalizado.")


if __name__ == '__main__':
    principal()
