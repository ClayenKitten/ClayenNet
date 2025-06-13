# ClayenNet

Private VPN with Telegram bot interface.

## Network

```
Client   Client   Client
  |        |        |
  +--------|--------+
           |
           |    WireGuard
           ▼
    Domestic server
           |
           |    WireGuard over WSTunnel
           |
           ▼
    Foreign server
           |
           |
           ▼
        Internet
```
