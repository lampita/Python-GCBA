# Sentencias SQL

inicia_tabla = """CREATE TABLE IF NOT EXISTS productos(
               lote INTEGER PRIMARY KEY AUTOINCREMENT,
               sku TEXT DEFAULT 'N/A',
               producto TEXT DEFAULT 'N/A',
               nombre_fantasia TEXT DEFAULT 'N/A',
               fecha_de_compra DATE DEFAULT 'N/A',
               pais_de_origen TEXT DEFAULT 'N/A',
               fecha_de_vencimiento DATE DEFAULT 'N/A',
               cantidad_unidades_en_stock INTEGER DEFAULT 0,
               precio REAL DEFAULT 0,
               pequena_descripcion TEXT DEFAULT 'N/A'
               )"""

todos = "SELECT * FROM productos"
por_id = "SELECT * FROM productos WHERE lote = {}"
por_vencer = "SELECT * FROM productos WHERE fecha_de_vencimiento != 'N/A' AND cantidad_unidades_en_stock > 0 AND fecha_de_vencimiento BETWEEN '{}' AND '{}'"
lote_vencido = "SELECT * FROM productos WHERE fecha_de_vencimiento != 'N/A' AND cantidad_unidades_en_stock > 0 AND fecha_de_vencimiento < '{}'"
poco_stock = "SELECT * FROM productos WHERE cantidad_unidades_en_stock <= {} AND cantidad_unidades_en_stock > 0"
agotados = "SELECT * FROM productos WHERE cantidad_unidades_en_stock = 0"
unidades = "SELECT SUM(cantidad_unidades_en_stock) FROM productos"
buscar_palabra = "SELECT * FROM productos WHERE producto LIKE '%{}%' OR nombre_fantasia LIKE '%{}%' OR pais_de_origen LIKE '%{}%' OR fecha_de_vencimiento LIKE '%{}%' OR cantidad_unidades_en_stock LIKE '%{}%' OR precio LIKE '%{}%' OR pequena_descripcion LIKE '%{}%'"
inserta_en_campos = (
    "sku",
    "producto",
    "nombre_fantasia",
    "fecha_de_compra",
    "pais_de_origen",
    "fecha_de_vencimiento",
    "cantidad_unidades_en_stock",
    "precio",
    "pequena_descripcion",
)
