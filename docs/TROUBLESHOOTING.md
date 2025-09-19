# Troubleshooting

## Temporal UI cannot connect
- Ensure `TEMporal_ADDRESS` resolves to the frontend private host and port 7233.
- Check network connectivity within Render private services.

## Database connection pool exhausted
- Increase PgBouncer `default_pool_size` and Postgres `max_connections`.
- Reduce worker concurrency temporarily.

## Elasticsearch red/yellow status
- Verify disk is attached and not full.
- Set `discovery.type=single-node` and right-size JVM heap via `ES_JAVA_OPTS`.

## Schema or namespace setup fails
- Re-run admin-tools job; commands are idempotent.
- Check credentials in `postgres-auth` env group.
