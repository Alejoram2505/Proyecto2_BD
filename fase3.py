import psycopg2
import threading

# Datos de mi bd (para probarlo cada uno tiene que poner su info)
BD = {
    "dbname": "Proyecto2",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": 5432
}

ASIENTO = 3  # Cambiar este id si se quiere probar con otro asiento
EVENTO = 1   
AISLAMIENTO = "READ COMMITTED"  # Cambiar a SERIALIZABLE, READ COMMITTED o REPEATABLE READ para probarlos 

exitos = 0
fallos = 0
lock = threading.Lock()

# Para hacer la reserva
def reservar(nombre_usuario, id_usuario):
    global exitos, fallos
    conn = None
    try:
        conn = psycopg2.connect(**BD)
        conn.set_session(isolation_level=AISLAMIENTO, autocommit=False)  
        cursor = conn.cursor()

        cursor.execute("SELECT id_asiento FROM asientos WHERE id_asiento = %s AND disponible = TRUE FOR UPDATE;", (ASIENTO,))
        asiento_bloqueado = cursor.fetchone()

        if not asiento_bloqueado:
            print(f"{nombre_usuario}: Asiento {ASIENTO} ya está ocupado.")
            conn.rollback()
            with lock:
                fallos += 1
            return

        cursor.execute(
            "INSERT INTO reservas (id_usuario, id_asiento) VALUES (%s, %s) RETURNING id_reserva;",
            (id_usuario, ASIENTO)
        )
        id_reserva = cursor.fetchone()[0]

        cursor.execute(
            "UPDATE asientos SET disponible = FALSE WHERE id_asiento = %s;", 
            (ASIENTO,)
        )

        cursor.execute(
            "INSERT INTO bitacora (tabla_afectada, accion, id_registro, usuario, descripcion) VALUES (%s, %s, %s, %s, %s);",
            ('reservas', 'INSERT', id_reserva, nombre_usuario, f'Reserva del asiento {ASIENTO}')
        )

        conn.commit()
        print(f"{nombre_usuario} reservo el asiento :) {ASIENTO}.")
        with lock:
            exitos += 1

    except Exception as e:
        print(f"Error en {nombre_usuario}: {type(e).__name__} - {e}")
        if conn:
            conn.rollback()
        with lock:
            fallos += 1
    finally:
        if conn:
            conn.close()

# Traer usuarios desde la bd
def obtener_usuarios():
    conn = psycopg2.connect(**BD)
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nombre FROM usuarios;")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def simulacion(n_usuarios):
    usuarios = obtener_usuarios()
    hilos = []
    for i in range(n_usuarios):
        nombre = usuarios[i % len(usuarios)][1] 
        id_usuario = usuarios[i % len(usuarios)][0] 
        t = threading.Thread(target=reservar, args=(nombre, id_usuario))
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    print(f"Usuarios concurrentes: {n_usuarios}")
    print(f"Nivel de aislamiento: {AISLAMIENTO}")
    print(f"Reservas realizadas: {exitos}")
    print(f"Reservas fallidas: {fallos}")

if __name__ == "__main__":
    op = [5, 10, 20, 30]
    while True:
        try:
            n = int(input("Elige el número de usuarios (5, 10, 20, 30): "))
            if n in op:
                break
            else:
                print("Error, selecciona un número válido.")
        except ValueError:
            print("Por favor ingresa un número válido.")
    
    simulacion(n)
