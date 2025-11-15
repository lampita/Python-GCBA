import sqlite3
import os

# determina la path del directorio en uso.
directorio_script = os.path.dirname(os.path.abspath(__file__))
# completa la path con el nombre del archivo d el abase de datos.
ruta_db_completa = os.path.join(directorio_script, "productos.db")


def crear_db(inicia_tabla):
    """Inicia la base de datos si no existe. El argumento de su parametro es la instruccion sql
    CREATE TABLE IF NOT EXISTS ...."""
    try:
        conexion = sqlite3.connect(ruta_db_completa)
        cursor = conexion.cursor()

        cursor.execute(inicia_tabla)

        conexion.commit()
        conexion.close()

    except sqlite3.Error as e:
        print(f"Ocurrió un error de SQLite: {e}")

    finally:
        if conexion:
            conexion.close()


def agregar_producto(registro_nuevo, inserta_en_campos):
    """Inserta (sanitizado) un registro en la base de datos. Toma dos parametros. El primero con los valores
    del registro a insertar y el segundo con los campos correspondientes de la tabla."""
    conexion = sqlite3.connect(ruta_db_completa)
    cursor = conexion.cursor()
    try:
        cursor.execute(
            f"INSERT INTO productos {inserta_en_campos} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            registro_nuevo,
        )

        conexion.commit()
        return True

    except sqlite3.Error as e:
        print(f"\nOcurrió un error al insertar el producto: {e}")

    finally:
        if conexion:
            conexion.close()


def consultar_base(todas_las_ocurrencias):
    """Consulta la base de datos y devuelve todas las filas encontradas de acuerdo al argumento sql
    pasado como parametro de entrada."""
    conexion = sqlite3.connect(ruta_db_completa)
    cursor = conexion.cursor()
    try:
        productos = []
        cursor.execute(todas_las_ocurrencias)
        items = cursor.fetchall()

        for item in items:
            productos.append(item)

        return productos

    except sqlite3.Error as e:
        print(f"Ocurrió un error al consultar con la base de datos: {e}")

    finally:
        if conexion:
            conexion.close()


def consultar_base_segun(palabra_clave):
    """Consulta la base de datos y devuelve todas las filas encontradas de acuerdo al argumento
    pasado como parametro de entrada. Busca en todos las campos coincidencia total o parcial."""
    conexion = sqlite3.connect(ruta_db_completa)
    cursor = conexion.cursor()
    try:
        productos = []
        cursor.execute(
            f"SELECT * FROM productos WHERE producto LIKE '%{palabra_clave}%'"
        )
        items = cursor.fetchall()

        for item in items:
            productos.append(item)

        return productos

    except sqlite3.Error as e:
        print(f"Ocurrió un error al buscar: {e}")

    finally:
        if conexion:
            conexion.close()


def eliminar_lote(lote):
    """Elimina un lote de la base de datos de acuerdo al Id pasado como parametro."""
    conexion = sqlite3.connect(ruta_db_completa)
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM productos WHERE lote=?", (lote,))
        conexion.commit()
        return True

    except sqlite3.Error as e:
        print(f"Ocurrió un error al borrar el lote: {e}")

    finally:
        if conexion:
            conexion.close()


def actualizar_lote(lote, unidades=None, precio=None):
    """Actualiza el stock y/o el precio de un lote de la base de datos de acuerdo al Id pasado como parametro."""
    conexion = sqlite3.connect(ruta_db_completa)
    cursor = conexion.cursor()
    try:
        if unidades is not None:
            cursor.execute(
                "UPDATE productos SET cantidad_unidades_en_stock=? WHERE lote=?",
                (
                    int(unidades),
                    lote,
                ),
            )
        if precio is not None:
            cursor.execute(
                "UPDATE productos SET precio=? WHERE lote=?",
                (
                    float(precio),
                    lote,
                ),
            )
        conexion.commit()
        return True

    except sqlite3.Error as e:
        print(f"Ocurrió un error al actualizar el lote: {e}")

    finally:
        if conexion:
            conexion.close()
