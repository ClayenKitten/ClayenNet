import { eq } from "drizzle-orm";
import { createConnection, type DB } from "./connection";
import * as schema from "./schema";
import type { Logger } from "winston";
import { WireguardConfig } from "../config";
import { entryNode } from "../nodes/entry-node";

export class Database {
    protected constructor(
        protected logger: Logger,
        protected connection: DB
    ) {}

    public static async create(logger: Logger): Promise<Database> {
        const connection = await createConnection();
        return new Database(logger, connection);
    }

    public async getUser(sender: SenderInfo): Promise<User | null> {
        const user = await this.updateUser(sender);
        if (!user) {
            if (!sender.tgUsername) return null;

            const isInvited = await this.popInvite(sender.tgUsername);
            if (!isInvited) return null;

            const user = await this.createNewUser(sender);
            this.logger.info("New user created", { sender });
            return user;
        }
        return user;
    }

    public async createNewUser(sender: SenderInfo): Promise<User> {
        return (
            await this.connection
                .insert(schema.users)
                .values({
                    firstName: sender.firstName,
                    lastName: sender.lastName,
                    tgUsername: sender.tgUsername,
                    tgUserId: sender.tgUserId,
                    exitNode: ""
                })
                .returning()
                .execute()
        )[0]!;
    }

    public async updateUser(sender: SenderInfo): Promise<User | null> {
        return (
            (
                await this.connection
                    .update(schema.users)
                    .set({
                        firstName: sender.firstName,
                        lastName: sender.lastName,
                        tgUsername: sender.tgUsername
                    })
                    .where(eq(schema.users.tgUserId, sender.tgUserId))
                    .returning()
                    .execute()
            )[0] ?? null
        );
    }

    public async popInvite(tgUsername: string): Promise<boolean> {
        const invite = await this.connection
            .delete(schema.invites)
            .where(eq(schema.invites.tgUsername, tgUsername))
            .returning()
            .execute();
        return invite.length > 0;
    }

    public async getConfigs(user?: User): Promise<WireguardConfig[]> {
        const configs = await this.connection.query.configs.findMany({
            where: user
                ? (configs, { eq }) => eq(configs.ownerId, user.id)
                : undefined
        });
        return configs.map(
            config =>
                new WireguardConfig(
                    config.id,
                    config.name,
                    config.address,
                    {
                        public: config.publicKey,
                        private: config.privateKey
                    },
                    ["10.96.0.1"],
                    [entryNode.asPeer()]
                )
        );
    }
}

export type User = (typeof schema.users)["$inferSelect"];
export type SenderInfo = {
    tgUserId: string;
    tgUsername: string | null;
    firstName: string;
    lastName: string | null;
};
