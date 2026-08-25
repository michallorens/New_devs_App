FROM postgres:15-alpine

COPY database/schema.sql /docker-entrypoint-initdb.d/1-schema.sql
COPY database/seed.sql /docker-entrypoint-initdb.d/2-seed.sql
