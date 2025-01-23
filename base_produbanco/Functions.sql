-- Función para validar la cédula

CREATE OR REPLACE FUNCTION validate_cedula(cedula VARCHAR) 
RETURNS BOOLEAN AS $$
DECLARE
    sum_even INTEGER := 0;      -- Suma de dígitos en posiciones pares
    sum_odd INTEGER := 0;       -- Suma de dígitos en posiciones impares
    length INTEGER;             -- Longitud de la cédula
    i INTEGER;                  -- Variable para iteración
    digit INTEGER;              -- Dígito actual siendo procesado
    temp INTEGER;               -- Variable temporal para cálculos
    check_digit INTEGER;        -- Último dígito de la cédula (dígito verificador)
    calculated_check INTEGER;   -- Dígito verificador calculado
BEGIN
    -- Validar que la cédula tenga exactamente 10 dígitos numéricos
    IF cedula !~ '^\d{10}$' THEN
        RETURN FALSE;
    END IF;
    
    length := LENGTH(cedula);
    -- Obtener el último dígito (dígito verificador)
    check_digit := CAST(SUBSTRING(cedula, 10, 1) AS INTEGER);
    
    -- Iterar sobre los primeros 9 dígitos
    FOR i IN 1..9 LOOP
        -- Convertir el carácter actual a número
        digit := CAST(SUBSTRING(cedula, i, 1) AS INTEGER);
        
        -- Para posiciones pares (2,4,6,8): sumar el dígito directamente
        IF i % 2 = 0 THEN
            sum_even := sum_even + digit;
        -- Para posiciones impares (1,3,5,7,9):
        -- 1. Multiplicar por 2
        -- 2. Si el resultado es mayor a 9, restar 9
        ELSE
            temp := digit * 2;
            IF temp > 9 THEN
                temp := temp - 9;
            END IF;
            sum_odd := sum_odd + temp;
        END IF;
    END LOOP;
    
    -- Calcular dígito verificador
    -- 1. Sumar los resultados de posiciones pares e impares
    temp := sum_odd + sum_even;
    -- 2. Obtener siguiente decena y restar la suma total
    calculated_check := ((FLOOR(temp/10) + 1) * 10) - temp;
    
    -- Si el dígito verificador calculado es 10, debe ser 0
    IF calculated_check = 10 THEN
        calculated_check := 0;
    END IF;
    
    -- Retornar verdadero si el dígito verificador calculado coincide con el real
    RETURN calculated_check = check_digit;
END;
$$ LANGUAGE plpgsql;

-- Función trigger para validar la cédula antes de insertar o actualizar
CREATE OR REPLACE FUNCTION trigger_validate_cedula()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT validate_cedula(NEW.cedula) THEN
        RAISE EXCEPTION 'Cédula inválida: %', NEW.cedula;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear el trigger
DROP TRIGGER IF EXISTS validate_cedula_trigger ON clientes;
CREATE TRIGGER validate_cedula_trigger
    BEFORE INSERT OR UPDATE ON clientes
    FOR EACH ROW
    EXECUTE FUNCTION trigger_validate_cedula();

-- Agregar restricción a la tabla para validar cédulas existentes
ALTER TABLE clientes
ADD CONSTRAINT check_cedula
CHECK (validate_cedula(cedula));