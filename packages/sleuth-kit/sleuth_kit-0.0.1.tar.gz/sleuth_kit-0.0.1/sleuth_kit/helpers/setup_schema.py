import sqlite3
import os

def setup_database_schema(db_path='data/sqlite/blocks.db'):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create ethereum_accounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ethereum_accounts (
            address TEXT PRIMARY KEY,
            created_timestamp TEXT,
            creator_address TEXT,
            last_active_timestamp TEXT,
            type TEXT
        )
    ''')

    # Create ethereum_transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ethereum_transactions (
            transaction_hash TEXT PRIMARY KEY,
            base_fee_per_gas NUMERIC,
            block_number INTEGER,
            contract_address TEXT,
            fees_burned NUMERIC,
            fees_rewarded NUMERIC,
            fees_saved NUMERIC,
            from_address TEXT,
            gas_limit NUMERIC,
            gas_price NUMERIC,
            gas_used NUMERIC,
            input TEXT,
            internal_failed_transaction_count INTEGER,
            internal_transaction_count INTEGER,
            log_count INTEGER,
            max_fee_per_gas NUMERIC,
            max_priority_fee_per_gas NUMERIC,
            nonce INTEGER,
            output TEXT,
            position INTEGER,
            timestamp TIMESTAMP,
            to_address TEXT,
            transaction_fee NUMERIC,
            type INTEGER,
            value NUMERIC
        )
    ''')

    conn.commit()
    conn.close()

    print(f"Database schema set up successfully at {db_path}")