#! /usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

readonly WORKERS_CNT=4

function main()
{
    gunicorn --workers ${WORKERS_CNT} myapp:app -b 0.0.0.0:8090 &

    cd ../project
    gunicorn --workers ${WORKERS_CNT} project.wsgi:application -b 0.0.0.0:8091 &
    echo "Both Gunicorn instances are starting..."
    
    # docker run -d --name mynginx -p 80:80 \
    #   -v $(pwd)/nginx/nginx.conf:/etc/nginx/nginx.conf \
    #   -v $(pwd)/nginx/public:/usr/share/nginx/html/public \
    #   nginx:latest
    docker restart mynginx
    # docker attach mynginx
}

main $@
