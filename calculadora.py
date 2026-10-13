import math

OPERACIONES = {
    "1": "suma",
    "2": "resta",
    "3": "multiplicación",
    "4": "división",
    "5": "promedio",
    "6": "potencia",
    "7": "mayor y menor",
}

# Operaciones que usan dos números y el orden en que se aplican.
ORDEN = {
    "resta": "primero menos segundo",
    "división": "primero entre segundo",
    "potencia": "primero elevado al segundo",
}


# CLASE
class Calculadora:

    def __init__(self, operacion, numeros):
        self.operacion = operacion
        self.numeros = numeros

    def suma(self):
        return sum(self.numeros)

    def resta(self):
        return self.numeros[0] - self.numeros[1]

    def multiplicacion(self):
        return math.prod(self.numeros)

    def division(self):
        return self.numeros[0] / self.numeros[1]

    def promedio(self):
        return sum(self.numeros) / len(self.numeros)

    def potencia(self):
        return math.pow(self.numeros[0], self.numeros[1])

    def mayor_y_menor(self):
        return max(self.numeros), min(self.numeros)

    def resultado(self):
        if self.operacion == "suma":
            return self.suma()
        elif self.operacion == "resta":
            return self.resta()
        elif self.operacion == "multiplicación":
            return self.multiplicacion()
        elif self.operacion == "división":
            return self.division()
        elif self.operacion == "promedio":
            return self.promedio()
        elif self.operacion == "potencia":
            return self.potencia()
        else:
            return self.mayor_y_menor()

def leer_numero(mensaje):
    while True:
        try:
            return float(input(mensaje).replace(",", "."))
        except ValueError:
            print("Valor no válido. Escribe un número, por ejemplo 8 o 3.5.")


def leer_cantidad():
    while True:
        texto = input("Cantidad de números: ").strip()
        if texto.isdecimal() and int(texto) >= 1:
            return int(texto)
        print("Cantidad no válida. Escribe un entero mayor o igual a 1.")


def formato(numero):
    numero = round(float(numero), 10)
    if numero.is_integer():
        return int(numero)
    return numero


while True:
    print("\n===== CALCULADORA =====")
    for opcion, nombre in OPERACIONES.items():
        print(opcion + ".", nombre.capitalize())
    print("0. Salir")
    opcion = input("Elige una opción: ").strip()

    if opcion == "0":
        print("Programa terminado.")
        break
    if opcion not in OPERACIONES:
        print("Opción no válida. Elige un número del menú.")
        continue

    operacion = OPERACIONES[opcion]
    print("Operación:", operacion)

    if operacion in ORDEN:
        print("Orden:", ORDEN[operacion])
        cantidad = 2
    else:
        cantidad = leer_cantidad()

    numeros = []
    for i in range(cantidad):
        numeros.append(leer_numero(f"Número {i + 1}: "))

    # OBJETO
    objeto = Calculadora(operacion, numeros)
    try:
        respuesta = objeto.resultado()
        if operacion == "mayor y menor":
            print("Resultado: mayor =", formato(respuesta[0]), "y menor =", formato(respuesta[1]))
        else:
            print("Resultado:", formato(respuesta))
    except ZeroDivisionError:
        print("Error: no se puede dividir entre cero.")
    except (ValueError, OverflowError):
        # Cero elevado a un negativo o un resultado demasiado grande.
        print("Error: no se puede calcular con esos valores.")
