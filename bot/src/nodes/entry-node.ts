import type { WireguardConfig, WireguardPeer } from "../config";
import type { Database } from "../db";

export class EntryNode {
    public readonly domain = "net.clayen.dev";
    public readonly port = 51280;
    public readonly publicKey = "cbkqd6JkvwqAqC/0d8mxq+QEn8q23q4nty8kbg4Djj0=";
    public readonly privateKey = "1234";

    public asPeer(): WireguardPeer {
        return {
            endpoint: `${this.domain}:${this.port}`,
            publicKey: this.publicKey,
            allowedIps: ["0.0.0.0/0"]
        };
    }

    public printConfig(peers: WireguardConfig[]): string {
        return [
            "[Interface]",
            "Address = 10.96.0.1/16",
            `PrivateKey = ${"privateKey"}`,
            "ListenPort = 51820",
            "",
            "PostUp = iptables -A FORWARD -i wg0 -o wg0 -j DROP",
            "PostUp = iptables -A FORWARD -i wg0 -j ACCEPT",
            "PostUp = iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE",
            "",
            "PostDown = iptables -D FORWARD -i wg0 -o wg0 -j DROP",
            "PostDown = iptables -D FORWARD -i wg0 -j ACCEPT",
            "PostDown = iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE",
            "",
            peers
                .map(c =>
                    [
                        `# ${c.name}`,
                        "[Peer]",
                        `PublicKey = ${c.keys.public}`,
                        `AllowedIPs = ${c.address}`
                    ].join("\n")
                )
                .join("\n\n")
        ].join("\n");
    }
}
export const entryNode = new EntryNode();
