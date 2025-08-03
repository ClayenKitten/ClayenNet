# clayennet-node

Simple Wireguard node with configuration provided via HTTP API.

Supports [Wstunnel](https://github.com/erebe/wstunnel) for obfuscation.

## Environment variables

| Name         | Description                                | Default |
| ------------ | ------------------------------------------ | :-----: |
| API_PASSWORD | Password used to authenticate API requests |    -    |
| WG_INTERFACE | Wireguard interface name                   |   wg0   |

## Development

Use provided `dev.compose.yaml` to start development server inside docker.
Swagger will open at http://localhost:9501/docs.

Developing on your local machine is not recommended, as it may mess up local
network configuration.
