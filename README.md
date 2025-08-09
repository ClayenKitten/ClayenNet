# ClayenNet

Private VPN with Telegram bot interface.

This package starts a WireGuard and WSTunnel servers, and WSTunnel server forwards all incoming traffic to the WireGuard interface.

Clients don't need to be aware of the wstunnel - they may connect to the proxy
server with wstunnel client running.

```
Client   Client   Client
  |        |        |
  +--------|--------+
           |
           |    WireGuard
           ▼
      Proxy server
           |
           |    WireGuard over WSTunnel
           ▼
       Main server
           |
           |    Unmasked traffic
           ▼
        Internet
```

## Proxy server configuration

Proxy server is expected to run a wstunnel client in the following way:
```shell
wstunnel client -L udp://0.0.0.0:${PUBLIC_PORT}$:localhost:9000 -P ${WS_PASSWORD} wss://myserver.net:${WS_PORT}
```

## Environment variables

| Name                    | Description                                                                                     | Default |
| ----------------------- | ----------------------------------------------------------------------------------------------- | :-----: |
| **Telegram**            |                                                                                                 |         |
| TELEGRAM_ADMIN_USERNAME | Telegram username of admin user                                                                 |    -    |
| TELEGRAM_BOT_TOKEN      | Telegram bot token                                                                              |    -    |
| **Public connection**   |                                                                                                 |         |
| PUBLIC_HOST             | Externally accessible domain or IP address, should be host of the proxy if proxy server is used |    -    |
| PUBLIC_PORT             | As PUBLIC_HOST, but for tcp/udp port                                                            |    -    |
| **WireGuard**           |                                                                                                 |         |
| WG_ADDRESS              | WireGuard server internal address                                                               |    -    |
| WG_PRIVATE_KEY          | WireGuard server private key                                                                    |    -    |
| WG_PUBLIC_KEY           | WireGuard server public key                                                                     |    -    |
| **WebSocket Tunnel**    |                                                                                                 |         |
| WS_PORT                 | WebSocket server port                                                                           |  8443   |
| WS_PASSWORD             | WebSocket tunnel password                                                                       |    -    |
| **Database**            |                                                                                                 |         |
| POSTGRES_HOST           | Postgres host                                                                                   |    -    |
| POSTGRES_DB             | Postgres database                                                                               |    -    |
| POSTGRES_USER           | Postgres user                                                                                   |    -    |
| POSTGRES_PASSWORD       | Postgres password                                                                               |    -    |
