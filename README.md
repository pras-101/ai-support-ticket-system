# AI Support Ticket System

Phase 2 is a FastAPI service backed by local PostgreSQL. It provides customer registration, JWT login, customer-owned tickets, and the customer/agent/admin role model.

## 1. Configure PostgreSQL

The local database must already exist:

```sql
CREATE DATABASE ai_support;
```

Create the application configuration, then enter the role/password that work with `psql` on this Mac:

```bash
cp .env.example .env
```

For a local role named `admin`, the URL looks like:

```env
DATABASE_URL=postgresql+asyncpg://admin:YOUR_PASSWORD@localhost:5432/ai_support
```

Set a random `JWT_SECRET_KEY` in `.env` as well:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 2. Install and run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Open the API docs at http://127.0.0.1:8000/docs. `alembic upgrade head` creates the `users` table and adds `customer_id` to the existing `tickets` table.

## API

Create a ticket:

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"prastuti","password":"a-long-local-password"}'
```

Log in to receive a bearer token:

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"prastuti","password":"a-long-local-password"}'
```

Use that token to create and retrieve your tickets:

```bash
curl -X POST http://127.0.0.1:8000/tickets \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"title":"Payment failed","description":"My card was declined at checkout."}'

curl -H 'Authorization: Bearer YOUR_TOKEN' http://127.0.0.1:8000/tickets
```

## Roles

- Public registration creates **customer** accounts only.
- Customers can create tickets and see only their own tickets.
- **Agents** and **admins** can view all tickets.

Create agent or admin accounts locally—without adding an insecure public registration route—using:

```bash
python scripts/create_user.py --username support-agent --role agent
python scripts/create_user.py --username local-admin --role admin
```
