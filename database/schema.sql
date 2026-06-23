-- database/schema.sql

-- Creamos el espacio seguro para tu plataforma si no existe
CREATE DATABASE IF NOT EXISTS db_diviertete_gratis;
USE db_diviertete_gratis;

-- 1. TABLA MAESTRA DE CATEGORÍAS (Para evitar duplicar texto en memoria)
CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

-- 2. TABLA MAESTRA DE DISTRITOS (Optimización geográfica ligera)
CREATE TABLE distritos (
    id_distrito INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

-- 3. TABLA PRINCIPAL DE EVENTOS (Estructurada para alto rendimiento)
CREATE TABLE eventos (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    id_categoria INT,
    id_distrito INT,
    fecha_evento DATE NOT NULL,
    hora_evento TIME,
    lugar_direccion VARCHAR(255) NOT NULL,
    imagen_url VARCHAR(255),
    fuente_oficial VARCHAR(255),
    estado VARCHAR(20) DEFAULT 'activo', -- 'activos' o 'finalizados' (Para no destruir tu SEO)
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Relaciones estrictas para mantener los datos limpios
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    FOREIGN KEY (id_distrito) REFERENCES distritos(id_distrito)
);

-- ⚡ EL ESCUDO DE ALTO TRÁFICO: Índice compuesto para búsquedas instantáneas
-- Esto evita que Azure te cobre de más porque MySQL encuentra todo en milisegundos.
CREATE INDEX idx_busqueda_rapida ON eventos (id_distrito, id_categoria, fecha_evento);

-- 📌 Inyección de datos iniciales para que tus filtros de la web tengan opciones
INSERT IGNORE INTO categorias (nombre) VALUES ('Cine'), ('Bailable'), ('Teatro'), ('Niños'), ('Ferias');
INSERT IGNORE INTO distritos (nombre) VALUES ('Cercado de Lima'), ('Miraflores'), ('Los Olivos'), ('San Miguel');