-- tabla de usuarios
CREATE TABLE usuarios (
    Id_usuario SERIAL PRIMARY KEY,
    Nombres VARCHAR(100) NOT NULL,
    Apellidos VARCHAR(100) NOT NULL,
    Direccion VARCHAR(200),
    Correo VARCHAR(100),
    Numero_cedula VARCHAR(10) NOT NULL UNIQUE,
    Numero_telefono VARCHAR(15)
);

-- tabla de cuentas bancarias
CREATE TABLE cuentas_bancarias (
    Id_cuenta SERIAL PRIMARY KEY,
    Numero_cuenta VARCHAR(20) NOT NULL UNIQUE,
    Propietario INT NOT NULL,
    Tipo_cuenta VARCHAR(50) NOT NULL,
    Saldo DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Propietario) REFERENCES usuarios(Id_usuario)
);

-- tabla de tarjetas
CREATE TABLE tarjetas (
    Id_tarjeta SERIAL PRIMARY KEY,
    Numero_tarjeta VARCHAR(20) NOT NULL UNIQUE,
    Cuenta_id INT NOT NULL,
    Fecha_emision DATE NOT NULL,
    Fecha_caducidad DATE NOT NULL,
    Estado_tarjeta VARCHAR(50) NOT NULL,
    PIN CHAR(4) NOT NULL,
    FOREIGN KEY (Cuenta_id) REFERENCES cuentas_bancarias(Id_cuenta)
);

-- Crear tabla de transacciones
CREATE TABLE transacciones (
    Id_transaccion SERIAL PRIMARY KEY,
    Tipo_transaccion VARCHAR(50) NOT NULL,
    Monto DECIMAL(10, 2),
    Fecha_hora TIMESTAMP NOT NULL,
    Cuenta_emision INT NOT NULL,
    Cuenta_destino INT,
    FOREIGN KEY (Cuenta_emision) REFERENCES cuentas_bancarias(Id_cuenta),
    FOREIGN KEY (Cuenta_destino) REFERENCES cuentas_bancarias(Id_cuenta)
);
