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
    borrar_consola,
    num_es_valido,
    validar_fecha,
    float_es_valido,
    display,
)
from datetime import datetime, timedelta
import engine_db as engine
import engine_tablas as tablas
import sql_patterns as sql


umbral_stock_critico = 50
umbral_vencimiento_critico = 5
console = Console(highlight=False)
hoy = datetime.now().date()


salida_menu = False
while not salida_menu:
    borrar_consola()
    prod = engine.consultar_base(sql.todos)
    dias_umbral = timedelta(days=umbral_vencimiento_critico)
    fecha_limite = hoy + dias_umbral
    vencimiento_critico = engine.consultar_base(
        sql.por_vencer.format(hoy, fecha_limite)
    )
    vencidos = engine.consultar_base(sql.lote_vencido.format(hoy))
    stock_critico = engine.consultar_base(sql.poco_stock.format(umbral_stock_critico))
    sin_stock = engine.consultar_base(sql.agotados)
    total_de_lotes = len(prod)
    total_de_unidades = engine.consultar_base(sql.unidades)[0][0]
    total_de_vencidos = len(vencidos)
    total_vencimiento_critico = len(vencimiento_critico)
    total_sin_stock = len(sin_stock)
    total_stock_critico = len(stock_critico)

    display(
        total_de_unidades,
        total_de_lotes,
        total_stock_critico,
        total_sin_stock,
        total_de_vencidos,
        total_vencimiento_critico,
        console,
    )

    console.print("""\nMENU DE OPCIONES:
    1. Modificar Umbrales de Stock y Vencimiento.
    2. Ver Total de Lotes.
    3. Ver Total de Lotes no Válidos.             
    4. Buscar por palabra clave.
    5. Agregar un Lote.
    6. Eliminar un Lote.
    7. Actualizar Stock o Precio.
    8. Salir.\n""")

    opcion_menu = input("Ingresar opcion:  ")

    match opcion_menu:
        case "1":
            console.print(
                "Ingrese Umbral Stock. [i](Actual en[/i] "
                + "[i]"
                + str(umbral_stock_critico)
                + " unidades[/i]): ",
                end="",
            )

            modificador_stock, check = num_es_valido(input())
            if check == "✔️\n":
                umbral_stock_critico = modificador_stock
                console.print(
                    f"-> Umbral Modificado en {umbral_stock_critico} unidades ",
                    end=check,
                )
            else:
                console.print(check, modificador_stock)

            console.print(
                "Ingrese Umbral Vencimiento. [i](Actual en[/i] "
                + "[i]"
                + str(umbral_vencimiento_critico)
                + " días[/i]): ",
                end="",
            )
            modificador_vencimiento, check = num_es_valido(input())
            if check == "✔️\n":
                umbral_vencimiento_critico = modificador_vencimiento
                console.print(
                    f"-> Umbral Modificado en {umbral_vencimiento_critico} días ",
                    end=check,
                )
            else:
                console.print(check, modificador_vencimiento)

            input("ENTER para volver al menu ")

        case "2":
            borrar_consola()

            tabla_total = tablas.crear_tabla_total()
            items = engine.consultar_base(sql.todos)
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

                tabla_total.add_row(
                    f"{item[0]}",
                    f"{item[1]}",
                    f"{item[2]}",
                    f"{item[3]}",
                    f"{fecha_con_alerta}",
                    f"{stock_con_alerta}",
                    f"{item[8]}",
                )

            console.print(tabla_total)

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
                console.print(tablas.crear_tabla(consolidado, titulo))
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

                resultados = engine.consultar_base(
                    sql.buscar_palabra.format(
                        query, query, query, query, query, query, query
                    )
                )

                if resultados == []:
                    console.print(
                        "[bold red on white ]NO SE ENCONTRARON RESULTADOS[/bold red on white ]"
                    )
                else:
                    console.print(tablas.crear_tabla(resultados, titulo, query))

                salida = input("\nENTER para continuar... ")

        case "5":
            borrar_consola()
            lote = "Id"
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
                tablas.crear_tabla(
                    [
                        (
                            "Id",
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
            agregar = input("\n ⚠️\tConfirma agregar Lote? (s/n): ").strip().lower()
            if agregar != "s":
                console.print("\n[red on white] No se Agregó el Lote. [/red on white]")
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

            agregado = engine.agregar_producto(registro)
            if agregado:
                console.print(
                    "\n[bold blue1 on white] Lote Agregado Correctamente. [/bold blue1 on white]"
                )

            input("\nENTER para volver al menu ")

        case "6":
            borrar_consola()

            console.print("[bold underline]BORRAR LOTE[/bold underline]\n")
            lote_id = input("Número de Lote a Borrar: ").strip()
            if not lote_id.isdigit():
                console.print("\n[red on white] Dato no Valido.[/red on white]")
                input("\nENTER para volver al menu ")
                continue

            para_borrar = engine.consultar_base(sql.por_id.format(lote_id))

            if para_borrar != []:
                console.print(
                    tablas.crear_tabla(
                        para_borrar,
                        "[bold underline]LOTE A BORRAR[/bold underline] 👇\n",
                    )
                )
                borrar = (
                    input("\n ⛔\tConfirma eliminar el Lote? (s/n): ").strip().lower()
                )
                if borrar != "s":
                    console.print("\n[red on white] No se borró. [/red on white]")
                    input("\nENTER para volver al menu ")
                    continue
                else:
                    borrado = engine.eliminar_lote(lote_id)
                    if borrado:
                        console.print(
                            "\n[bold blue1 on white] Lote Borrado Correctamente. [/bold blue1 on white]"
                        )

                input("\nENTER para volver al menu ")

            else:
                console.print(
                    "\n[red on white] ADVERTENCIA: Lote Inexistente. [/red on white]\n"
                )
                input("\nENTER para volver al menu ")

        case "7":
            borrar_consola()
            console.print(
                "[bold underline]ACTUALIZAR STOCK O PRECIO[/bold underline]\n"
            )
            lote_id = input("Número de Lote a Actualizar: ").strip()
            if not lote_id.isdigit():
                console.print("\n[red on white] Dato no Valido.[/red on white]")
                input("\nENTER para volver al menu ")
                continue

            para_actualizar = engine.consultar_base(sql.por_id.format(lote_id))

            if para_actualizar != []:
                console.print(
                    tablas.crear_tabla(
                        para_actualizar,
                        "[bold underline]LOTE A ACTUALIZAR[/bold underline] 👇\n",
                    )
                )
                actualizar = (
                    input("\n ⚠️\tConfirma actualizar el Lote? (s/n): ").strip().lower()
                )
                if actualizar != "s":
                    console.print("\n[red on white] No se actualizó. [/red on white]")
                    input("\nENTER para volver al menu ")
                    continue
                else:
                    nuevo_stock = input("\nNuevo Stock: ").strip()
                    if not nuevo_stock.isdigit():
                        nuevo_stock = None
                        console.print(
                            "\n[red on white] ADVERTENCIA: No se modifico el Stock. [/red on white]\n"
                        )
                    nuevo_precio = input("\nNuevo Precio: ").strip()

                    if not float_es_valido(nuevo_precio):
                        nuevo_precio = None
                        console.print(
                            "\n[red on white] ADVERTENCIA: No se modifico el Precio. [/red on white]\n"
                        )

                    if nuevo_stock is None and nuevo_precio is None:
                        console.print(
                            "\n[bold red on white] ADVERTENCIA: No se modifico el Lote. [/bold red on white]"
                        )
                        input("\nENTER para volver al menu ")
                        continue

                    else:
                        actualizado = engine.actualizar_lote(
                            lote_id, nuevo_stock, nuevo_precio
                        )
                        if actualizado:
                            console.print(
                                "\n[bold blue1 on white] Lote Actualizado Correctamente. [/bold blue1 on white]"
                            )
                            console.print(
                                f"\n[bold blue1 on white] Nuevo Stock= {nuevo_stock} - Nuevo Precio= {nuevo_precio} [/bold blue1 on white]"
                            )
                        input("\nENTER para volver al menu ")

            else:
                console.print(
                    "\n[red on white] ADVERTENCIA: Lote Inexistente. [/red on white]\n"
                )
                input("\nENTER para volver al menu ")

        case "8":
            console.print("Saliendo...\n")
            salida_menu = True
