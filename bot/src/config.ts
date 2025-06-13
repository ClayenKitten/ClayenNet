export class WireguardConfig {
    public constructor(
        public id: string,
        public name: string,
        public address: string,
        public keys: {
            private: string,
            public: string,
        },
        public dns: string[],
        public peers: WireguardPeer[]
    ) {}

    /** Prints config into wg-easy format. */
    public print() {
        return [
            `# ${this.name}`,
            "[Interface]",
            `Address = ${this.address}`,
            `PrivateKey = ${this.keys.private}`,
            this.dns.length > 0 ? `DNS = ${this.dns.join(", ")}` : null,
            "",
            this.peers
                .map(peer =>
                    [
                        "[Peer]",
                        `Endpoint = ${peer.endpoint}`,
                        `PublicKey = ${peer.publicKey}`,
                        `AllowedIPs = ${peer.allowedIps.join(", ")}`
                    ].join("\n")
                )
                .join("\n\n")
        ]
            .filter(s => s !== null)
            .join("\n") + "\n";
    }
}

export type WireguardPeer = {
    endpoint: string;
    publicKey: string;
    allowedIps: string[];
};
