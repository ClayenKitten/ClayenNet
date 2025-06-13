FROM debian:12

RUN apt-get update && apt-get install -y wireguard iproute2

COPY --chown=744 ./entrypoint.sh /app/entrypoint.sh
ENTRYPOINT [ "sh", "/app/entrypoint.sh" ]
