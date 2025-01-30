-- Procedures


-- Ingresar catalogos

CREATE OR REPLACE PROCEDURE ingresar_catalogo(nombre VARCHAR(100))
LANGUAGE plpgsql
AS $$
BEGIN
	IF EXISTS (SELECT nombre_catalogo FROM catalogo WHERE nombre_catalogo = nombre) THEN
		RAISE EXCEPTION 'El catalogo % ya existe.', nombre;
	END IF;
	
	INSERT INTO catalogo(nombre_catalogo)
	VALUES(
		nombre
	);
END;
$$;

CREATE OR REPLACE PROCEDURE ingresar_item_catalogo(item VARCHAR(100), menu VARCHAR(100))
LANGUAGE plpgsql
AS $$
DECLARE
	raiz INTEGER;
BEGIN
	IF NOT EXISTS (SELECT nombre_catalogo FROM catalogo WHERE nombre_catalogo = menu) THEN
		RAISE EXCEPTION 'El catalogo % no existe.', menu;
	END IF;
	
	SELECT catalogo_id INTO raiz
	FROM catalogo
	WHERE nombre_catalogo = menu;
	
	INSERT INTO catalogo(nombre_item, raiz_id)
	VALUES(
		item,
		raiz
	);
END;
$$;


-- Añadir Clientes

CREATE OR REPLACE PROCEDURE añadir_cliente(nombres VARCHAR(100), apellidos VARCHAR(100), email VARCHAR(100), cedula CHAR(10)) 
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO clientes (nombres, apellidos, email, cedula)
    VALUES (nombres, apellidos, email, cedula);
END;
$$;

-- Crear cuenta

CREATE OR REPLACE PROCEDURE crear_cuenta(client_id INT, tipo_cuenta VARCHAR) 
LANGUAGE plpgsql
AS $$
DECLARE
    tipo INTEGER;
BEGIN
    SELECT catalogo_id INTO tipo FROM catalogo WHERE nombre_item = tipo_cuenta;
    INSERT INTO cuentas (client_id, tipo_cuenta)
    VALUES (client_id, tipo);
END;
$$;

-- Asignar Tarjeta

CREATE OR REPLACE PROCEDURE asignar_tarjeta(client_id INT, cuenta_id INT, pin CHAR(4)) 
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO tarjetas (client_id, cuenta_id, pin)
    VALUES (client_id, cuenta_id, pin);
END;
$$;

-- Cambio de pin

CREATE OR REPLACE PROCEDURE cambiar_pin(tarjeta_id INT, nuevo_pin CHAR(4)) 
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE tarjetas
    SET pin = nuevo_pin, pin_cambiado = TRUE
    WHERE tarjeta_id = tarjeta_id;
END;
$$;

-- Retiros

CREATE OR REPLACE PROCEDURE retiro(p_tarjeta_id INT, monto NUMERIC) 
LANGUAGE plpgsql
AS $$
DECLARE
    balance_actual NUMERIC;
    p_cuenta_id INT;
BEGIN
    SELECT cuenta_id INTO p_cuenta_id FROM tarjetas WHERE tarjeta_id = p_tarjeta_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'La tarjeta % no existe', p_tarjeta_id;
    END IF;
    -- Chequea el saldo de la cuenta
    SELECT balance INTO balance_actual FROM cuentas WHERE cuenta_id = p_cuenta_id;
    IF balance_actual < monto THEN
        RAISE EXCEPTION 'Fondos insuficientes';
    END IF;

    -- Chequea el monto máximo
    IF monto > 500 THEN
        RAISE EXCEPTION 'El monto máximo de retiro es 500.00';
    END IF;

    -- Retira y guarda la transacción
    UPDATE cuentas SET balance = balance - monto WHERE cuenta_id = p_cuenta_id;

    INSERT INTO transacciones (cuenta_id, tipo_transaccion, monto)
    VALUES (p_cuenta_id, 5, monto);
END;
$$;

-- Depósitos

CREATE OR REPLACE PROCEDURE deposito(p_cuenta_id INT, monto NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE cuentas 
    SET balance = balance + monto 
    WHERE cuenta_id = p_cuenta_id;
    
    INSERT INTO transacciones (cuenta_id, tipo_transaccion, monto)
    VALUES (p_cuenta_id, 6, monto);
END;
$$;


-- Pagos

CREATE OR REPLACE PROCEDURE pagos(cuenta_id INT, servicio TEXT, monto NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE cuentas SET balance = balance - monto WHERE cuenta_id = cuenta_id;

    INSERT INTO transacciones (cuenta_id, tipo_transaccion, monto)
    VALUES (cuenta_id, 7, monto);
END;
$$;

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