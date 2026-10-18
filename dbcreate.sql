CREATE TABLE IF NOT EXISTS "Users" (
	"id" INTEGER NOT NULL,
	"nickname" VARCHAR NOT NULL,
	"email" VARCHAR NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "subscriptions" (
	"id" INTEGER NOT NULL,
	"user_id" INTEGER NOT NULL,
	"plan_type" VARCHAR NOT NULL,
	"monthly_limit" INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("user_id") REFERENCES "Users"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "billing" (
	"id" INTEGER NOT NULL,
	"user_id" INTEGER NOT NULL,
	"amount" INTEGER NOT NULL,
	"transaction_type" VARCHAR NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("user_id") REFERENCES "Users"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "api_keys" (
	"id" INTEGER NOT NULL,
	"user_id" INTEGER NOT NULL,
	"key_value" VARCHAR NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("user_id") REFERENCES "Users"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "categories" (
	"id" INTEGER NOT NULL,
	"name" VARCHAR NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "models" (
	"id" INTEGER NOT NULL,
	"category_id" INTEGER NOT NULL,
	"name" VARCHAR NOT NULL,
	"param_count" VARCHAR NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("category_id") REFERENCES "categories"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "chats" (
	"id" INTEGER NOT NULL,
	"user_id" INTEGER NOT NULL,
	"model_id" INTEGER NOT NULL,
	"title" VARCHAR NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("user_id") REFERENCES "Users"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("model_id") REFERENCES "models"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "prompts" (
	"id" INTEGER NOT NULL,
	"user_id" INTEGER NOT NULL,
	"title" VARCHAR NOT NULL,
	"body" TEXT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("user_id") REFERENCES "Users"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "datasets" (
	"id" INTEGER NOT NULL,
	"name" VARCHAR NOT NULL,
	"file_size" INTEGER NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "fine_tuning_jobs" (
	"id" INTEGER NOT NULL,
	"model_id" INTEGER NOT NULL,
	"dataset_id" INTEGER NOT NULL,
	"status" VARCHAR NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("model_id") REFERENCES "models"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("dataset_id") REFERENCES "datasets"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

INSERT OR IGNORE INTO "Users" (id, nickname, email) VALUES
	(1, 'Aleksandrs', 'aleksandrs@example.com'),
	(2, 'Teimurs', 'teimurs@example.com'),
	(3, 'Kirills', 'kirills@example.com'),
	(4, 'Ričards', 'richards@example.com'),
	(5, 'Helvijs', 'helvijs@example.com');

INSERT OR IGNORE INTO "categories" (id, name) VALUES
	(1, 'Text generation'),
	(2, 'Vision'),
	(3, 'Speech'),
	(4, 'Embeddings');

INSERT OR IGNORE INTO "models" (id, category_id, name, param_count) VALUES
	(1, 1, 'Hy-4-preview', '770B'),
	(2, 2, 'GLM-5.3 Flash','320B'),
	(3, 3, 'Whisper-large-v3', '1.55B'),
	(4, 4, 'EmbeddingGemma 2', '740M');

INSERT OR IGNORE INTO "datasets" (id, name, file_size) VALUES
	(1, 'web_text_corpus', 52428800),
	(2, 'image_caption_pairs', 31457280),
	(3, 'voice_samples_lat', 10485760),
	(4, 'embedding_pairs_lat', 8388608);

INSERT OR IGNORE INTO "fine_tuning_jobs" (id, model_id, dataset_id, status) VALUES
	(1, 1, 1, 'completed'),
	(2, 2, 2, 'running'),
	(3, 3, 3, 'failed'),
	(4, 4, 4, 'queued');

INSERT OR IGNORE INTO "subscriptions" (id, user_id, plan_type, monthly_limit) VALUES
	(1, 1, 'premium', 1000),
	(2, 2, 'free', 100),
	(3, 3, 'standard', 500),
	(4, 4, 'premium', 1000),
	(5, 5, 'standard', 750);

INSERT OR IGNORE INTO "billing" (id, user_id, amount, transaction_type, created_at) VALUES
	(1, 1, 2400, 'payment', '2026-10-01 10:15:00'),
	(2, 2, 0, 'payment', '2026-10-01 10:20:00'),
	(3, 3, 1200, 'payment', '2026-10-02 09:00:00'),
	(4, 1, 500, 'refund', '2026-10-05 14:30:00'),
	(5, 4, 2400, 'payment', '2026-10-10 18:45:00'),
	(6, 5, 1800, 'payment', '2026-10-12 11:30:00');

INSERT OR IGNORE INTO "api_keys" (id, user_id, key_value) VALUES
	(1, 1, 'sk-al-4f9d2c8e17b6'),
	(2, 2, 'sk-te-9a3b5f7e2c1d'),
	(3, 3, 'sk-ki-7e1f4b9a3d2c'),
	(4, 4, 'sk-ri-2c8e5a7f1b9d'),
	(5, 5, 'sk-he-6b3a9d1e4f7c');

INSERT OR IGNORE INTO "chats" (id, user_id, model_id, title) VALUES
	(1, 1, 1, 'Physics homework help'),
	(2, 1, 2, 'Vacation photo tagging'),
	(3, 2, 1, 'Latvian essay draft'),
	(4, 3, 4, 'Search embeddings demo'),
	(5, 4, 3, 'Transcribe lecture audio');

INSERT OR IGNORE INTO "prompts" (id, user_id, title, body) VALUES
	(1, 1, 'Explain entropy', 'Explain thermodynamic entropy in simple words for a high school student.'),
	(2, 2, 'Essay outline', 'Create an outline for an essay about Riga in three paragraphs.'),
	(3, 4, 'Photo tags', 'Suggest five short caption tags for a sunset photo taken in Jurmala.'),
	(4, 5, 'Summarize meeting', 'Summarize the following meeting notes in five bullet points.');