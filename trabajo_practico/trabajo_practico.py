from datetime import datetime, timedelta
from base_datos import inventario_supermercado as invt

umbral_stock_critico = 50
umbral_vencimiento_critico = 5

hoy = datetime.now().date()
dias_umbral = timedelta(days=umbral_vencimiento_critico)
fecha_limite = hoy + dias_umbral

vencimiento_critico = {
    k: v
    for (k, v) in invt.items()
    if v["fecha_de_vencimiento"] != "N/A"
    and v["cantidad_unidades_en_stock"] > 0
    and hoy
    <= datetime.strptime(v["fecha_de_vencimiento"], "%Y-%m-%d").date()
    <= fecha_limite
}
print("vencimiento_critico-------------->", vencimiento_critico.keys())
for k, v in vencimiento_critico.items():
    print(v.get("producto", {}))

print()
vencidos = {
    k: v
    for (k, v) in invt.items()
    if v["fecha_de_vencimiento"] != "N/A"
    and v["cantidad_unidades_en_stock"] > 0
    and hoy > datetime.strptime(v["fecha_de_vencimiento"], "%Y-%m-%d").date()
}
print("vencidos-------------->", vencidos)

for k, v in vencidos.items():
    print(v.get("producto"))

stock_critico = {
    k: v
    for (k, v) in invt.items()
    if v["cantidad_unidades_en_stock"] < umbral_stock_critico
    and v["cantidad_unidades_en_stock"] > 0
}
sin_stock = {k: v for (k, v) in invt.items() if v["cantidad_unidades_en_stock"] == 0}


# print("--- Productos próximos a vencer (dentro de los próximos 7 días) ---\n")

# # 2. Iterar sobre el diccionario principal
# for sku, datos_producto in invt.items():
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
