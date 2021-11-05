#!/usr/bin/env bash

LOGGING_LEVEL="${LOGGING_LEVEL:DEBUG}"

# directories for logs
mkdir -p /conference-management/data/logs/web/

# run web server
if [ "$FLASK_CONFIG" == "production" ]; then
  if [ "$DEPLOYED_INSTANCE" == "bleeding" ]; then
    gunicorn --access-logfile "/conference-management/data/logs/web/${HOSTNAME}_access.log" --error-logfile "/conference-management/data/logs/web/${HOSTNAME}_error.log" --log-level LOGGING_LEVEL --worker-class gevent --workers=3 --timeout 60 --bind 0.0.0.0:8081 manage:app
  else
    gunicorn --access-logfile "-" --error-logfile "-" --log-level LOGGING_LEVEL --worker-class gevent --workers=3 --timeout 60 --bind 0.0.0.0:8081 manage:app
  fi
else
    gunicorn --reload --access-logfile "-" --error-logfile "-" --log-level LOGGING_LEVEL --worker-class gevent --workers=3 --timeout 60 --bind 0.0.0.0:8081 manage:app
fi
