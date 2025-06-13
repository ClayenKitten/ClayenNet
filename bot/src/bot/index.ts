import type { Logger } from "winston";
import type { Database, SenderInfo, User } from "../db";
import { Context, Bot as Grammy, InputFile } from "grammy";

export class TelegramBot {
    protected constructor(
        protected logger: Logger,
        protected db: Database,
        protected grammy: Grammy<MyContext>
    ) {}

    public static async create(logger: Logger, db: Database) {
        const grammy = new Grammy<MyContext>(process.env.TELEGRAM_BOT_TOKEN!);

        await grammy.api.setMyCommands([
            { command: "/info", description: "Информация о VPN" },
            { command: "/switch", description: "Сменить выходную точку" }
        ]);

        grammy.chatType("private", async (ctx, next) => {
            const sender: SenderInfo = {
                firstName: ctx.from.first_name,
                lastName: ctx.from.last_name ?? null,
                tgUserId: ctx.from.id.toFixed(0),
                tgUsername: ctx.from.username ?? null
            };
            const user = await db.getUser(sender);
            if (!user) {
                await ctx.reply("Вы не авторизованы.");
                return;
            }
            ctx.user = user;
            await next();
        });

        grammy.chatType("private").command(["start", "info"], async ctx => {
            const configs = await db.getConfigs(ctx.user);
            await ctx.reply("Привет!", {
                reply_markup: {
                    inline_keyboard: [
                        configs.map(c => ({
                            text: c.name,
                            callback_data: `cfg-${c.id}`
                        }))
                    ]
                }
            });
        });

        grammy.chatType("private").callbackQuery(/^cfg-.+$/, async ctx => {
            const configs = await db.getConfigs(ctx.user);
            
            const targetId = ctx.callbackQuery.data.replace("cfg-", "");
            const config = configs.find(c => c.id === targetId);
            if (!config) {
                await ctx.answerCallbackQuery("Неизвестный конфиг");
                return;
            }

            const filename = `${config.name}.conf`;
            const content = config.print();
            const file = new InputFile(Buffer.from(content), filename);

            await ctx.answerCallbackQuery();
            await ctx.replyWithDocument(file);
        });

        grammy.chatType("private").command("switch", async ctx => {
            await ctx.reply("Переключение");
        });

        return new TelegramBot(logger, db, grammy);
    }

    public async start() {
        await this.grammy.start();
    }
}

type MyContext = Context & {
    user: User;
};
