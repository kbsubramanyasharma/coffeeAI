-- Coffee AI Database Schema
-- SQLite database for the complete coffee shop application

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    parent_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

-- Product groups table
CREATE TABLE IF NOT EXISTS product_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product types table
CREATE TABLE IF NOT EXISTS product_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    category_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER UNIQUE,  -- Original CSV product_id
    name VARCHAR(255) NOT NULL,
    description TEXT,
    full_description TEXT,
    product_group_id INTEGER,
    category_id INTEGER,
    product_type_id INTEGER,
    unit_of_measure VARCHAR(50),
    wholesale_price DECIMAL(10,2),
    retail_price DECIMAL(10,2),
    tax_exempt BOOLEAN DEFAULT FALSE,
    is_promo BOOLEAN DEFAULT FALSE,
    is_new BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_popular BOOLEAN DEFAULT FALSE,
    image_url TEXT,
    rating DECIMAL(3,2) DEFAULT 0.0,
    allergens TEXT,
    ingredients TEXT,
    nutrition_info TEXT,  -- JSON string
    brewing_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_group_id) REFERENCES product_groups(id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (product_type_id) REFERENCES product_types(id)
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Password reset tokens table
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Chat sessions table
CREATE TABLE IF NOT EXISTS chat_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(255) NOT NULL UNIQUE,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Chat messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    intent VARCHAR(100),
    agent VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id)
);

-- Cart table - One cart per user
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

-- Cart items table - Individual items in carts
CREATE TABLE IF NOT EXISTS cart_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    selected_size VARCHAR(50),
    customizations TEXT,  -- JSON string for product metadata (variants, options, etc.)
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    UNIQUE(cart_id, product_id, selected_size, customizations) -- Prevent duplicates
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    user_id INTEGER,
    session_id VARCHAR(255),
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    total_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    tax_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    discount_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    final_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    payment_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    payment_method VARCHAR(50),
    shipping_address TEXT,
    billing_address TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    selected_size VARCHAR(50),
    customizations TEXT,  -- JSON string
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_active ON products(is_active);
CREATE INDEX IF NOT EXISTS idx_products_popular ON products(is_popular);
CREATE INDEX IF NOT EXISTS idx_carts_user ON carts(user_id);
CREATE INDEX IF NOT EXISTS idx_carts_session ON carts(session_id);
CREATE INDEX IF NOT EXISTS idx_carts_status ON carts(status);
CREATE INDEX IF NOT EXISTS idx_cart_items_cart ON cart_items(cart_id);
CREATE INDEX IF NOT EXISTS idx_cart_items_product ON cart_items(product_id);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_chat_session ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Insert default categories
INSERT OR IGNORE INTO categories (id, name, description) VALUES
(1, 'Whole Bean/Teas', 'Coffee beans and loose tea products'),
(2, 'Beverages', 'Ready-to-drink beverages'),
(3, 'Food', 'Food items including bakery'),
(4, 'Merchandise', 'Branded merchandise and housewares'),
(5, 'Add-ons', 'Additional items and flavors');

-- Insert sub-categories
INSERT OR IGNORE INTO categories (id, name, description, parent_id) VALUES
(6, 'Coffee beans', 'Whole coffee beans', 1),
(7, 'Loose Tea', 'Loose leaf tea', 1),
(8, 'Packaged Chocolate', 'Drinking chocolate products', 1),
(9, 'Coffee', 'Coffee beverages', 2),
(10, 'Tea', 'Tea beverages', 2),
(11, 'Drinking Chocolate', 'Hot chocolate beverages', 2),
(12, 'Bakery', 'Baked goods', 3),
(13, 'Branded', 'Branded merchandise', 4),
(14, 'Flavours', 'Syrups and flavorings', 5);

-- Insert product groups
INSERT OR IGNORE INTO product_groups (id, name, description) VALUES
(1, 'Whole Bean/Teas', 'Coffee beans and loose tea products'),
(2, 'Beverages', 'Ready-to-drink beverages'),
(3, 'Food', 'Food items including bakery'),
(4, 'Merchandise', 'Branded merchandise and housewares'),
(5, 'Add-ons', 'Additional items and flavors');

-- Insert product types
INSERT OR IGNORE INTO product_types (id, name, description, category_id) VALUES
(1, 'Organic Beans', 'Organic coffee beans', 6),
(2, 'House blend Beans', 'House blend coffee beans', 6),
(3, 'Espresso Beans', 'Espresso coffee beans', 6),
(4, 'Gourmet Beans', 'Gourmet coffee beans', 6),
(5, 'Premium Beans', 'Premium coffee beans', 6),
(6, 'Green beans', 'Green coffee beans', 6),
(7, 'Herbal tea', 'Herbal tea varieties', 7),
(8, 'Black tea', 'Black tea varieties', 7),
(9, 'Green tea', 'Green tea varieties', 7),
(10, 'Chai tea', 'Chai tea varieties', 7),
(11, 'Drinking Chocolate', 'Drinking chocolate products', 8),
(12, 'Organic Chocolate', 'Organic chocolate products', 8),
(13, 'Drip coffee', 'Drip coffee beverages', 9),
(14, 'Organic brewed coffee', 'Organic brewed coffee', 9),
(15, 'Gourmet brewed coffee', 'Gourmet brewed coffee', 9),
(16, 'Premium brewed coffee', 'Premium brewed coffee', 9),
(17, 'Barista Espresso', 'Barista espresso drinks', 9),
(18, 'Seasonal drink', 'Seasonal coffee drinks', 9),
(19, 'Specialty coffee', 'Specialty coffee drinks', 9),
(20, 'Brewed herbal tea', 'Brewed herbal tea', 10),
(21, 'Brewed Green tea', 'Brewed green tea', 10),
(22, 'Brewed Black tea', 'Brewed black tea', 10),
(23, 'Brewed Chai tea', 'Brewed chai tea', 10),
(24, 'Hot chocolate', 'Hot chocolate beverages', 11),
(25, 'Seasonal drink', 'Seasonal hot chocolate', 11),
(26, 'Pastry', 'Pastry items', 12),
(27, 'Scone', 'Scone varieties', 12),
(28, 'Biscotti', 'Biscotti varieties', 12),
(29, 'Clothing', 'Branded clothing', 13),
(30, 'Housewares', 'Branded housewares', 13),
(31, 'Regular syrup', 'Regular flavored syrups', 14),
(32, 'Sugar free syrup', 'Sugar-free flavored syrups', 14); 