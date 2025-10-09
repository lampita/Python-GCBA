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