DROP TABLE IF EXISTS wallets;
DROP TABLE IF EXISTS pending;

CREATE TABLE wallets (
  username TEXT PRIMARY KEY UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE pending (
  wallet TEXT PRIMARY KEY,
  amount INTEGER,
  receiver TEXT NOT NULL,
  creation_time INTEGER,
  redirect_url TEXT
);

CREATE TABLE transaction_history (
  receiver TEXT NOT NULL,
  wallet TEXT,
  payment_time INTEGER,
  amount INTEGER,
  redirect_url TEXT
);