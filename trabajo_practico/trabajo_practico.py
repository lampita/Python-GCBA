try:
    import rich

except ImportError:
    print(
        "El módulo 'rich' no está instalado. Por favor, instálalo con: 'pip install rich'"
    )
    exit()

from rich.console import Console
from rich.table import Table
from funciones import crear_tabla, borrar_consola, conv_to_super
from datetime import datetime, timedelta
from base_datos import productos as prod
import prueba as pr

umbral_stock_critico = 50
umbral_vencimiento_critico = 5
console = Console(highlight=False)
hoy = datetime.now().date()






salida_menu = False
while not salida_menu:
    borrar_consola()
    dias_umbral = timedelta(days=umbral_vencimiento_critico)
    fecha_limite = hoy + dias_umbral

    vencimiento_critico = {
        k: v
        for (k, v) in prod.items()
        if v["fecha_de_vencimiento"] != "N/A"
        and v["cantidad_unidades_en_stock"] > 0
        and hoy
        <= datetime.strptime(v["fecha_de_vencimiento"], "%Y-%m-%d").date()
        <= fecha_limite
    }
    vencidos = {
        k: v
        for (k, v) in prod.items()
        if v["fecha_de_vencimiento"] != "N/A"
        and v["cantidad_unidades_en_stock"] > 0
        and hoy > datetime.strptime(v["fecha_de_vencimiento"], "%Y-%m-%d").date()
    }

    stock_critico = {
        k: v
        for (k, v) in prod.items()
        if v["cantidad_unidades_en_stock"] <= umbral_stock_critico
        and v["cantidad_unidades_en_stock"] > 0
    }
    sin_stock = {
        k: v for (k, v) in prod.items() if v["cantidad_unidades_en_stock"] == 0
    }

    total_de_lotes = len(prod)
    total_de_unidades = sum(v["cantidad_unidades_en_stock"] for v in prod.values())
    total_de_vencidos = len(vencidos)
    total_vencimiento_critico = len(vencimiento_critico)
    total_sin_stock = len(sin_stock)
    total_stock_critico = len(stock_critico)

    console.print(
        f"\t{'=' * 31}\n\t[bold red]CONTROL DE STOCK Y VENCIMIENTOS[/bold red]\n\t{'=' * 31}"
    )
    console.print(f"Total de Unidades: [black]{total_de_unidades}[/black]")
    console.print(f"Total de Lotes en Registro: [black]{total_de_lotes}[/black]\n")
    console.print(
        f"Total Lotes[bold green ]{conv_to_super(total_de_lotes)}[/bold green ] Stock Critico[bold yellow]{conv_to_super((total_stock_critico))}[/bold yellow] Agotados[bold red]{conv_to_super(total_sin_stock)}[/bold red]"
    )
    console.print(
        f"Lotes Validos[bold green]{conv_to_super(total_de_lotes - total_sin_stock - total_de_vencidos)}[/bold green] Por Vencer[bold yellow]{conv_to_super(total_vencimiento_critico)}[/bold yellow] Vencidos[bold red]{conv_to_super(total_de_vencidos)}[/bold red]"
    )

    console.print("""\nMENU DE OPCIONES:
    1. Cambiar Umbrales de Stock y Vencimiento.
    2. Mostrar Total de Lotes.
    3. Consolidado no Válidos.             
    4. Buscar un producto.
    5. Agregar un Lote.
    6. Eliminar un Lote.
    7. Salir.\n""")

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

            umbral_stock_critico, check = pr.num_es_valido(input())
            if check == "✔️\n":
                console.print(
                    f"-> Umbral Modificado en {umbral_stock_critico} ", end=check
                )
            else:
                print(check)
                umbral_stock_critico = umbral_stock_critico[0]

            console.print(
                "Ingrese Umbral Vencimiento. [i]Actual[/i] "
                + "([i]"
                + str(umbral_vencimiento_critico)
                + "[/i]): ",
                end="",
            )
            umbral_vencimiento_critico, check = pr.num_es_valido(input())
            if check == "✔️\n":
                console.print(
                    f"-> Umbral Modificado en {umbral_vencimiento_critico} ", end=check
                )  ## revisar.
            else:
                console.print(check)
                umbral_vencimiento_critico = umbral_vencimiento_critico[1]
            input("ENTER para volver al menu ")
            continue

        case "2":
            borrar_consola()

            table = Table(title="Lotes en Registro")
            table.add_column(
                "Lote", justify="left", style="dark_olive_green1", no_wrap=True
            )
            table.add_column(
                "SKU", justify="left", style="dark_turquoise ", no_wrap=True
            )
            table.add_column(
                "Producto", justify="left", style="turquoise4", no_wrap=True
            )
            table.add_column("Origen", justify="left", style="green4", no_wrap=True)
            table.add_column(
                "Fecha de Vencimiento",
                justify="right",
                style="steel_blue bold",
                no_wrap=True,
            )
            table.add_column(
                "Unidades en Stock",
                justify="right",
                style="steel_blue bold",
                no_wrap=True,
            )
            table.add_column(
                "Precio", justify="right", style="wheat4 bold", no_wrap=True
            )

            for k, v in prod.items():
                unidades = v["cantidad_unidades_en_stock"]
                fechas = v["fecha_de_vencimiento"]

                if (
                    unidades != "N/A"
                    and unidades <= umbral_stock_critico
                    and unidades > 0
                ):
                    stock_con_alerta = (
                        f"[yellow bold blink]{unidades}[/bold yellow blink]"
                    )
                elif unidades == 0:
                    stock_con_alerta = f"[red bold blink]{unidades}[/bold red blink]"

                else:
                    stock_con_alerta = f"{unidades}"

                if (
                    fechas != "N/A"
                    and hoy
                    <= datetime.strptime(fechas, "%Y-%m-%d").date()
                    <= fecha_limite
                ):
                    fecha_con_alerta = (
                        f"[yellow bold blink]{fechas}[/bold yellow blink]"
                    )
                elif (
                    fechas != "N/A"
                    and hoy
                    > datetime.strptime(v["fecha_de_vencimiento"], "%Y-%m-%d").date()
                ):
                    fecha_con_alerta = f"[red bold blink]{fechas}[/bold red blink]"

                else:
                    fecha_con_alerta = f"{fechas}"

                table.add_row(
                    f"{k[0]}",
                    f"{k[1]}",
                    f"{v['producto']}",
                    f"{v['pais_de_origen']}",
                    f"{fecha_con_alerta}",
                    f"{stock_con_alerta}",
                    f"{v['precio']}",
                )

            console.print(table)

            input("\nENTER para volver al menu ")

            continue

        case "3":
            borrar_consola()
            lotes_no_validos = sin_stock | vencidos
            console.print("[bold underline]Consolidado[/bold underline]\n")
            consolidado = []
            query = "LOTE"

            for k, v in lotes_no_validos.items():
                consolidado.append((k, v))

            if consolidado == []:
                console.print("No se encontraron resultados")
            else:
                console.print(crear_tabla(consolidado, query))
            input("\nENTER para volver al menu ")
            continue

        case "4":
            borrar_consola()
            table = Table()  # vacía la tabla que queda de una búsqueda anterior.
            query = input("ingrese busqueda: ").lower().strip()
            print()

            resultados = []
            for k, v in prod.items():
                if (
                    query in k[0].lower()
                    or query in k[1].lower()
                    or query in v["producto"].lower()
                    or query in v["nombre_fantasia"].lower()
                    or query in v["pais_de_origen"].lower()
                    or query in v["fecha_de_vencimiento"].lower()
                    or query in str(v["cantidad_unidades_en_stock"]).lower()
                    or query in str(v["precio"]).lower()
                    or query in v["pequena_descripcion"].lower()
                ):
                    resultados.append((k, v))
            if resultados == []:
                console.print("No se encontraron resultados")
            else:
                console.print(crear_tabla(resultados, query))
            

            input("\nENTER para volver al menu ")
            continue

        case "5":
            borrar_consola()
            console.print("[bold underline]Agregar un Lote[/bold underline]\n")
            sku = input("Ingrese SKU: ").strip()
            producto = input("Ingrese Nombre del Producto: ").strip()
            nombre_fantasia = input("Ingrese Nombre de Fantasia (Marca): ").strip()
            pais_de_origen = input("Ingrese Pais de Origen: ").strip()
            fecha_de_compra = input("Ingrese Fecha de Compra (YYYY-MM-DD): ").strip()
            fecha_de_vencimiento = input(
                "Ingrese Fecha de Vencimiento (YYYY-MM-DD): "
            ).strip()
            cantidad_unidades_en_stock = input(
                "Ingrese Cantidad de Unidades en Stock: "
            ).strip()
            precio = input("Ingrese Precio por Unidad: ").strip()
            pequena_descripcion = input("Ingrese Pequeña Descripción: ").strip()
            lote = (sku, f"L{len(prod) + 1:03d}")
            prod[lote] = {
                "producto": producto,
                "nombre_fantasia": nombre_fantasia,
                "pais_de_origen": pais_de_origen,
                "fecha_de_compra": fecha_de_compra,
                "fecha_de_vencimiento": fecha_de_vencimiento,
                "cantidad_unidades_en_stock": int(cantidad_unidades_en_stock),
                "precio": float(precio),
                "pequena_descripcion": pequena_descripcion,
            }
            console.print("\nLote agregado exitosamente!\n")

            input("\nENTER para volver al menu ")
            continue
        case "6":
            borrar_consola()
            console.print("[bold underline]Eliminar un Lote[/bold underline]\n")
            sku = input("Ingrese SKU: ").strip()
            lote_id = input("Ingrese ID del Lote (e.g., L001): ").strip()
            lote = (sku, lote_id)
            if lote in prod:
                del prod[lote]
                console.print("\nLote eliminado exitosamente!\n")
            else:
                console.print("\nLote no encontrado.\n")

            input("\nENTER para volver al menu ")
            continue
        case "7":
            console.print("Saliendo...\n")
            salida_menu = True


# print("--- Productos próximos a vencer (dentro de los próximos 7 días) ---\n")

# # 2. Iterar sobre el diccionario principal
# for sku, datos_producto in prod.items():
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