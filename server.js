require("dotenv").config();

const path = require("path");
const argon2 = require("argon2");
const express = require("express");
const { Pool } = require("pg");

const app = express();
const port = Number(process.env.PORT) || 3000;
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

app.post("/api/register", async (req, res) => {
  try {
    const email = String(req.body.email || "").trim().toLowerCase();
    const passwordHash = await argon2.hash(String(req.body.password || ""));

    const result = await pool.query(
      `
        INSERT INTO users (email, password_hash)
        VALUES ($1, $2)
        RETURNING id, email, created_at
      `,
      [email, passwordHash]
    );

    res.status(201).json({ user: result.rows[0] });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Nie udało się utworzyć konta." });
  }
});

app.listen(port, "0.0.0.0", () => {
  console.log(`Serwer działa pod adresem http://localhost:${port}`);
});
