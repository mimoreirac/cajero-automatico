-- Tablas de la base de datos

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
    tipo_cuenta TEXT CHECK (tipo_cuenta IN ('ahorros', 'corriente')),
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
    tipo_transaccion TEXT CHECK (tipo_transaccion IN ('retiro', 'deposito', 'pago')),
    monto NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cuenta_id INT REFERENCES cuentas(cuenta_id)
);