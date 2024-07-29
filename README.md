# demo-fastapi-async-sqlalchemy

Demo of set up for Web App Backend using FastAPI + Async SQLAlchemy.

## Commands

Start project:

```
docker compose up -d
```

Create migration file:

```
backend/scripts/autogenerate_migrations.sh "My migration"
```

Run migration:

```
backend/scripts/run_migrations.sh
```
