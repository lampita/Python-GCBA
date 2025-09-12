import os


def filtrar_nombres(lista_nombres):
    nombres_validos = []
    nombres_invalidos = []

    for nombre in lista_nombres:
        if not nombre.strip():
            nombres_invalidos.append((nombre, "Está vacío o solo contiene espacios"))
            continue

        palabras = nombre.split()

        if len(palabras) < 2:
            nombres_invalidos.append((nombre, "No tiene al menos dos palabras"))
            continue

        if any(char.isdigit() for char in nombre):
            nombres_invalidos.append((nombre, "Contiene números"))
            continue

        if any(not char.isalpha() and not char.isspace() for char in nombre):
            nombres_invalidos.append((nombre, "Contiene caracteres especiales"))
            continue

        nombres_validos.append(" ".join(palabras))

    return nombres_validos, nombres_invalidos


nombres_a_filtrar = [
    "Juan   Pérez",
    "   ",
    "",
    "Ana    López",
    "Pedro 123",
    "Luis",
    "María García",
    "PedroPa lmieri",
    "Carlos",
    "María",
    "Elisa 45",
    "Diego de la Vega",
    "Raúl 55  Ortega",
    "   Andrés  García  ",
    "   2255  ",
    " pere$ andres",
    "Car los",
]

nombres_validos, nombres_invalidos = filtrar_nombres(nombres_a_filtrar)


def conv_to_super(n):
    super = list(map(chr, [8304, 185, 178, 179, 8308, 8309, 8310, 8311, 8312, 8313]))
    st = ""

    for i in str(n):
        st += super[int(i)]

    return st


salir = False
while not salir:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print(
        f"\t{'=' * 35}\n\t\033[1;91mVALIDACION  DE  LISTAS  DE NOMBRES\033[0m\n\t{'=' * 35}"
    )
    print("\nArchivo a Procesar: nombres_a_filtrar")
    print(f"Total de Clientes: \033[1;37m{len(nombres_a_filtrar)}\033[1;0m")
    print(
        f"Validos\033[1;32m{conv_to_super(len(nombres_validos))}\033[1;0m-Invalidos\033[1;91m{conv_to_super(len(nombres_invalidos))}\033[1;0m"
    )
    print("""\nMENU DE OPCIONES:
    1. Mostrar lista Completa
    2. Mostrar Lista de Válidos
    3. Mostrar Lista de Inválidos
    4. Procesar Manualemente Inválidos
    5. Procesar Manualmente Válidos
    6. Salir\n""")

    opcion_menu = input("Ingresar opcion:  ")
    print()
    match opcion_menu:
        case "1":
            print("\nLista Completa de Nombres:\n")
            for i, nombre in enumerate(nombres_a_filtrar, start=1):
                print(i,"\t", nombre)
            input("\nENTER para volver al menu ")
            continue

        case "2":
            print("\nLista de Nombres Válidos:\n")
            for i, nombre in enumerate(nombres_validos, start=1):
                print(i, "\t",nombre)
            input("\nENTER para volver al menu ")
            continue

        case "3":
            print("\nLista de Nombres Inválidos:\n")
            for (
                i,
                nombre,
            ) in enumerate(nombres_invalidos, start=1):
                print(f'{i:<6}"{nombre[0] + '"':<25}->\033[1;91m{nombre[1]}\033[1;0m')
            input("\nENTER para volver al menu ")
            continue
        case "4":
            print("Seleccione si(\033[1;91ms\033[1;0m), no(\033[1;91mn\033[1;0m) o termina(\033[1;91mt\033[1;0m)\n")
            i = 0

            while i < len(nombres_invalidos):
                nombre = nombres_invalidos[i]
                print(f"\r{i+1}/{len(nombres_validos)}\t{nombre[0]}\t->\033[33m{nombre[1]}\033[0m", end="", flush=True)
                tag = input("\t-> \033[3mES VALIDO?: \033[0m").lower()
                print("\x1b[1A\x1b[2K" + "" * 50, end="\r")

                if tag == "s":
                    nombres_validos.append(nombre[0])

                    nombres_invalidos.pop(i)

                elif tag == "t":
                    break
                else:
                    i += 1

            input("\nENTER para volver al menu ")
            continue
        case "5":
            print("Seleccione si(\033[1;91ms\033[1;0m), no(\033[1;91mn\033[1;0m) o termina(\033[1;91mt\033[1;0m)\n")
            i = 0

            while i < len(nombres_validos):
                nombre = nombres_validos[i]
                print(f"\r{i+1}/{len(nombres_validos)}\t{nombre}", end="", flush=True)
                tag = input("\t-> \033[3mES VALIDO?: \033[0m").lower()
                print("\x1b[1A\x1b[2K" + "" * 50, end="\r")

                if tag == "n":
                    nombres_invalidos.append((nombre, "Extraído de Válidos"))

                    nombres_validos.pop(i)

                elif tag == "t":
                    break
                else:
                    i += 1

            input("\nENTER para volver al menu ")
            continue
        case "6":
            print("Saliendo...\n")
            salir = True
