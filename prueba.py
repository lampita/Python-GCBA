import sys

# Escribir el mensaje sin un salto de línea al final
sys.stdout.write("Ingresa tu nombre: ")

# Asegurar que el mensaje se muestre inmediatamente
sys.stdout.flush()

# Capturar la entrada del usuario
nombre = sys.stdin.readline().strip()

print(f"\rHola, {nombre}!")