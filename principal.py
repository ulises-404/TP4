import clase
import pickle
import os


#r1.1
def busqueda_binaria(v, x):
    n = len(v)
    izq = 0
    der = n - 1
    while izq <= der:
        i = (izq + der) // 2
        if v[i].codigo == x.codigo:
            pos = i
            break
        else:
            if v[i].codigo < x.codigo:
                der = i - 1
            else:
                izq = i + 1
    if izq > der:
        pos = izq
    v[pos:pos] = [x]

def cargar_envios():
    v = []
    archivo = open("envios.csv", "r")
    for linea in archivo:
        if linea.strip() != "":
            envio = clase.generar_envio(linea)
            busqueda_binaria(v, envio)
    archivo.close()

    i = int(input("Ingrese índice: "))
    if 0 <= i < len(v):
        print("r1.1:", v[i].obtener_identificador_pago())
    else:
        print("r1.1: Índice fuera de rango")

    return v

#r2.1
def gen_binario_matriz(v):
    if not v:
        print("Debe cargar primero los envíos (opción 1).")
        return

    monedas = ["ARS", "USD", "EUR", "GBP", "JPY"]
    n = len(monedas)

    matriz = [[0, 0] for _ in range(n)]

    for envio in v:
        _, comision = monto_base(envio.monto_nominal, envio.algoritmo_comision)
        i = envio.obtener_codigo_moneda_origen() - 1
        matriz[i][0] += comision
        matriz[i][1] += 1

    promedios = [0] * n
    for i in range(n):
        if matriz[i][1] != 0:
            promedios[i] = matriz[i][0] / matriz[i][1]

    nombre = "envios_filtrados.dat"
    archivo = open(nombre, "wb")
    for envio in v:
        _, comision = monto_base(envio.monto_nominal, envio.algoritmo_comision)
        i = envio.obtener_codigo_moneda_origen() - 1
        if comision > promedios[i]:
            pickle.dump(envio, archivo)
    archivo.close()

    archivo = open(nombre, "rb")
    tamanio = os.path.getsize(nombre)
    while archivo.tell() < tamanio:
        envio = pickle.load(archivo)
        print(envio)
    archivo.close()

#--------------DEL TP3---------------------------
def mayor_monto_por_moneda(envios):
    monedas = ["ARS", "USD", "EUR", "GBP", "JPY"]
    n = len(monedas)
    matriz = []
    for i in range(n):
        fila = [0] * n
        matriz.append(fila)

    for envio in envios:
        monto_b, _ = monto_base(envio.monto_nominal, envio.algoritmo_comision)
        monto_f = monto_final(monto_b, envio.algoritmo_impositivo)
        i = envio.obtener_codigo_moneda_origen() - 1
        j = envio.obtener_codigo_moneda_destino() - 1
        if monto_f > matriz[i][j]:
            matriz[i][j] = monto_f
    return matriz, monedas


def mostrar_matriz(matriz, monedas):
    n = len(monedas)
    for i in range(n):
        for j in range(n):
            print(f"Origen {monedas[i]} Destino {monedas[j]}: {round(matriz[i][j], 2)}")

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


def mostrar(v):
    suma_porc = 0
    max_porc = 0
    id_pago_max = ""
    monto_final_max = 0

    for envio in v:
        monto_b, comision = monto_base(envio.monto_nominal, envio.algoritmo_comision)
        porc_comision = (comision / envio.monto_nominal) * 100
        suma_porc += porc_comision

        monto_f = monto_final(monto_b, envio.algoritmo_impositivo)
        desc_total = envio.monto_nominal - monto_f
        porc_desc = (desc_total / envio.monto_nominal) * 100

        if porc_desc > max_porc:
            max_porc = porc_desc
            monto_final_max = round(monto_f, 2)
            id_pago_max = str(envio.obtener_identificador_pago())

    promedio_comisiones = suma_porc / len(v)

    matriz, monedas = mayor_monto_por_moneda(v)

    mostrar_matriz(matriz, monedas)



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
    while op != 0:
        print("1. Cargar envíos")
        print("2. Generar archivo binario")
        print("0. Salir")
        op = int(input("Ingrese opción: "))
        if op == 1:
            v = cargar_envios()
        elif op == 2:
            gen_binario_matriz(v)
        elif op == 0:
            print("Programa finalizado.")

if __name__ == '__main__':
    principal()