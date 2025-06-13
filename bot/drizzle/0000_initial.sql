CREATE TABLE "configs" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"name" text NOT NULL,
	"owner_id" uuid,
	"address" "inet" NOT NULL,
	"private_key" text NOT NULL
);
--> statement-breakpoint
CREATE TABLE "invites" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"tg_username" text NOT NULL,
	CONSTRAINT "invites_tgUsername_unique" UNIQUE("tg_username")
);
--> statement-breakpoint
CREATE TABLE "users" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"first_name" text NOT NULL,
	"last_name" text,
	"tg_user_id" text NOT NULL,
	"tg_username" text,
	"exit_node" text NOT NULL,
	CONSTRAINT "users_tgUserId_unique" UNIQUE("tg_user_id"),
	CONSTRAINT "users_tgUsername_unique" UNIQUE("tg_username")
);
--> statement-breakpoint
ALTER TABLE "configs" ADD CONSTRAINT "configs_owner_id_users_id_fk" FOREIGN KEY ("owner_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;