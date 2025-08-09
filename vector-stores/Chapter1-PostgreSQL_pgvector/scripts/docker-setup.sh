#!/usr/bin/env bash

# Pull the official Docker image for PostgreSQL with pgvector extension preinstalled
docker pull ankane/pgvector

# Run the container in detached mode with the name 'pgvector-quick'
# Set the POSTGRES_PASSWORD to 'pgpass' and expose port 5432
docker run -d --name pgvector-quick \
  -e POSTGRES_PASSWORD=pgpass \
  -p 5432:5432 \
  ankane/pgvector



