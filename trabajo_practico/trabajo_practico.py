try:
    import rich

except ImportError:
    print(
        "El módulo 'rich' no está instalado. Por favor, instálalo con: 'pip install rich'"
    )
    exit()

from rich.console import Console
from rich.table import Table
from rich.text import Text
import os

from datetime import datetime, timedelta
from base_datos import productos as prod


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
        return (
            umbral_stock_critico,
            umbral_vencimiento_critico,
        ), "❌ ->Dato Vacío -> No se modificó el valor.\n"
    if any(not num.isdigit() for num in num):
        return (
            umbral_stock_critico,
            umbral_vencimiento_critico,
        ), "❌ ->Dato Erroneo -> No se modificó el valor.\n"
    else:
        return int(num), "✔️\n"


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

            umbral_stock_critico, check = num_es_valido(input())
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
            umbral_vencimiento_critico, check = num_es_valido(input())
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
            console.print("[bold underline]Consolidado[/bold underline]\n")
            console.print(vencidos)
            for k, v in vencidos.items():
                print(k, v["producto"])

            input("\nENTER para volver al menu ")
            continue

        case "4":
            borrar_consola()
            table = Table() #vacía la tabla que queda de una búsqueda anterior.
            query = input("ingrese busqueda: ").lower().strip()
            print()

            resultados=[]
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
                    resultados.append((k,v))           
                    

                    table = Table(title="Busqueda. Palabra clave: " + query)
                    table.add_column("Lote", justify="left")
                    table.add_column("SKU", justify="left")
                    table.add_column("Producto", justify="left")
                    table.add_column("Marca", justify="left")
                    table.add_column("Comprado", justify="right")
                    table.add_column("Origen", justify="left")
                    table.add_column("Vence", justify="right")
                    table.add_column("Stock", justify="right")
                    table.add_column("Precio", justify="right")
                    table.add_column("Descripción", justify="left")


                    for resultado in resultados:

                       
                        
                            
                        lote = Text(str(resultado[0][0]))
                        lote.highlight_words(
                            [query], style="bold yellow", case_sensitive=False
                        )

                        sku = Text(str(resultado[0][0]))
                        sku.highlight_words(
                            [query], style="bold yellow", case_sensitive=False
                        )

                        producto = Text(str(resultado[1]["producto"]))
                        producto.highlight_words(
                            [query], style="bold yellow", case_sensitive=False
                        )

                        marca = Text(str(resultado[1]["nombre_fantasia"]))
                        marca.highlight_words(
                            [query], style="bold yellow", case_sensitive=False
                        )

                        comprado = Text(str(resultado[1]["cantidad_unidades_en_stock"]))
                        comprado.highlight_words(
                            [query], style="bold yellow", case_sensitive=False
                        )

                        origen = Text(str(resultado[1]["pais_de_origen"]))
                        origen.highlight_words(
                            [query], style="bold yellow", case_sensitive=False
                        )

                        vence = Text(str(resultado[1]["fecha_de_vencimiento"]))
                        vence.highlight_words(
                            [query], style="bold yellow", case_sensitive=False
                        )

                        stock = Text(str(resultado[1]["cantidad_unidades_en_stock"]))
                        stock.highlight_words(
                            [query], style="bold yellow", case_sensitive=False
                        )

                        precio = Text(str(resultado[1]["precio"]))
                        precio.highlight_words(
                            [query], style="bold yellow", case_sensitive=False
                        )

                        descripcion = Text(str(resultado[1]["pequena_descripcion"]))
                        descripcion.highlight_words(
                            [query], style="bold yellow", case_sensitive=False
                        )

                        table.add_row(
                            lote,
                            sku,
                            producto,
                            marca,
                            comprado,
                            origen,
                            vence,
                            stock,
                            precio,
                            descripcion,
                        )

            if resultados==[]:
                 console.print("No se encontraron resultados")
            else:
                console.print(table)
            

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
