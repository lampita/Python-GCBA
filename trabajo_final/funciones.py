import os
from rich.table import Table
from rich.text import Text
from datetime import datetime

hoy = datetime.now().date()


def borrar_consola():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def conv_to_super(n):
    super = list(map(chr, [8304, 185, 178, 179, 8308, 8309, 8310, 8311, 8312, 8313]))
    st = ""
    for i in str(n):
        st += super[int(i)]
    return st


def num_es_valido(num):
    if not num.strip():
        return (" ->Dato Vacío -> No se modificó el valor.\n"), "❌ "
    if not num.isdigit():  ##isdigt() tambien devuelve False en casos de str que representen numeros negativos
        return (" ->Dato Erroneo -> No se modificó el valor.\n"), "❌ "
    if int(num) < 0:
        return (" ->Numero Negativo-> No se modificó el valor.\n"), "❌ "
    else:
        return int(num), "✔️\n"


def float_es_valido(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def validar_fecha(cadena_fecha):
    try:
        datetime.strptime(cadena_fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def agregar_ultima_clave(clave):
    penultimo_lote = []
    for caracter in clave[::-1]:
        if caracter.isdigit():
            penultimo_lote.append(caracter)
        else:
            break
    penultimo_lote.reverse()
    ultima_clave = "".join(penultimo_lote)
    ultima_clave = str(int(ultima_clave) + 1)
    return "LOTE-" + ultima_clave


def crear_tabla(resultados, titulo, query=None):
    table = Table(title=titulo)
    table.add_column("Lote", justify="left", style="orange3 bold")
    table.add_column("SKU", justify="left")
    table.add_column("Producto", justify="left")
    table.add_column("Marca", justify="left")
    table.add_column("Origen", justify="left")
    table.add_column("Vence", justify="right")
    table.add_column("Stock", justify="right")
    table.add_column("Precio", justify="right")
    table.add_column("Descripción", justify="left")

    for resultado in resultados:
        lote = Text(str(resultado[0][1]))
        if query is not None:
            lote.highlight_words([query], style="bold yellow", case_sensitive=False)

        sku = Text(str(resultado[0][0]))
        if query is not None:
            sku.highlight_words([query], style="bold yellow", case_sensitive=False)

        producto = Text(str(resultado[1]["producto"]))
        if query is not None:
            producto.highlight_words([query], style="bold yellow", case_sensitive=False)

        marca = Text(str(resultado[1]["nombre_fantasia"]))
        if query is not None:
            marca.highlight_words([query], style="bold yellow", case_sensitive=False)

        origen = Text(str(resultado[1]["pais_de_origen"]))
        if query is not None:
            origen.highlight_words([query], style="bold yellow", case_sensitive=False)

        vence = Text(str(resultado[1]["fecha_de_vencimiento"]))
        if query is not None:
            vence.highlight_words([query], style="bold yellow", case_sensitive=False)
        elif (
            resultado[1]["fecha_de_vencimiento"] != "N/A"
            and hoy
            > datetime.strptime(resultado[1]["fecha_de_vencimiento"], "%Y-%m-%d").date()
        ):
            vence.style = "red bold"

        stock = Text(str(resultado[1]["cantidad_unidades_en_stock"]))
        if query is not None:
            stock.highlight_words([query], style="bold yellow", case_sensitive=False)
        elif resultado[1]["cantidad_unidades_en_stock"] == 0:
            stock.style = "red bold"

        precio = Text(str(resultado[1]["precio"]))
        if query is not None:
            precio.highlight_words([query], style="bold yellow", case_sensitive=False)

        descripcion = Text(str(resultado[1]["pequena_descripcion"]))
        if query is not None:
            descripcion.highlight_words(
                [query], style="bold yellow", case_sensitive=False
            )

        table.add_row(
            lote,
            sku,
            producto,
            marca,
            origen,
            vence,
            stock,
            precio,
            descripcion,
        )
    return table
