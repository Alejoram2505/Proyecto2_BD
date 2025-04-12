import psycopg2
import threading
import time

# Datos de mi bd (para probarlo cada uno tiene que poner su info)
BD = {
    "dbname": "Proyecto2",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": 5432
}

ASIENTO = 2
#AISLAMIENTO = "READ COMMITTED"  

AISLAMIENTO = "SERIALIZABLE"
#AISLAMIENTO = "REPEATABLE READ"

exitos = 0
fallos = 0
lock = threading.Lock()

def reservar(nombre_usuario, id_usuario):
    global exitos, fallos
    conn = None
    try:
        conn = psycopg2.connect(**BD)
        conn.set_session(isolation_level=AISLAMIENTO, autocommit=False)
        cursor = conn.cursor()

        # Bloqueo del asiento
        cursor.execute("SELECT disponible FROM asientos WHERE id_asiento = %s FOR UPDATE;", (ASIENTO,))
        estado = cursor.fetchone()

        if not estado:
            print(f"{nombre_usuario}: Asiento no existe.")
            conn.rollback()
            with lock:
                fallos += 1
            return

        if not estado[0]:
            print(f"{nombre_usuario}: Asiento ya ocupado.")
            conn.rollback()
            with lock:
                fallos += 1
            return

        # Actualizar disponibilidad
        cursor.execute("UPDATE asientos SET disponible = FALSE WHERE id_asiento = %s;", (ASIENTO,))

        # Insertar reserva
        cursor.execute("INSERT INTO reservas (id_usuario, id_asiento) VALUES (%s, %s) RETURNING id_reserva;", (id_usuario, ASIENTO))
        id_reserva = cursor.fetchone()[0]

        # Insertar bitacora
        cursor.execute("INSERT INTO bitacora (tabla_afectada, accion, id_registro, usuario, descripcion) VALUES (%s, %s, %s, %s, %s);", 
            ('reservas', 'INSERT', id_reserva, nombre_usuario, f'Reserva del asiento {ASIENTO}'))

        conn.commit()
        print(f"{nombre_usuario} reservó el asiento correctamente.")
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
    tiempo_inicio = time.time()
    

    for i in range(n_usuarios):
        nombre = usuarios[i % len(usuarios)][1]
        id_usuario = usuarios[i % len(usuarios)][0]
        t = threading.Thread(target=reservar, args=(nombre, id_usuario))
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()
        tiempo_fin = time.time()  # Marcar fin de la simulación

    tiempo_promedio = (tiempo_fin - tiempo_inicio) * 1000 

    print(f"Usuarios concurrentes: {n_usuarios}")
    print(f"Nivel de aislamiento: {AISLAMIENTO}")
    print(f"Reservas exitosas: {exitos}")
    print(f"Reservas fallidas: {fallos}")
    print(f"Tiempo promedio de ejecución: {tiempo_promedio:.2f} ms")


if __name__ == "__main__":
    op = [5, 10, 20, 30]
    while True:
        try:
            n = int(input("Elige número de usuarios (5, 10, 20, 30): "))
            if n in op:
                break
            else:
                print("Número inválido")
        except ValueError:
            print("Por favor ingresa un número válido.")

    simulacion(n)
