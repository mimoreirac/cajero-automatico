-- Procedures

-- Añadir Clientes

CREATE OR REPLACE FUNCTION añadir_cliente(nombres VARCHAR(100), apellidos VARCHAR(100), email VARCHAR(100), cedula CHAR(10)) 
RETURNS VOID AS $$
BEGIN
    INSERT INTO clientes (nombres, apellidos, email, cedula)
    VALUES (nombres, apellidos, email, cedula);
END;
$$ LANGUAGE plpgsql;

-- Crear cuenta

CREATE OR REPLACE FUNCTION crear_cuenta(client_id INT, tipo_cuenta TEXT) 
RETURNS VOID AS $$
BEGIN
    INSERT INTO cuentas (client_id, tipo_cuenta)
    VALUES (client_id, tipo_cuenta);
END;
$$ LANGUAGE plpgsql;

-- Asignar Tarjeta

CREATE OR REPLACE FUNCTION asignar_tarjeta(client_id INT, cuenta_id INT, pin CHAR(4)) 
RETURNS VOID AS $$
BEGIN
    INSERT INTO tarjetas (client_id, cuenta_id, pin)
    VALUES (client_id, cuenta_id, pin);
END;
$$ LANGUAGE plpgsql;

-- Cambio de pin

CREATE OR REPLACE FUNCTION cambiar_pin(tarjeta_id INT, nuevo_pin CHAR(4)) 
RETURNS VOID AS $$
BEGIN
    UPDATE tarjetas
    SET pin = nuevo_pin, pin_cambiado = TRUE
    WHERE tarjeta_id = tarjeta_id;
END;
$$ LANGUAGE plpgsql;

-- Retiros

CREATE OR REPLACE FUNCTION retiro(tarjeta_id INT, monto NUMERIC) 
RETURNS VOID AS $$
DECLARE
    balance_actual NUMERIC;
BEGIN
    -- Chequea el saldo de la cuenta
    SELECT balance INTO balance_actual FROM cuentas WHERE cuenta_id = cuenta_id;
    IF balance_actual < monto THEN
        RAISE EXCEPTION 'Fondos insuficientes';
    END IF;

    -- Chequea el monto máximo
    IF monto > 500 THEN
        RAISE EXCEPTION 'El monto máximo de retiro es 500.00';
    END IF;

    -- Retira y guarda la transacción
    UPDATE cuentas SET balance = balance - monto WHERE cuenta_id = cuenta_id;

    INSERT INTO transacciones (cuenta_id, tipo_transaccion, monto)
    VALUES (cuenta_id, 'retiro', monto);
END;
$$ LANGUAGE plpgsql;

-- Depósitos

CREATE OR REPLACE FUNCTION deposito(cuenta_id INT, monto NUMERIC) 
RETURNS VOID AS $$
BEGIN
    UPDATE cuentas SET balance = balance + monto WHERE cuenta_id = cuenta_id;

    INSERT INTO transacciones (cuenta_id, tipo_transaccion, monto)
    VALUES (cuenta_id, 'deposito', monto);
END;
$$ LANGUAGE plpgsql;

-- Inicio de sesión

CREATE OR REPLACE FUNCTION login(tarjeta_id INT, pin_ingresado TEXT) 
RETURNS BOOLEAN AS $$
DECLARE
    pin_valido BOOLEAN;
    pin_cambiado BOOLEAN;
BEGIN
    -- Chequea que la tarjeta exista y el pin sea válido
    SELECT 
        CASE 
            WHEN pin = pin_ingresado THEN TRUE 
            ELSE FALSE 
        END,
        pin_cambiado
    INTO pin_valido, pin_cambiado
    FROM tarjetas
    WHERE tarjeta_id = tarjeta_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'No se encuentra la tarjeta';
    END IF;

    -- Si el pin es incorrecto, mostrar un error
    IF NOT pin_valido THEN
        RAISE EXCEPTION 'El PIN ingresado es incorrecto';
    END IF;

    -- Si el pin no ha sido actualizado, llamar al procedure para cambiar pin
    IF NOT pin_cambiado THEN
        PERFORM cambiar_pin(tarjeta_id, 'NUEVO PIN AQUI'); -- Hay que reemplazar este campo con el pin ingresado por el usuario
        RETURN FALSE; -- Para que regrese FALSE si el pin necesitaba ser cambiado
    END IF;

    -- Si todo es válido, regresa TRUE mostrando que el login es correcto 
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;