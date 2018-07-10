#!/usr/bin/env sh

mod_wsgi-express start-server \
    --server-root apache \
    --log-directory logs \
    --access-log \
    --startup-log \
    --rotate-logs \
    --host 127.0.0.1 \
    --port 5002 \
    --user www-data \
    --group www-data \
    crkva-svete-trojice.wsgi
