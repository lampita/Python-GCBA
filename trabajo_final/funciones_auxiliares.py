import os
from datetime import datetime

def borrar_consola():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def conv_to_super(n):
    """Devuelve el numero ingresado como un string-superindice, usando la funcion chr() de Python"""
    super = list(map(chr, [8304, 185, 178, 179, 8308, 8309, 8310, 8311, 8312, 8313]))
    st = ""
    for i in str(n):
        st += super[int(i)]
    return st


def num_es_valido(num):
    """Valida un numero entero ingresado por el usuario. Si es valido devuelve una tupla con el numero convertido
    en un entero o, caso contrario, el mensaje de error al validar.
    En ambos casos el segundo valor de la tupla es un flag indicando si es valido o no."""
    if not num.strip():
        return (" ->Dato Vacío -> No se modificó el valor.\n"), "❌ "
    if not num.isdigit():  ##isdigt() tambien devuelve False en casos de str que representen numeros negativos
        return (" ->Dato Erroneo -> No se modificó el valor.\n"), "❌ "
    if int(num) < 0:
        return (" ->Numero Negativo-> No se modificó el valor.\n"), "❌ "
    else:
        return int(num), "✔️\n"


def float_es_valido(num):
    """Valida un numero flotante ingresado por el usuario. Si es valido devuelve True, caso contrario False."""
    try:
        float(num)
        return True
    except ValueError:
        return False


def validar_fecha(cadena_fecha):
    """Valida una fecha ingresada por el usuario. Si la fecha es valida devuelve True, caso contrario False."""
    try:
        datetime.strptime(cadena_fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def display(
    total_de_unidades,
    total_de_lotes,
    total_stock_critico,
    total_sin_stock,
    total_de_vencidos,
    total_vencimiento_critico,
    console,
):
    """Muestra el total de lotes y unidades. Muestra con superindices los lotes validos, criticos e invalidos"""
    console.print(
        f"\t{'=' * 31}\n\t[bold red]CONTROL DE STOCK Y VENCIMIENTOS[/bold red]\n\t{'=' * 31}"
    )
    console.print(f"Total de Unidades: [orange3]{total_de_unidades}[/orange3]")
    console.print(f"Total de Lotes en Registro: [orange3]{total_de_lotes}[/orange3]\n")
    console.print(
        f"Total Lotes[bold green ]{conv_to_super(total_de_lotes)}[/bold green ]"
    )
    console.print(
        f"Lotes Validos[bold green]{conv_to_super(total_de_lotes - total_sin_stock - total_de_vencidos)}[/bold green]")
    
    console.print(
        f"Stock Critico[bold yellow]{conv_to_super((total_stock_critico))}[/bold yellow] Agotados[bold red]{conv_to_super(total_sin_stock)}[/bold red]"
    )
    console.print(
        f"Por Vencer[bold yellow]{conv_to_super(total_vencimiento_critico)}[/bold yellow] Vencidos[bold red]{conv_to_super(total_de_vencidos)}[/bold red]"
    )
