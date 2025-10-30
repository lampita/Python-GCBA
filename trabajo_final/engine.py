import sqlite3
import os

directorio_script = os.path.dirname(os.path.abspath(__file__))
ruta_db_completa = os.path.join(directorio_script, "productos.db")

conexion = sqlite3.connect(ruta_db_completa)
cursor = conexion.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS productos(
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
               )""")

conexion.commit()
conexion.close()
campos = (
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
lote = (
    "MG-BAN-PE",
    "Banana",
    "Pedorra",
    "2025-06-12",
    "Brasil",
    "2025-06-18",
    20,
    1.90,
    "banana de mierda",
)


def agregar_producto(lote):
    conexion = sqlite3.connect(ruta_db_completa)
    cursor = conexion.cursor()
    try:
        cursor.execute(
            f"INSERT INTO productos {campos} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            lote,
        )

        conexion.commit()

    except sqlite3.Error as e:
        print(f"Ocurrió un error al insertar el producto: {e}")

    finally:
        if conexion:
            conexion.close()


def consultar_base():
    conexion = sqlite3.connect(ruta_db_completa)
    cursor = conexion.cursor()
    try:
        productos = []
        cursor.execute("SELECT * FROM productos")
        items = cursor.fetchall()

        for item in items:
            productos.append(item)

        return productos

    except sqlite3.Error as e:
        print(f"Ocurrió un error al consultar con la base de datos: {e}")

    finally:
        if conexion:
            conexion.close()

def consultar_base_segun(query):
    conexion = sqlite3.connect(ruta_db_completa)
    cursor = conexion.cursor()
    try:
        productos = []
        cursor.execute(f"SELECT * FROM productos WHERE producto LIKE '%{query}%'")
        items = cursor.fetchall()

        for item in items:
            productos.append(item)

        return productos

    except sqlite3.Error as e:
        print(f"Ocurrió un error al buscar: {e}")

    finally:
        if conexion:
            conexion.close()

def eliminar_lote(lote): #falta confirmar que el registro exista
    conexion = sqlite3.connect(ruta_db_completa)
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM productos WHERE lote=?",(lote,))

        print( "Borrado Correctamente")
        conexion.commit()


    except sqlite3.Error as e:
        print(f"Ocurrió un error al borrar el producto: {e}")

    finally:
        if conexion:
            conexion.close()

#agregar_producto(lote)
#print(consultar_base())
#print(consultar_base_segun("pera"))
#eliminar_lote()




