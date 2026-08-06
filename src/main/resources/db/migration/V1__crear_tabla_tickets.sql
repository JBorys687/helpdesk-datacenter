CREATE TABLE tickets (
    id BIGSERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion VARCHAR(2000) NOT NULL,
    categoria VARCHAR(20) NOT NULL CHECK (categoria IN ('RED', 'HARDWARE', 'SOFTWARE')),
    prioridad VARCHAR(20) NOT NULL CHECK (prioridad IN ('ALTA', 'MEDIA', 'BAJA')),
    estado VARCHAR(20) NOT NULL DEFAULT 'ABIERTO' CHECK (estado IN ('ABIERTO', 'EN_PROGRESO', 'CERRADO')),
    creado_en TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tickets_estado ON tickets (estado);
CREATE INDEX idx_tickets_prioridad ON tickets (prioridad);
