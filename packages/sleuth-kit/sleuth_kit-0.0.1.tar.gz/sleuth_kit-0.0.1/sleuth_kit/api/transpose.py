import time
from sleuth_kit.config import Config
import requests
import os
from sleuth_kit.helpers.storage import save_to_csv, save_to_sqlite

def load_sql_query(filename):
    filepath = os.path.join('sleuth_kit', 'sql', filename)
    print(f"Loading SQL file: {filepath}")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"SQL file not found: {filepath}")
    with open(filepath, 'r') as file:
        query = file.read().strip()
    if not query:
        raise ValueError(f"SQL file is empty: {filepath}")
    print(f"Loaded query: {query}")
    return query

def query_transpose(sql_query, params=None):
    url = "https://api.transpose.io/sql"
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': Config.TRANSPOSE_API_KEY,
    }
    
    if params:
        for key, value in params.items():
            sql_query = sql_query.replace(f'{{{{{key}}}}}', str(value))
    
    print(f"Querying Transpose API for {params.get('wallet_address', 'unknown address')}")
    
    response = requests.post(url, headers=headers, json={'sql': sql_query})
    
    if response.status_code == 200:
        result = response.json()['results']
    else:
        print(f"Error making request: {response.status_code}")
        print(f"Response content: {response.text}")
        response.raise_for_status()
    
    time.sleep(1)  # Enforce a 1-second delay between queries
    
    return result

def query_ethereum_transactions(addresses):
    sql_query = load_sql_query('ethereum_transactions.sql')
    all_transactions = []
    
    for address in addresses:
        offset = 0
        limit = 100
        
        while True:
            params = {
                'wallet_address': address,
                'limit': limit,
                'offset': offset
            }
            transactions = query_transpose(sql_query, params)
            
            if not transactions:
                break
            
            all_transactions.extend(transactions)
            
            # Save every 100 transactions
            save_transactions(transactions)
            print(f"Saved {len(transactions)} transactions for address {address}")
            
            offset += limit
    
    return all_transactions

def save_transactions(transactions):
    if Config.SAVE_AS_CSV:
        save_to_csv(transactions, 'data/csv/ethereum-transactions.csv', ['transaction_hash', 'base_fee_per_gas', 'block_number', 'contract_address', 'fees_burned', 'fees_rewarded', 'fees_saved', 'from_address', 'gas_limit', 'gas_price', 'gas_used', 'input', 'internal_failed_transaction_count', 'internal_transaction_count', 'log_count', 'max_fee_per_gas', 'max_priority_fee_per_gas', 'nonce', 'output', 'position', 'timestamp', 'to_address', 'transaction_fee', 'type', 'value'])
    
    if Config.SAVE_AS_SQLITE:
        save_to_sqlite(transactions, 'ethereum_transactions')

def query_ethereum_account(address: str):
    sql_query = load_sql_query('ethereum_accounts.sql')
    return query_transpose(sql_query, {'address': address})