import * as d from "drizzle-orm/pg-core";

export const users = d.pgTable("users", {
    id: d.uuid().primaryKey().defaultRandom(),
    firstName: d.text().notNull(),
    lastName: d.text(),
    tgUserId: d.text().unique().notNull(),
    tgUsername: d.text().unique(),
    exitNode: d.text().notNull()
});

export const configs = d.pgTable("configs", {
    id: d.uuid().primaryKey().defaultRandom(),
    name: d.text().notNull(),
    ownerId: d.uuid().references(() => users.id),
    address: d.inet().notNull(),
    privateKey: d.text().notNull(),
    publicKey: d.text().notNull()
});

export const invites = d.pgTable("invites", {
    id: d.uuid().primaryKey().defaultRandom(),
    tgUsername: d.text().unique().notNull()
});
