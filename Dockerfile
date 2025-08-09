FROM python:3.13-slim

# Setup Poetry
ARG POETRY_VERSION=2.1.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install "poetry==${POETRY_VERSION}"

# WireGuard and network management tools
RUN apt-get update && apt-get install -y wireguard iproute2 iptables curl

# wstunnel
RUN curl -L https://github.com/erebe/wstunnel/releases/download/v10.4.3/wstunnel_10.4.3_linux_amd64.tar.gz -o wstunnel.tar.gz && \
    tar -xzf wstunnel.tar.gz wstunnel && \
    rm wstunnel.tar.gz && \
    chmod +x wstunnel && \
    mv wstunnel /usr/local/bin

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root

COPY ./alembic.ini /app/alembic.ini
COPY ./alembic /app/alembic
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./src /app/src

ENTRYPOINT ["/app/entrypoint.sh"]
