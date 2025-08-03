FROM python:3.13
WORKDIR /app

RUN apt-get update && apt-get install -y wireguard iproute2
RUN pipx install poetry==2.0.0

COPY ./pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir --upgrade -r /app/pyproject.toml
COPY . /app

RUN curl -L https://github.com/erebe/wstunnel/releases/download/v10.4.3/wstunnel_10.4.3_linux_amd64.tar.gz -o wstunnel.tar.gz && \
    tar -xzf wstunnel.tar.gz wstunnel && \
    rm wstunnel.tar.gz && \
    chmod +x wstunnel && \
    mv wstunnel /usr/local/bin

CMD ["fastapi", "run", "/app/src/main.py", "--host", "0.0.0.0", "--port", "3000"]
