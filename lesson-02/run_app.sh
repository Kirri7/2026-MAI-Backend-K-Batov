#! /usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

readonly WORKERS_CNT=4

function main()
{
  if ! gunicorn --workers ${WORKERS_CNT} myapp:app ; then
    echo "Failed to run gunicorn..."
    return 1
  fi
    # docker run -d --name mynginx -p 80:80 \
    #   -v $(pwd)/nginx/nginx.conf:/etc/nginx/nginx.conf \
    #   -v $(pwd)/nginx/public:/usr/share/nginx/html/public \
    #   nginx:latest
    docker restart mynginx
}

main $@
