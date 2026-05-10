--CREATE DATABASE "quack-test" TEMPLATE "template0";
--DROP DATABASE "quack-test";
--SELECT current_database();
/* DO $$ 
DECLARE 
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS public.' || r.tablename || ' CASCADE';
    END LOOP;
END $$; */;

-- Создание таблицы пользователей
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL CHECK (username ~ '^[a-zA-Z0-9_]+$'),
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы криптовалют
CREATE TABLE crypto_currencies (
    crypto_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    code_name VARCHAR(50) NOT NULL
);

-- Создание таблицы кошельков
CREATE TABLE wallets (
    wallet_id SERIAL PRIMARY KEY,
    deposit_address VARCHAR(255) UNIQUE NOT NULL,
    crypto_id INT NOT NULL REFERENCES crypto_currencies(crypto_id) ON DELETE RESTRICT,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    balance DECIMAL(20, 8) DEFAULT 0.0 NOT NULL,
    UNIQUE (user_id, crypto_id)
);

-- Создание таблицы коллекций
CREATE TABLE collections (
    collection_id SERIAL PRIMARY KEY,
    crypto_id INT NOT NULL REFERENCES crypto_currencies(crypto_id) ON DELETE RESTRICT,
    mint_cost DECIMAL(20, 8) CHECK (mint_cost >= 0) NOT NULL,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

-- Создание таблицы NFT
CREATE TABLE nfts (
    nft_id SERIAL PRIMARY KEY,
    collection_id INT NOT NULL REFERENCES collections(collection_id) ON DELETE CASCADE,
	owner_id INT REFERENCES users(user_id) ON DELETE SET NULL,
    image_url VARCHAR(255) UNIQUE,
    mint_date TIMESTAMP -- дата первой покупки
);

-- Создание таблицы атрибутов NFT
CREATE TABLE attributes (
    attribute_id SERIAL PRIMARY KEY,
    attribute_name VARCHAR(50),
    attribute_value VARCHAR(50),
    UNIQUE (attribute_name, attribute_value)
);

-- Связующая таблица NFT и Attributes
CREATE TABLE nft_attributes (
    attribute_link_id SERIAL PRIMARY KEY,
    attribute_id INT NOT NULL REFERENCES attributes(attribute_id) ON DELETE CASCADE,
    nft_id INT NOT NULL REFERENCES nfts(nft_id) ON DELETE CASCADE,
    UNIQUE (attribute_id, nft_id)
);

-- Создание таблицы сделок
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    nft_id INT REFERENCES nfts(nft_id) ON DELETE SET NULL,
    buyer_id INT REFERENCES users(user_id) DEFAULT NULL ON DELETE SET NULL,
    seller_id INT REFERENCES users(user_id) ON DELETE SET NULL,
    price DECIMAL(20, 8) CHECK (price >= 0) NOT NULL,
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    end_date TIMESTAMP DEFAULT NULL,
    CONSTRAINT start_before_end CHECK (
    	end_date IS NULL OR start_date <= end_date
	)
);

-- Предотвращение двойного выставления на продажу
CREATE UNIQUE INDEX unique_active_sale_per_nft
ON transactions (seller_id, nft_id)
WHERE end_date IS NULL;



INSERT INTO collections (crypto_id, name, description)
VALUES (1, 'Новая Коллекция PFP', 'Коллекция PFP деловитые персонажи с новыми атрибутами')
RETURNING collection_id;

SELECT * FROM users u;
SELECT * FROM nft_attributes a
JOIN nfts n ON n.nft_id = a.nft_id
WHERE n.collection_id = 1;

INSERT INTO users (username, password_hash, email)
VALUES ('name1', '123', 'email1');

INSERT INTO wallets (deposit_address, crypto_id, user_id, balance)
VALUES ('addr', 1, 5, 99);

;SELECT * FROM users;
;SELECT * FROM nfts;
;SELECT * FROM collections;
;SELECT * FROM wallets;
;SELECT * FROM crypto_currencies;
;SELECT * FROM transactions;

UPDATE wallets
SET balance = balance + 10
WHERE user_id = 2 AND crypto_id = 1;

UPDATE transactions
SET buyer_id = NULL, end_date = NULL
WHERE id = 1;

INSERT INTO nfts (collection_id, image_url)
VALUES (3, 'image2');

INSERT INTO transactions (nft_id, buyer_id, seller_id, price, is_sale)
VALUES (4, 2, NULL, 0.0, TRUE);

COPY transactions TO '/tmp/file.csv' WITH (FORMAT csv, HEADER true);
COPY transactions FROM '/tmp/file.csv' WITH (FORMAT csv, HEADER true);


