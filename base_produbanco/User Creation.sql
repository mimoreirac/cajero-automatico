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