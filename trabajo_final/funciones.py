import os

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


def display(
    total_de_unidades,
    total_de_lotes,
    total_stock_critico,
    total_sin_stock,
    total_de_vencidos,
    total_vencimiento_critico,
    console,
):
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
