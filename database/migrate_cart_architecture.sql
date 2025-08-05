-- Improved Cart Architecture Schema
-- This migration will create a proper cart table structure

-- Create new cart table
CREATE TABLE IF NOT EXISTS carts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id VARCHAR(255),
    status VARCHAR(20) DEFAULT 'active',  -- active, abandoned, converted
    total_items INTEGER DEFAULT 0,
    total_amount DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, status) -- Only one active cart per user
);

-- Backup existing cart_items
CREATE TABLE IF NOT EXISTS cart_items_backup AS SELECT * FROM cart_items;

-- Drop existing cart_items table
DROP TABLE IF EXISTS cart_items;

-- Create new cart_items table with proper foreign key to carts
CREATE TABLE IF NOT EXISTS cart_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    selected_size VARCHAR(50),
    customizations TEXT,  -- JSON string
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    UNIQUE(cart_id, product_id, selected_size, customizations) -- Prevent duplicates
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_carts_user ON carts(user_id);
CREATE INDEX IF NOT EXISTS idx_carts_session ON carts(session_id);
CREATE INDEX IF NOT EXISTS idx_carts_status ON carts(status);
CREATE INDEX IF NOT EXISTS idx_cart_items_cart ON cart_items(cart_id);
CREATE INDEX IF NOT EXISTS idx_cart_items_product ON cart_items(product_id);

-- Migrate existing data
INSERT INTO carts (user_id, session_id, status, created_at, updated_at)
SELECT DISTINCT 
    user_id,
    NULL as session_id,  -- We'll generate this later
    'active' as status,
    MIN(created_at) as created_at,
    MAX(updated_at) as updated_at
FROM cart_items_backup
GROUP BY user_id;

-- Migrate cart items
INSERT INTO cart_items (cart_id, product_id, quantity, selected_size, customizations, unit_price, total_price, created_at, updated_at)
SELECT 
    c.id as cart_id,
    cib.product_id,
    cib.quantity,
    cib.selected_size,
    cib.customizations,
    cib.unit_price,
    cib.total_price,
    cib.created_at,
    cib.updated_at
FROM cart_items_backup cib
JOIN carts c ON c.user_id = cib.user_id;

-- Update cart totals
UPDATE carts SET 
    total_items = (
        SELECT SUM(quantity) 
        FROM cart_items 
        WHERE cart_id = carts.id
    ),
    total_amount = (
        SELECT SUM(total_price) 
        FROM cart_items 
        WHERE cart_id = carts.id
    );

-- Clean up backup table
DROP TABLE cart_items_backup;
