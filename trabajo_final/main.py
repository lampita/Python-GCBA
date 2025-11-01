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
import engine


umbral_stock_critico = 50
umbral_vencimiento_critico = 5
console = Console(highlight=False)
hoy = datetime.now().date()


salida_menu = False
while not salida_menu:
    borrar_consola()
    prod = engine.consultar_base("SELECT * FROM productos")
    dias_umbral = timedelta(days=umbral_vencimiento_critico)
    fecha_limite = hoy + dias_umbral

    pattern_vc = f"SELECT * FROM productos WHERE fecha_de_vencimiento != 'N/A' AND cantidad_unidades_en_stock > 0 AND fecha_de_vencimiento BETWEEN '{hoy}' AND '{fecha_limite}'"
    vencimiento_critico = engine.consultar_base(pattern_vc)

    pattern_v = f"SELECT * FROM productos WHERE fecha_de_vencimiento != 'N/A' AND cantidad_unidades_en_stock > 0 AND fecha_de_vencimiento < '{hoy}'"
    vencidos = engine.consultar_base(pattern_v)

    pattern_sc = f"SELECT * FROM productos WHERE cantidad_unidades_en_stock <= {umbral_stock_critico} AND cantidad_unidades_en_stock > 0"
    stock_critico = engine.consultar_base(pattern_sc)

    pattern_ss = "SELECT * FROM productos WHERE cantidad_unidades_en_stock = 0"
    sin_stock = engine.consultar_base(pattern_ss)

    total_de_lotes = len(prod)
    pattern_tu = "SELECT SUM(cantidad_unidades_en_stock) FROM productos"
    total_de_unidades = engine.consultar_base(pattern_tu)[0][0]
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

            items = engine.consultar_base("SELECT * FROM productos")
            for item in items:
                unidades = int(item[7])

                fechas = item[6]

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
                    and hoy > datetime.strptime(fechas, "%Y-%m-%d").date()
                ):
                    fecha_con_alerta = f"[red bold ]{fechas}[/bold red ]"

                else:
                    fecha_con_alerta = f"{fechas}"

                table.add_row(
                    f"{item[0]}",
                    f"{item[1]}",
                    f"{item[2]}",
                    f"{item[3]}",
                    f"{fecha_con_alerta}",
                    f"{stock_con_alerta}",
                    f"{item[7]}",
                )

            console.print(table)

            input("\nENTER para volver al menu ")

        case "3":
            borrar_consola()

            lotes_no_validos = sin_stock + vencidos
            consolidado = []

            titulo = "[bold underline]TOTAL DE LOTES NO VÁLIDOS PARA LA VENTA[/bold underline]\n"
            for registro in lotes_no_validos:
                consolidado.append(registro)

            if consolidado == []:
                console.print(
                    "[red on white bold]NO SE ENCONTRARON LOTES NO VÁLIDOS[/red on white bold]"
                )
            else:
                console.print(crear_tabla(consolidado, titulo))
            input("\nENTER para volver al menu ")

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
                pattern_query = f"SELECT * FROM productos WHERE producto LIKE '%{query}%' OR nombre_fantasia LIKE '%{query}%' OR pais_de_origen LIKE '%{query}%' OR fecha_de_vencimiento LIKE '%{query}%' OR cantidad_unidades_en_stock LIKE '%{query}%' OR precio LIKE '%{query}%' OR pequena_descripcion LIKE '%{query}%'"
                resultados = engine.consultar_base(pattern_query)

                if resultados == []:
                    console.print(
                        "[bold red on white ]NO SE ENCONTRARON RESULTADOS[/bold red on white ]"
                    )
                else:
                    console.print(crear_tabla(resultados, titulo, query))

                salida = input("\nENTER para continuar... ")

        case "5":
            borrar_consola()
            lote = "Id Incremental"
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

            titulo = "[bold underline]LOTE A REGISTRAR[/bold underline] 👇\n"
            console.print(
                crear_tabla(
                    [
                        (
                            "Id Incremental",
                            sku,
                            producto,
                            nombre_fantasia,
                            fecha_de_compra,
                            pais_de_origen,
                            fecha_de_vencimiento,
                            int(cantidad_unidades_en_stock),
                            float(precio),
                            pequena_descripcion,
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
            registro = (
                sku,
                producto,
                nombre_fantasia,
                fecha_de_compra,
                pais_de_origen,
                fecha_de_vencimiento,
                int(cantidad_unidades_en_stock),
                float(precio),
                pequena_descripcion,
            )

            engine.agregar_producto(registro)

            input("\nENTER para volver al menu ")

        case "6":
            borrar_consola()

            console.print("[bold underline]BORRAR LOTE[/bold underline]\n")
            lote_id = input("Número de Lote a Borrar: ").strip()
            if not lote_id.isdigit():
                console.print("\n[red on white] Dato no Valido.[/red on white]")
                input("\nENTER para volver al menu ")
                continue
            pattern_id = f"SELECT * FROM productos WHERE lote = {lote_id}"
            para_borrar = engine.consultar_base(pattern_id)

            if para_borrar != []:
                console.print(
                    crear_tabla(
                        para_borrar,
                        "[bold underline]LOTE A BORRAR[/bold underline] 👇\n",
                    )
                )
                borrar = (
                    input("\n🛑\tConfirma eliminar el Lote? (s/n): ").strip().lower()
                )
                if borrar != "s":
                    console.print("No se borró.")
                    input("\nENTER para volver al menu ")
                    continue
                else:
                    engine.eliminar_lote(lote_id)
                input("\nENTER para volver al menu ")

            else:
                console.print(
                    "\n[red on white] ADVERTENCIA: Lote Inexistente. [/red on white]\n"
                )
                input("\nENTER para volver al menu ")

        case "7":
            console.print("Saliendo...\n")
            salida_menu = True
