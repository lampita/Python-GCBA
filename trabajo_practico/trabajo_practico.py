try:
    import rich

except ImportError:
    print(
        "El módulo 'rich' no está instalado. Por favor, instálalo con: 'pip install rich'"
    )
    exit()

from rich.console import Console
from rich.table import Table
from rich import print
import os
from datetime import datetime, timedelta
from base_datos import inventario_supermercado as invt

console = Console()
umbral_stock_critico = 50
umbral_vencimiento_critico = 5

hoy = datetime.now().date()
dias_umbral = timedelta(days=umbral_vencimiento_critico)
fecha_limite = hoy + dias_umbral

vencimiento_critico = {
    k: v
    for (k, v) in invt.items()
    if v["fecha_de_vencimiento"] != "N/A"
    and v["cantidad_unidades_en_stock"] > 0
    and hoy
    <= datetime.strptime(v["fecha_de_vencimiento"], "%Y-%m-%d").date()
    <= fecha_limite
}
vencidos = {
    k: v
    for (k, v) in invt.items()
    if v["fecha_de_vencimiento"] != "N/A"
    and v["cantidad_unidades_en_stock"] > 0
    and hoy > datetime.strptime(v["fecha_de_vencimiento"], "%Y-%m-%d").date()
}

stock_critico = {
    k: v
    for (k, v) in invt.items()
    if v["cantidad_unidades_en_stock"] < umbral_stock_critico
    and v["cantidad_unidades_en_stock"] > 0
}
sin_stock = {k: v for (k, v) in invt.items() if v["cantidad_unidades_en_stock"] == 0}

total_de_marcas = len(invt)

total_de_unidades = sum(v["cantidad_unidades_en_stock"] for v in invt.values())

total_de_vencidos = len(vencidos)

total_vencimiento_critico = len(vencimiento_critico)

total_sin_stock = len(sin_stock)

total_stock_critico = len(stock_critico)






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
        f"\t{'=' * 31}\n\t[bold red]CONTROL DE STOCK Y VENCIMIENTOS[/bold red]\n\t{'=' * 31}"
    )

    print(f"Total de Marcas: [bold red]{total_de_marcas}[/bold red]")
    print(f"Total de Unidades: [bold red]{total_de_unidades}[/bold red]")
    print(
        f"Validas[bold green]{conv_to_super(total_de_unidades - (total_de_vencidos + total_vencimiento_critico))}[/bold green] Criticas[bold yellow]{conv_to_super(total_vencimiento_critico)}[/bold yellow] Vencidas[bold red]{conv_to_super(total_de_vencidos)}[/bold red]"
    )
    print(
        f"En Stock[bold green]{conv_to_super(total_de_unidades)}[/bold green] Por Agotarse[bold yellow]{conv_to_super(total_stock_critico)}[/bold yellow] Agotados[bold red]{conv_to_super(total_sin_stock)}[/bold red]"
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
                print(i, "\t", nombre)
            input("\nENTER para volver al menu ")
            continue

        case "2":
            print("\nLista de Nombres Válidos:\n")
            for i, nombre in enumerate(nombres_validos, start=1):
                print(i, "\t", nombre)
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
            print(
                "Seleccione si(\033[1;91ms\033[1;0m), no(\033[1;91mn\033[1;0m) o termina(\033[1;91mt\033[1;0m)\n"
            )
            i = 0

            while i < len(nombres_invalidos):
                nombre = nombres_invalidos[i]
                print(
                    f"\r{i + 1}/{len(nombres_validos)}\t{nombre[0]}\t->\033[33m{nombre[1]}\033[0m",
                    end="",
                    flush=True,
                )
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
            print(
                "Seleccione si(\033[1;91ms\033[1;0m), no(\033[1;91mn\033[1;0m) o termina(\033[1;91mt\033[1;0m)\n"
            )
            i = 0

            while i < len(nombres_validos):
                nombre = nombres_validos[i]
                print(f"\r{i + 1}/{len(nombres_validos)}\t{nombre}", end="", flush=True)
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


# print("--- Productos próximos a vencer (dentro de los próximos 7 días) ---\n")

# # 2. Iterar sobre el diccionario principal
# for sku, datos_producto in invt.items():
#     # 3. Omitir productos sin fecha de vencimiento
#     if datos_producto['fecha_de_vencimiento'] == 'N/A':
#         continue

#     # 4. Convertir la cadena de texto de la fecha a un objeto de fecha
#     fecha_vencimiento = datetime.strptime(datos_producto['fecha_de_vencimiento'], '%Y-%m-%d').date()

#     # 5. Comprobar si el producto está en el rango de vencimiento
#     if hoy <= fecha_vencimiento <= fecha_limite:
#         print(f"Producto: {datos_producto['producto']}")
#         print(f"SKU: {sku}")
#         print(f"Vence el: {fecha_vencimiento}")
#         print(f"Descripción: {datos_producto['pequena_descripcion']}\n")
