require("dotenv").config();

const fs = require("fs/promises");
const path = require("path");
const { Client } = require("pg");

async function migrate() {
  if (!process.env.DATABASE_URL) {
    throw new Error("Brak zmiennej DATABASE_URL");
  }

  const migrationPath = path.join(
    __dirname,
    "..",
    "migrations",
    "001_create_users.sql"
  );
  const sql = await fs.readFile(migrationPath, "utf8");
  const client = new Client({ connectionString: process.env.DATABASE_URL });

  try {
    await client.connect();
    await client.query(sql);
    console.log("Migracja została wykonana.");
  } finally {
    await client.end();
  }
}

migrate().catch((error) => {
  console.error("Błąd migracji:", error);
  process.exitCode = 1;
});
