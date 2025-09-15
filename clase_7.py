"""
Una vez finalizada la carga, ordená alfabéticamente los nombres en la lista y mostrá la lista ordenada utilizando un bucle for."""

import os, datetime
import colorama

lista_de_nombres = []


def nombre_es_valido(nombre):
    if not nombre.strip():
        return "\n❌ Error. ->Campo Vacío", False

    if any(char.isdigit() for char in nombre):
        return "\n❌ Error. ->Contiene Números", False

    if any(not char.isalpha() and not char.isspace() for char in nombre):
        return "\n❌ Error. ->Contiene caracteres especiales o inválidos", False

    return " ✔️\n", True


salir = False
while not salir:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print(f"\t{'=' * 19}\n\t\033[1;91mINGRESO DE NOMBRES\033[0m\n\t{'=' * 19}")
    print(
        colorama.Fore.CYAN
        + colorama.Style.BRIGHT
        + f"FECHA: {datetime.datetime.now().strftime('%d/%m/%Y')}"
        + colorama.Style.RESET_ALL
    )

    print("""MENU DE OPCIONES:
    1. Ingresar Nombre y Apellido
    2. Mostrar Lista Completa
    3. Ordenar por Apellido
    4. Ordenar por Nombre
    5. Salir
    """)

    opcion_menu = input("OPCION:  ")
    match opcion_menu:
        case "1":
            print("\nINGRESANDO DATOS (Sale con \033[1;91m'fin'\033[0m.)")
            while True:
                nombre = input("INGRESE NOMBRE: ").strip()
                if nombre.lower() == "fin":
                    break

                if not (nombre_es_valido(nombre)[1]):
                    print(f"{(nombre_es_valido(nombre)[0])}. ->Intente Nuevamente.")
                    continue
                else:
                    print(nombre, nombre_es_valido(nombre)[0])

                apellido = input("INGRESE APELLIDO: ").strip()
                if apellido.lower() == "fin":
                    break

                if not nombre_es_valido(apellido):
                    print(f"{(nombre_es_valido(apellido)[0])}. ->Intente Nuevamente.")
                    continue
                else:
                    print(apellido, nombre_es_valido(apellido)[0])
                nombre_completo = [nombre.title(), apellido.title()]

                fecha_actual = [datetime.datetime.now().strftime("%d/%m/%Y")]

                registro = fecha_actual + nombre_completo

                lista_de_nombres.append(registro)
                print(
                    f" '{nombre_completo[0]} {nombre_completo[1]}' ->Agregado a la Lista."
                )

        case "2":
            if not lista_de_nombres:
                print("La lista de nombres está vacía.")
            else:
                print("\nMOSTRANDO LISTA COMPLETA:\n")
                for i, nombre_completo in enumerate(lista_de_nombres, start=1):
                    print(f"{i}. {nombre_completo}")
            input("\nPresione ENTER para volver al menú...")

        case "3":
            lista_ordenada_por_apellido = sorted(lista_de_nombres, key=lambda x: x[2])
            for i, nombre_completo in enumerate(
                lista_ordenada_por_apellido, start=1
            ):
                print(f"{i}. {nombre_completo[2]}, {nombre_completo[1]}")
            input("\nPresione ENTER para volver al menú...")
        
        case "4":
            lista_ordenada_por_nombre = sorted(lista_de_nombres, key=lambda x: x[1])
            for i, nombre_completo in enumerate(
                lista_ordenada_por_nombre, start=1
            ):
                print(f"{i}. {nombre_completo[1]}, {nombre_completo[2]}")
            input("\nPresione ENTER para volver al menú...")
        case "5":
            print("Saliendo...\n\n")
            salir = True
