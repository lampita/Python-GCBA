try:
    import rich

except ImportError:
    print(
        "El módulo 'rich' no está instalado. Por favor, instálalo con: 'pip install rich'"
    )
    exit()

from rich.console import Console
from rich.table import Table
import os
from datetime import datetime, timedelta
from base_datos import inventario_supermercado as invt


def borrar_consola():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


console = Console(highlight=False)
hoy = datetime.now().date()
umbral_stock_critico = 50
umbral_vencimiento_critico = 5


def conv_to_super(n):
    super = list(map(chr, [8304, 185, 178, 179, 8308, 8309, 8310, 8311, 8312, 8313]))
    st = ""

    for i in str(n):
        st += super[int(i)]

    return st


def num_es_valido(num):
    global umbral_stock_critico
    global umbral_vencimiento_critico

    if not num.strip():
        print("❌ ->Dato Vacío -> No se modifico el valor.\n")
        return umbral_stock_critico, umbral_vencimiento_critico

    if any(not num.isdigit() for num in num):
        print("❌ ->Dato Invalido -> No se modifico el valor.\n")
        return umbral_stock_critico, umbral_vencimiento_critico

    else:
        return int(num), "✔️\n"


salir = False
while not salir:
    borrar_consola()

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
        if v["cantidad_unidades_en_stock"] <= umbral_stock_critico
        and v["cantidad_unidades_en_stock"] > 0
    }
    sin_stock = {
        k: v for (k, v) in invt.items() if v["cantidad_unidades_en_stock"] == 0
    }

    total_de_lotes = len(invt)

    total_de_unidades = sum(v["cantidad_unidades_en_stock"] for v in invt.values())

    total_de_vencidos = len(vencidos)

    total_vencimiento_critico = len(vencimiento_critico)

    total_sin_stock = len(sin_stock)

    total_stock_critico = len(stock_critico)

    console.print(
        f"\t{'=' * 31}\n\t[bold red]CONTROL DE STOCK Y VENCIMIENTOS[/bold red]\n\t{'=' * 31}"
    )

    console.print(f"Total de Unidades: [black]{total_de_unidades}[/black]")
    console.print(f"Total de Lotes en Registro: [black]{total_de_lotes}[/black]")

    console.print(
        f"Total Lotes[bold green]{conv_to_super(total_de_lotes)}[/bold green] Stock Critico[bold yellow]{conv_to_super((total_stock_critico))}[/bold yellow] Agotados[bold red]{conv_to_super(total_sin_stock)}[/bold red]"
    )
    console.print(
        f"Lotes Validos[bold green]{conv_to_super(total_de_lotes - total_sin_stock - total_de_vencidos)}[/bold green] Por Vencer[bold yellow]{conv_to_super(total_vencimiento_critico)}[/bold yellow] Vencidos[bold red]{conv_to_super(total_de_vencidos)}[/bold red]"
    )

    console.print("""\nMENU DE OPCIONES:
    1. Cambiar Umbrales de Stock y Vencimiento.
    2. Mostrar Total de Lotes
    3. Buscar un producto
    4. Agregar un Lote
    5. Eliminar un Lote
    6. Salir\n""")

    opcion_menu = input("Ingresar opcion:  ")

    match opcion_menu:
        case "1":
            console.print(
                "Ingrese Umbral Stock. [i]Actual[/i] "
                + "([i]"
                + str(umbral_stock_critico)
                + "[/i]): ",
                end="",
            )

            umbral_stock_critico, check = num_es_valido(input())
            if check == "✔️\n":
                console.print(check, end="")

            console.print(
                "Ingrese Umbral Vencimiento. [i]Actual[/i] "
                + "([i]"
                + str(umbral_vencimiento_critico)
                + "[/i]): ",
                end="",
            )
            umbral_vencimiento_critico, check = num_es_valido(input())
            if check == "✔️\n":
                console.print(check, end="")

            input("\nENTER para volver al menu ")
            continue

        case "2":
            borrar_consola()

            table = Table(title="Lotes en Registro")
            table.add_column("Lote", justify="left", style="dark_olive_green1", no_wrap=True)
            table.add_column("SKU", justify="left", style="dark_turquoise ", no_wrap=True)
            table.add_column(
                "Producto", justify="left", style="turquoise4", no_wrap=True
            )
            table.add_column(
                "Origen", justify="left", style="green4", no_wrap=True
            )
            table.add_column(
                "Fecha de Vencimiento",
                justify="right",
                style="steel_blue bold",
                no_wrap=True,
            )
            table.add_column(
                "Unidades en Stock", justify="right", style="steel_blue bold", no_wrap=True
            )
            table.add_column(
                "Precio", justify="right", style="wheat4 bold", no_wrap=True
            )

            for k, v in invt.items():
                unidades = v["cantidad_unidades_en_stock"]
                fechas=v['fecha_de_vencimiento']


                if unidades != "N/A" and unidades  <= umbral_stock_critico and unidades > 0:
                    stock_con_estilo = (
                        f"[yellow bold blink]{unidades}[/bold yellow blink]"
                    )
                elif unidades == 0:
                    stock_con_estilo = f"[red bold blink]{unidades}[/bold red blink]"

                else:
                    stock_con_estilo = f"{unidades}"
                
                if fechas != "N/A" and hoy <= datetime.strptime(fechas, "%Y-%m-%d").date() <= fecha_limite:
                    fecha_con_estilo = (
                        f"[yellow bold blink]{fechas}[/bold yellow blink]"
                    )
                elif fechas != "N/A" and hoy > datetime.strptime(v["fecha_de_vencimiento"], "%Y-%m-%d").date():
                    fecha_con_estilo = f"[red bold blink]{fechas}[/bold red blink]"

                else:
                    fecha_con_estilo = f"{fechas}"

                table.add_row(
                    f"{k[0]}",
                    f"{k[1]}",
                    f"{v['producto']}",
                    f"{v['pais_de_origen']}",
                    f"{fecha_con_estilo}",
                    f"{stock_con_estilo}",
                    f"{v['precio']}",
                )
                # table.add_row(stock_con_estilo)

            console.print(table)

            input("\nENTER para volver al menu ")

            continue

        case "3":
            continue
        case "4":
            continue
        case "5":
            continue
        case "6":
            console.print("Saliendo...\n")
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
