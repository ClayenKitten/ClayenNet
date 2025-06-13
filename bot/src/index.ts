import winston, { createLogger } from "winston";
import { Database } from "./db";
import { TelegramBot } from "./bot";
import { getEntryNodeConfig } from "./nodes/entry-node";

const logger = createLogger({
    levels: winston.config.cli.levels,
    transports: new winston.transports.Console()
});
const db = await Database.create(logger);
const bot = await TelegramBot.create(logger, db);

await bot.start();
