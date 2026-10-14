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

# Nombres alternativos sin acentos, útiles al usar la API.
SINONIMOS = {
    "multiplicacion": "multiplicación",
    "division": "división",
    "mayor_y_menor": "mayor y menor",
}


# CLASE
class Calculadora:

    def __init__(self, operacion, numeros):
        self.operacion = SINONIMOS.get(operacion, operacion)
        self.numeros = numeros

    def suma(self):
        return sum(self.numeros)

    def resta(self):
        return self.numeros[0] - self.numeros[1]

    def multiplicacion(self):
        return math.prod(self.numeros)

    def division(self):
        if self.numeros[1] == 0:
            raise ZeroDivisionError("No se puede dividir entre cero.")
        return self.numeros[0] / self.numeros[1]

    def promedio(self):
        return sum(self.numeros) / len(self.numeros)

    def potencia(self):
        try:
            return math.pow(self.numeros[0], self.numeros[1])
        except (ValueError, OverflowError):
            # Cero elevado a un negativo, raíz de un negativo o un resultado demasiado grande.
            raise ValueError("No se puede calcular la potencia con esos valores.") from None

    def mayor_y_menor(self):
        return max(self.numeros), min(self.numeros)

    def validar(self):
        if self.operacion not in ORDEN and self.operacion not in OPERACIONES.values():
            raise ValueError(f"Operación no válida: {self.operacion}.")
        if not isinstance(self.numeros, (list, tuple)) or not self.numeros:
            raise ValueError("Debes indicar al menos un número.")
        for numero in self.numeros:
            if isinstance(numero, bool) or not isinstance(numero, (int, float)):
                raise ValueError(f"Valor no válido: {numero!r}. Solo se aceptan números.")
            if not math.isfinite(numero):
                raise ValueError("Los números deben ser finitos.")
        if self.operacion in ORDEN and len(self.numeros) != 2:
            raise ValueError(f"La operación {self.operacion} necesita exactamente dos números.")

    def resultado(self):
        self.validar()
        metodos = {
            "suma": self.suma,
            "resta": self.resta,
            "multiplicación": self.multiplicacion,
            "división": self.division,
            "promedio": self.promedio,
            "potencia": self.potencia,
            "mayor y menor": self.mayor_y_menor,
        }
        respuesta = metodos[self.operacion]()
        if not isinstance(respuesta, tuple) and not math.isfinite(respuesta):
            raise ValueError("El resultado es demasiado grande para calcularlo.")
        return respuesta


def leer_numero(mensaje):
    while True:
        try:
            numero = float(input(mensaje).replace(",", "."))
        except ValueError:
            print("Valor no válido. Escribe un número, por ejemplo 8 o 3.5.")
            continue
        if math.isfinite(numero):
            return numero
        print("Valor no válido. Escribe un número finito.")


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


def realizar_operacion(operacion):
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
    except (ZeroDivisionError, ValueError) as error:
        print("Error:", error)
        return
    if operacion == "mayor y menor":
        print("Resultado: mayor =", formato(respuesta[0]), "y menor =", formato(respuesta[1]))
    else:
        print("Resultado:", formato(respuesta))


def main():
    while True:
        mostrar_menu()
        try:
            opcion = input("Elige una opción: ").strip()
            if opcion == "0":
                print("Programa terminado.")
                break
            if opcion not in OPERACIONES:
                print("Opción no válida. Elige un número del menú.")
                continue
            realizar_operacion(OPERACIONES[opcion])
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma terminado.")
            break


if __name__ == "__main__":
    main()
