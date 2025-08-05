import sqlite3

DB_PATH = 'database/coffee_shop.db'

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# 1. Backup existing cart_items data (excluding session_id)
c.execute('''
    CREATE TABLE IF NOT EXISTS cart_items_backup AS 
    SELECT id, user_id, product_id, quantity, selected_size, customizations, unit_price, total_price, created_at, updated_at 
    FROM cart_items
''')

# 2. Drop the old cart_items table
c.execute('DROP TABLE IF EXISTS cart_items')

# 3. Recreate the new cart_items table without session_id
c.execute('''
    CREATE TABLE cart_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        selected_size VARCHAR(50),
        customizations TEXT,
        unit_price DECIMAL(10,2) NOT NULL,
        total_price DECIMAL(10,2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
''')

# 4. Restore data from backup
c.execute('''
    INSERT INTO cart_items (id, user_id, product_id, quantity, selected_size, customizations, unit_price, total_price, created_at, updated_at)
    SELECT id, user_id, product_id, quantity, selected_size, customizations, unit_price, total_price, created_at, updated_at FROM cart_items_backup
''')

# 5. Drop the backup table
c.execute('DROP TABLE IF EXISTS cart_items_backup')

conn.commit()
conn.close()

print('Migration complete: session_id removed from cart_items table.') 