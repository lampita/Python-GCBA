try:
    import rich

except ImportError:
    print(
        "El módulo 'rich' no está instalado. Por favor, instálalo con: 'pip install rich'"
    )
    exit()

from rich.console import Console
from rich.table import Table
from funciones import (
    crear_tabla,
    borrar_consola,
    conv_to_super,
    num_es_valido,
    validar_fecha,
    float_es_valido,
)
from datetime import datetime, timedelta
from base_datos import productos as prod


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
    console.print(f"Total de Unidades: [orange3]{total_de_unidades}[/orange3]")
    console.print(f"Total de Lotes en Registro: [orange3]{total_de_lotes}[/orange3]\n")
    console.print(
        f"Total Lotes[bold green ]{conv_to_super(total_de_lotes)}[/bold green ] Stock Critico[bold yellow]{conv_to_super((total_stock_critico))}[/bold yellow] Agotados[bold red]{conv_to_super(total_sin_stock)}[/bold red]"
    )
    console.print(
        f"Lotes Validos[bold green]{conv_to_super(total_de_lotes - total_sin_stock - total_de_vencidos)}[/bold green] Por Vencer[bold yellow]{conv_to_super(total_vencimiento_critico)}[/bold yellow] Vencidos[bold red]{conv_to_super(total_de_vencidos)}[/bold red]"
    )

    console.print("""\nMENU DE OPCIONES:
    1. Cambiar Umbrales de Stock y Vencimiento.
    2. Total de Lotes.
    3. Total de Lotes no válidos.             
    4. Buscar por palabra clave.
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

            modificador_stock, check = num_es_valido(input())
            if check == "✔️\n":
                umbral_stock_critico = modificador_stock
                console.print(
                    f"-> Umbral Modificado en {umbral_stock_critico} ", end=check
                )
            else:
                console.print(check, modificador_stock)

            console.print(
                "Ingrese Umbral Vencimiento. [i]Actual[/i] "
                + "([i]"
                + str(umbral_vencimiento_critico)
                + "[/i]): ",
                end="",
            )
            modificador_vencimiento, check = num_es_valido(input())
            if check == "✔️\n":
                umbral_vencimiento_critico = modificador_vencimiento
                console.print(
                    f"-> Umbral Modificado en {umbral_vencimiento_critico} ", end=check
                )
            else:
                console.print(check, modificador_vencimiento)

            input("ENTER para volver al menu ")
            continue

        case "2":
            borrar_consola()

            table = Table(
                title="[bold underline ]\nTOTAL DE LOTES EN REGISTRO\n[/bold underline]"
            )
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
                    stock_con_alerta = f"[yellow bold ]{unidades}[/bold yellow ]"
                elif unidades == 0:
                    stock_con_alerta = f"[red bold ]{unidades}[/bold red ]"

                else:
                    stock_con_alerta = f"{unidades}"

                if (
                    fechas != "N/A"
                    and hoy
                    <= datetime.strptime(fechas, "%Y-%m-%d").date()
                    <= fecha_limite
                ):
                    fecha_con_alerta = f"[yellow bold ]{fechas}[/bold yellow ]"
                elif (
                    fechas != "N/A"
                    and hoy
                    > datetime.strptime(v["fecha_de_vencimiento"], "%Y-%m-%d").date()
                ):
                    fecha_con_alerta = f"[red bold ]{fechas}[/bold red ]"

                else:
                    fecha_con_alerta = f"{fechas}"

                table.add_row(
                    f"{k[1]}",
                    f"{k[0]}",
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
            consolidado = []

            titulo = "[bold underline]TOTAL DE LOTES NO VÁLIDOS PARA LA VENTA[/bold underline]\n"
            for k, v in lotes_no_validos.items():
                consolidado.append((k, v))

            if consolidado == []:
                console.print(
                    "[red on white bold]NO SE ENCONTRARON LOTES NO VÁLIDOS[/red on white bold]"
                )
            else:
                console.print(crear_tabla(consolidado, titulo))
            input("\nENTER para volver al menu ")
            continue

        case "4":
            while True:
                borrar_consola()
                table = Table()  # vacía la tabla que queda de una búsqueda anterior.

                query = (
                    input(
                        "\n  🔎 BUSCAR PALABRA CLAVE (o escriba 'salir' para terminar) =>  "
                    )
                    .lower()
                    .strip()
                )
                if query == "salir":
                    break
                elif query == "":
                    continue

                titulo = f" 🔎  MOSTRANDO PALABRA CLAVE: [bold red underline]{query.upper()}[/bold red underline]\n"
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
                    console.print(
                        "[bold red on white ]NO SE ENCONTRARON RESULTADOS[/bold red on white ]"
                    )
                else:
                    console.print(crear_tabla(resultados, titulo, query))

                salida = input("\nENTER para continuar... ")
                continue

        case "5":
            borrar_consola()
            ultima_clave = list(prod.keys())[-1]
            console.print("[bold underline]AGREGAR LOTE[/bold underline]\n")
            sku = []
            for i in range(3):
                codigo = input(f"Ingrese SKU {i + 1}º Codigo: ").strip().upper()
                sku.append(codigo)
            sku = "-".join(sku)
            if sku == "--":
                sku = "N/A"
            console.print(f"\n[red bold]SKU ingresado:[/red bold] {sku}\n")

            producto = input("Tipo de Producto: ").strip().capitalize()
            if producto == "":
                producto = "N/A"
            nombre_fantasia = input("Nombre del  Producto: ").strip().capitalize()
            if nombre_fantasia == "":
                nombre_fantasia = "N/A"
            pais_de_origen = input("Ingrese Pais de Origen: ").strip().capitalize()
            if pais_de_origen == "":
                pais_de_origen = "N/A"
            fecha_de_compra = hoy.strftime("%Y-%m-%d")
            vence = []
            formato = ["YYYY", "MM", "DD"]
            for i in range(3):
                fecha = input(f"Ingrese Fecha de Vencimiento ({formato[i]}): ").strip()
                vence.append(fecha)
            fecha_de_vencimiento = "-".join(vence)
            if not validar_fecha(fecha_de_vencimiento):
                fecha_de_vencimiento = "N/A"
                console.print(
                    "\n[red on white] ADVERTENCIA: introdujo una fecha incorrecta. Se asignó 'N/A' [/red on white]\n"
                )

            cantidad_unidades_en_stock = input("Unidades en el Lote: ")
            if not cantidad_unidades_en_stock.isdigit():
                cantidad_unidades_en_stock = "0"
                console.print(
                    "\n[red on white] ADVERTENCIA: introdujo una valor incorrecto. Se asignó 0 [/red on white]\n"
                )

            precio = input("Precio por Unidad: ")
            if not float_es_valido(precio):
                precio = "0"
                console.print(
                    "\n[red on white] ADVERTENCIA: introdujo una valor incorrecto. Se asignó 0.0 [/red on white]\n"
                )

            pequena_descripcion = input("Descripción: ").strip()
            if pequena_descripcion == "":
                pequena_descripcion = "N/A"

            borrar_consola()

            lote = (sku, f"LOTE-{int(ultima_clave[1].split('-')[1]) + 1}")
            titulo = "[bold underline]LOTE A REGISTRAR[/bold underline] 👇\n"
            console.print(
                crear_tabla(
                    [
                        (
                            lote,
                            {
                                "producto": producto,
                                "nombre_fantasia": nombre_fantasia,
                                "pais_de_origen": pais_de_origen,
                                "fecha_de_compra": fecha_de_compra,
                                "fecha_de_vencimiento": fecha_de_vencimiento,
                                "cantidad_unidades_en_stock": int(
                                    cantidad_unidades_en_stock
                                ),
                                "precio": float(precio),
                                "pequena_descripcion": pequena_descripcion,
                            },
                        )
                    ],
                    titulo,
                )
            )
            agregar = input("\n⚠️\tConfirma agregar Lote? (s/n): ").strip().lower()
            if agregar != "s":
                console.print("\nNo se Agregó el Lote.")
                input("\nENTER para volver al menu ")
                continue

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
            console.print("\nLote agregado con éxito\n")

            input("\nENTER para volver al menu ")
            continue
        case "6":
            borrar_consola()
            por_borrar = []
            console.print("[bold underline]BORRAR LOTE[/bold underline]\n")
            lote_id = input("Número de Lote a Borrar: ").strip()
            lote = f"LOTE-{lote_id}"
            for k, v in prod.items():
                if k[1] == lote:
                    por_borrar.append((k, v))
                    break
            if por_borrar == []:
                console.print(
                    "\n[red on white] ADVERTENCIA: Lote Inexistente. [/red on white]\n"
                )
                input("\nENTER para volver al menu ")
                continue
            titulo = "[bold underline]LOTE A BORRAR[/bold underline] 👇\n"
            console.print(crear_tabla(por_borrar, titulo))

            borrar = input("\n🛑\tConfirma eliminar el Lote? (s/n): ").strip().lower()
            if borrar != "s":
                console.print("No se borró.")
                input("\nENTER para volver al menu ")
                continue
            del prod[por_borrar[0][0]]
            console.print(f"\n{lote} eliminado.\n")

            input("\nENTER para volver al menu ")
            continue
        case "7":
            console.print("Saliendo...\n")
            salida_menu = True

