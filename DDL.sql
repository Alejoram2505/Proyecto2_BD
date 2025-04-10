
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE eventos (
    id_evento SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    fecha DATE NOT NULL,
    lugar VARCHAR(100) NOT NULL
);

CREATE TABLE asientos (
    id_asiento SERIAL PRIMARY KEY,
    id_evento INT NOT NULL REFERENCES eventos(id_evento) ON DELETE CASCADE,
    numero_asiento VARCHAR(10) NOT NULL,
    disponible BOOLEAN DEFAULT TRUE,
    UNIQUE(id_evento, numero_asiento)
);

CREATE TABLE reservas (
    id_reserva SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    id_asiento INT NOT NULL REFERENCES asientos(id_asiento) ON DELETE CASCADE,
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_asiento) -- un asiento solo puede estar reservado una vez
);

-- Tabla para registrar acciones en el sistema
CREATE TABLE bitacora (
    id_log SERIAL PRIMARY KEY,
    tabla_afectada VARCHAR(50) NOT NULL,
    accion VARCHAR(20) NOT NULL, -- INSERT, UPDATE, DELETE
    id_registro INT,
    usuario TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT
);

