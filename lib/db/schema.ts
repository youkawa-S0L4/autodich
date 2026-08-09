import { pgTable, text, timestamp, boolean, serial, integer } from "drizzle-orm/pg-core"

// --- Better Auth required tables -------------------------------------------
// Column names are camelCase to match Better Auth's defaults. Do not rename.

export const user = pgTable("user", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  emailVerified: boolean("emailVerified").notNull().default(false),
  image: text("image"),
  createdAt: timestamp("createdAt").notNull().defaultNow(),
  updatedAt: timestamp("updatedAt").notNull().defaultNow(),
})

export const session = pgTable("session", {
  id: text("id").primaryKey(),
  expiresAt: timestamp("expiresAt").notNull(),
  token: text("token").notNull().unique(),
  createdAt: timestamp("createdAt").notNull().defaultNow(),
  updatedAt: timestamp("updatedAt").notNull().defaultNow(),
  ipAddress: text("ipAddress"),
  userAgent: text("userAgent"),
  userId: text("userId")
    .notNull()
    .references(() => user.id, { onDelete: "cascade" }),
})

export const account = pgTable("account", {
  id: text("id").primaryKey(),
  accountId: text("accountId").notNull(),
  providerId: text("providerId").notNull(),
  userId: text("userId")
    .notNull()
    .references(() => user.id, { onDelete: "cascade" }),
  accessToken: text("accessToken"),
  refreshToken: text("refreshToken"),
  idToken: text("idToken"),
  accessTokenExpiresAt: timestamp("accessTokenExpiresAt"),
  refreshTokenExpiresAt: timestamp("refreshTokenExpiresAt"),
  scope: text("scope"),
  password: text("password"),
  createdAt: timestamp("createdAt").notNull().defaultNow(),
  updatedAt: timestamp("updatedAt").notNull().defaultNow(),
})

export const verification = pgTable("verification", {
  id: text("id").primaryKey(),
  identifier: text("identifier").notNull(),
  value: text("value").notNull(),
  expiresAt: timestamp("expiresAt").notNull(),
  createdAt: timestamp("createdAt").defaultNow(),
  updatedAt: timestamp("updatedAt").defaultNow(),
})

// --- App tables ------------------------------------------------------------

// A book/series. kind = "novel" (txt/epub text) or "manga" (image pages).
export const books = pgTable("books", {
  id: serial("id").primaryKey(),
  userId: text("userId").notNull(),
  title: text("title").notNull(),
  author: text("author"),
  kind: text("kind").notNull().default("novel"), // "novel" | "manga"
  sourceLang: text("sourceLang").notNull().default("auto"), // auto | ja | zh | en
  targetLang: text("targetLang").notNull().default("vi"),
  coverImage: text("coverImage"),
  createdAt: timestamp("createdAt").notNull().defaultNow(),
  updatedAt: timestamp("updatedAt").notNull().defaultNow(),
})

// Chapters for text novels. originalText holds source, translatedText holds VI.
export const chapters = pgTable("chapters", {
  id: serial("id").primaryKey(),
  userId: text("userId").notNull(),
  bookId: integer("bookId").notNull(),
  idx: integer("idx").notNull().default(0),
  title: text("title").notNull(),
  originalText: text("originalText").notNull().default(""),
  translatedText: text("translatedText"),
  translated: boolean("translated").notNull().default(false),
  createdAt: timestamp("createdAt").notNull().defaultNow(),
})

// Pages for manga. imageUrl is a data URL / blob path. ocrText + translatedText.
export const pages = pgTable("pages", {
  id: serial("id").primaryKey(),
  userId: text("userId").notNull(),
  bookId: integer("bookId").notNull(),
  idx: integer("idx").notNull().default(0),
  imageUrl: text("imageUrl").notNull(),
  ocrText: text("ocrText"),
  translatedText: text("translatedText"),
  translated: boolean("translated").notNull().default(false),
  createdAt: timestamp("createdAt").notNull().defaultNow(),
})

// Per-user reading progress for each book.
export const progress = pgTable("progress", {
  id: serial("id").primaryKey(),
  userId: text("userId").notNull(),
  bookId: integer("bookId").notNull(),
  position: integer("position").notNull().default(0), // chapter idx or page idx
  updatedAt: timestamp("updatedAt").notNull().defaultNow(),
})
