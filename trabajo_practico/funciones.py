import os
from rich.console import Console
from rich.table import Table
from rich.text import Text
#console = Console(highlight=False)
#umbral_stock_critico = 50
#umbral_vencimiento_critico = 5
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





def crear_tabla(resultados, query="LOTE"):

    
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

        
        
            
        lote = Text(str(resultado[0][1]))
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
    return table