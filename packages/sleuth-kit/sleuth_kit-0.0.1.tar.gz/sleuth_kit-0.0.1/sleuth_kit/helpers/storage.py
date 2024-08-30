import csv
import sqlite3
import os

def save_to_csv(data, filepath, fieldnames):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Read existing data
    existing_data = []
    if os.path.exists(filepath):
        with open(filepath, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            existing_data = list(reader)

    # Convert existing data to a dictionary for easy updating
    existing_data_dict = {row[fieldnames[0]]: row for row in existing_data} if existing_data else {}

    # Update existing data or add new data
    for record in data:
        key = record.get(fieldnames[0])
        if key:
            existing_data_dict[key] = record

    # Write all data (updated and new) back to CSV
    with open(filepath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_data_dict.values())

def save_to_sqlite(data, table_name, db_path='data/sqlite/blocks.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Upsert (insert or update) records
    placeholders = ', '.join(['?' for _ in data[0].keys()])
    columns = ', '.join(data[0].keys())
    sql = f'''
        INSERT OR REPLACE INTO {table_name} ({columns})
        VALUES ({placeholders})
    '''

    # Convert large integers to strings
    for record in data:
        for key, value in record.items():
            if isinstance(value, int) and value > 2**63 - 1:
                record[key] = str(value)

    # Save in batches of 100
    batch_size = 100
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        cursor.executemany(sql, [tuple(record.values()) for record in batch])
        conn.commit()

    conn.close()