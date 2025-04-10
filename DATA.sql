-- Insertar usuarios
INSERT INTO usuarios (nombre, correo) VALUES
('Juan Pérez', 'juan@example.com'),
('María López', 'maria@example.com'),
('Carlos Gómez', 'carlos@example.com');

-- Insertar evento
INSERT INTO eventos (nombre, fecha, lugar) VALUES
('Concierto RockFest', '2025-06-15', 'Estadio Nacional');

-- Asumimos que este es el ID del evento recién insertado
-- Vamos a crear 10 asientos para este evento
INSERT INTO asientos (id_evento, numero_asiento) VALUES
(1, 'A1'), (1, 'A2'), (1, 'A3'), (1, 'A4'), (1, 'A5'),
(1, 'B1'), (1, 'B2'), (1, 'B3'), (1, 'B4'), (1, 'B5');

-- Reservas: 3 usuarios reservan distintos asientos
INSERT INTO reservas (id_usuario, id_asiento) VALUES
(1, 1),  -- Juan reserva A1
(2, 2),  -- María reserva A2
(3, 6);  -- Carlos reserva B1

-- Actualizar disponibilidad de los asientos reservados
UPDATE asientos SET disponible = FALSE WHERE id_asiento IN (1, 2, 6);

-- Bitácora: registrar las reservas y la actualización de asientos
INSERT INTO bitacora (tabla_afectada, accion, id_registro, usuario, descripcion) VALUES
('reservas', 'INSERT', 1, 'juan@example.com', 'Reserva del asiento A1 para evento 1'),
('reservas', 'INSERT', 2, 'maria@example.com', 'Reserva del asiento A2 para evento 1'),
('reservas', 'INSERT', 3, 'carlos@example.com', 'Reserva del asiento B1 para evento 1'),
('asientos', 'UPDATE', NULL, 'sistema', 'Se marcaron como no disponibles los asientos A1, A2, B1');
