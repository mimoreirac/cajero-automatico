-- First, create the sequence for account numbers
CREATE SEQUENCE cuentas_account_number_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO CYCLE;

-- Add the new account_number column
ALTER TABLE cuentas
ADD COLUMN numero_cuenta CHAR(10) UNIQUE;

-- Update existing rows with account numbers
UPDATE cuentas
SET numero_cuenta = '01' || LPAD(nextval('cuentas_account_number_seq')::TEXT, 8, '0');

-- Make the column NOT NULL after populating existing rows
ALTER TABLE cuentas
ALTER COLUMN numero_cuenta SET NOT NULL;

-- Add the DEFAULT constraint for new rows
ALTER TABLE cuentas
ALTER COLUMN numero_cuenta 
SET DEFAULT '01' || LPAD(nextval('cuentas_account_number_seq')::TEXT, 8, '0');