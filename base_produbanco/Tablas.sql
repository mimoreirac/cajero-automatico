-- Tablas de la base de datos

-- Catálogo
CREATE TABLE catalogo (
    catalogo_id SERIAL PRIMARY KEY,
    nombre_catalogo VARCHAR(100) UNIQUE, 
    nombre_item VARCHAR(100) UNIQUE, 
    raiz_id INT REFERENCES catalogo(catalogo_id) DEFAULT NULL
);

-- Clientes
CREATE TABLE clientes (
    client_id SERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    cedula CHAR(10) UNIQUE NOT NULL
);

-- Cuentas
CREATE TABLE cuentas (
    cuenta_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clientes(client_id),
    tipo_cuenta INT REFERENCES catalogo(catalogo_id),
    balance NUMERIC(12, 2) DEFAULT 0 CHECK (balance >= 0)
);

-- Tarjetas
CREATE TABLE tarjetas (
    tarjeta_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clientes(client_id),
    cuenta_id INT REFERENCES cuentas(cuenta_id),
    pin CHAR(4) NOT NULL,
    pin_cambiado BOOLEAN DEFAULT FALSE -- Es posible que esto eliminemos, veamos que tan difícil es la cosa.
);

-- Transacciones
CREATE TABLE transacciones (
    transaccion_id SERIAL PRIMARY KEY,
    cuenta_id INT REFERENCES cuentas(cuenta_id),
    tipo_transaccion INT REFERENCES catalogo(catalogo_id),
    monto NUMERIC(12, 2) NOT NULL CHECK (monto > 0),
    hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);