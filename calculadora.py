import math

# Nombres de las operaciones; se definen una vez para no repetir los textos.
SUMA = "suma"
RESTA = "resta"
MULTIPLICACION = "multiplicación"
DIVISION = "división"
PROMEDIO = "promedio"
POTENCIA = "potencia"
MAYOR_Y_MENOR = "mayor y menor"

OPERACIONES = {
    "1": SUMA,
    "2": RESTA,
    "3": MULTIPLICACION,
    "4": DIVISION,
    "5": PROMEDIO,
    "6": POTENCIA,
    "7": MAYOR_Y_MENOR,
}

# Operaciones que usan dos números y el orden en que se aplican.
ORDEN = {
    RESTA: "primero menos segundo",
    DIVISION: "primero entre segundo",
    POTENCIA: "primero elevado al segundo",
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
        if self.operacion == SUMA:
            return self.suma()
        elif self.operacion == RESTA:
            return self.resta()
        elif self.operacion == MULTIPLICACION:
            return self.multiplicacion()
        elif self.operacion == DIVISION:
            return self.division()
        elif self.operacion == PROMEDIO:
            return self.promedio()
        elif self.operacion == POTENCIA:
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


def mostrar_menu():
    print("\n===== CALCULADORA =====")
    for opcion, nombre in OPERACIONES.items():
        print(opcion + ".", nombre.capitalize())
    print("0. Salir")


def pedir_numeros(operacion):
    if operacion in ORDEN:
        print("Orden:", ORDEN[operacion])
        cantidad = 2
    else:
        cantidad = leer_cantidad()
    return [leer_numero(f"Número {i + 1}: ") for i in range(cantidad)]


def mostrar_resultado(operacion, numeros):
    try:
        respuesta = Calculadora(operacion, numeros).resultado()
    except ZeroDivisionError:
        print("Error: no se puede dividir entre cero.")
        return
    except (ValueError, OverflowError):
        # Cero elevado a un negativo o un resultado demasiado grande.
        print("Error: no se puede calcular con esos valores.")
        return

    if operacion == MAYOR_Y_MENOR:
        print("Resultado: mayor =", formato(respuesta[0]), "y menor =", formato(respuesta[1]))
    else:
        print("Resultado:", formato(respuesta))


def main():
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "0":
            print("Programa terminado.")
            break
        if opcion not in OPERACIONES:
            print("Opción no válida. Elige un número del menú.")
            continue

        operacion = OPERACIONES[opcion]
        print("Operación:", operacion)
        mostrar_resultado(operacion, pedir_numeros(operacion))


if __name__ == "__main__":
    main()
