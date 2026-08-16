# AI Support local database

This stack runs PostgreSQL and pgAdmin locally with Docker Compose.

## Start

1. Create your local configuration:

   ```bash
   cp .env.example .env
   ```

2. Start the services:

   ```bash
   docker compose up -d
   ```

3. Open pgAdmin at [http://localhost:5050](http://localhost:5050) and sign in with the values in `.env`.

## Database connection

Use this connection string in the app:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_support
```

To add the server in pgAdmin, use:

- Host name/address: `postgres`
- Port: `5432`
- Maintenance database: `ai_support`
- Username: `postgres`
- Password: `postgres`

`postgres` is the Docker service name, so it works from pgAdmin. From your Mac, use `localhost` instead.

## Useful commands

```bash
# Follow database logs
docker compose logs -f postgres

# Open a PostgreSQL shell
docker compose exec postgres psql -U postgres -d ai_support

# Stop containers while retaining database data
docker compose down

# Stop containers and remove all local database data
docker compose down -v
```

Change the default passwords in `.env` if this machine is shared or the ports are exposed beyond your computer.
