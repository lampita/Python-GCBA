"""Guarde cada nombre válido en una lista, asegurándote de agregarlo con el método .append().

Permití que se finalice la carga de nombres escribiendo la palabra "fin".

Una vez finalizada la carga, ordená alfabéticamente los nombres en la lista y mostrá la lista ordenada utilizando un bucle for."""

import os, datetime

lista_de_nombres: []

salir = False
while not salir:
    
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print(f"\t{'=' * 35}\n\t\033[1;91mINGRESO DE NOMBRES\033[0m\n\t{'=' * 35}")

    print("""MENU DE OPCIONES:
    1. Ingresar Nombre y Apellido
    2. Mostrar Lista Completa
    3. Ordenar por Apellido
    4. Ordenar por Nombre
    5. Salir
    """)
    print(datetime.date.today())
    opcion_menu = input("Ingresar opcion:")
    match opcion_menu:
        case "1":
            continue

        case "2":
            continue

        case "3":
            continue
        case "4":
            continue
        case "5":
            salir = True
