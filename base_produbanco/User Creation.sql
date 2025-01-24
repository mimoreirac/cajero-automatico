CREATE ROLE banco WITH LOGIN PASSWORD 'administrador';
GRANT ALL PRIVILEGES ON DATABASE produbanco to banco;

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO banco;

-- Grant ability to create tables
GRANT CREATE ON SCHEMA public TO banco;

-- Grant all privileges on all tables in public schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO banco;

-- Grant all privileges on future tables too
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT ALL PRIVILEGES ON TABLES TO banco;

-- Otros permisos

GRANT USAGE, SELECT ON SEQUENCE clientes_client_id_seq TO banco;
GRANT UPDATE ON SEQUENCE clientes_client_id_seq TO banco;

GRANT USAGE, SELECT ON SEQUENCE catalogo_catalogo_id_seq TO banco;
GRANT UPDATE ON SEQUENCE catalogo_catalogo_id_seq TO banco;

GRANT USAGE, SELECT ON SEQUENCE cuentas_cuenta_id_seq TO banco;
GRANT UPDATE ON SEQUENCE cuentas_cuenta_id_seq TO banco;

GRANT USAGE, SELECT ON SEQUENCE tarjetas_tarjeta_id_seq TO banco;
GRANT UPDATE ON SEQUENCE tarjetas_tarjeta_id_seq TO banco;

GRANT USAGE, SELECT ON SEQUENCE transacciones_transaccion_id_seq TO banco;
GRANT UPDATE ON SEQUENCE transacciones_transaccion_id_seq TO banco;


-- Para mejor rendimiento de django

ALTER ROLE banco SET client_encoding = 'UTF8';

ALTER ROLE banco SET default_transaction_isolation = 'read committed';

ALTER ROLE banco SET timezone = 'UTC';
