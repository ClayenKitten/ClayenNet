import { drizzle } from "drizzle-orm/bun-sql";
import { migrate } from "drizzle-orm/bun-sql/migrator";
import * as schema from "./schema";

export const createConnection = async () => {
    const db = drizzle("postgres://user:1234@localhost:5432/app", {
        casing: "snake_case",
        schema
    });

    await migrate(db, { migrationsFolder: "drizzle" });
    return db;
};
export type DB = Awaited<ReturnType<typeof createConnection>>;
