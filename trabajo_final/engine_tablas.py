from rich.table import Table
from rich.text import Text
from datetime import datetime

hoy = datetime.now().date()


def crear_tabla_total():
    table = Table(
        title="[bold underline ]\nTOTAL DE LOTES EN REGISTRO\n[/bold underline]"
    )
    table.add_column("Lote", justify="left", style="dark_olive_green1", no_wrap=True)
    table.add_column("SKU", justify="left", style="dark_turquoise ", no_wrap=True)
    table.add_column("Producto", justify="left", style="turquoise4", no_wrap=True)
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
    table.add_column("Precio", justify="right", style="wheat4 bold", no_wrap=True)
    return table


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
        lote = Text(str(resultado[0]))
        if query is not None:
            lote.highlight_words([query], style="bold yellow", case_sensitive=False)

        sku = Text(str(resultado[1]))
        if query is not None:
            sku.highlight_words([query], style="bold yellow", case_sensitive=False)

        producto = Text(str(resultado[2]))
        if query is not None:
            producto.highlight_words([query], style="bold yellow", case_sensitive=False)

        marca = Text(str(resultado[3]))
        if query is not None:
            marca.highlight_words([query], style="bold yellow", case_sensitive=False)

        origen = Text(str(resultado[5]))
        if query is not None:
            origen.highlight_words([query], style="bold yellow", case_sensitive=False)

        vence = Text(str(resultado[6]))
        if query is not None:
            vence.highlight_words([query], style="bold yellow", case_sensitive=False)
        elif (
            resultado[6] != "N/A"
            and hoy > datetime.strptime(resultado[6], "%Y-%m-%d").date()
        ):
            vence.style = "red bold"

        stock = Text(str(resultado[7]))
        if query is not None:
            stock.highlight_words([query], style="bold yellow", case_sensitive=False)
        elif resultado[7] == 0:
            stock.style = "red bold"

        precio = Text(str(resultado[8]))
        if query is not None:
            precio.highlight_words([query], style="bold yellow", case_sensitive=False)

        descripcion = Text(str(resultado[9]))
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
