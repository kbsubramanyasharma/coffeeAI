# Cafe Chat Corner - Complete Setup Guide

This guide will help you set up the complete Cafe Chat Corner application with SQLite database integration.

## Project Overview

**Cafe Chat Corner** is a full-stack coffee shop application featuring:
- **Frontend**: React + TypeScript + Vite with shadcn/ui components
- **Backend**: FastAPI + SQLite + SQLAlchemy
- **AI Integration**: Google Gemini AI chatbot
- **Database**: Complete SQLite database with 6 tables
- **Features**: Product catalog, shopping cart, order management, user management

## Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **Git**

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd cafe-chat-corner-main

# Install frontend dependencies
npm install

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..
```

### 2. Backend Setup

```bash
cd backend

# Create environment file
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env

# Test database setup
python test_db.py

# Seed the database with sample data
python seed_data.py

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
# In a new terminal, from the project root
npm run dev
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Database Schema

The application uses a comprehensive SQLite database with the following tables:

### 1. Categories Table
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

### 2. Products Table
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    full_description TEXT,
    price FLOAT NOT NULL,
    image VARCHAR(500),
    rating FLOAT DEFAULT 0.0,
    category_id INTEGER NOT NULL,
    is_popular BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    allergens JSON,
    ingredients JSON,
    nutrition_info JSON,
    brewing_notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

### 3. Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

### 4. Orders Table
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    total_amount FLOAT NOT NULL,
    tax_amount FLOAT DEFAULT 0.0,
    discount_amount FLOAT DEFAULT 0.0,
    final_amount FLOAT NOT NULL,
    payment_status VARCHAR(50) DEFAULT 'pending',
    payment_method VARCHAR(50),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 5. Order Items Table
```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price FLOAT NOT NULL,
    total_price FLOAT NOT NULL,
    selected_size VARCHAR(50),
    customizations JSON,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### 6. Cart Items Table
```sql
CREATE TABLE cart_items (
    id INTEGER PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    user_id INTEGER,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    selected_size VARCHAR(50),
    customizations JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

## API Endpoints

### Base URL: `http://localhost:8000/api/v1`

#### Products
- `GET /products/` - List all products
- `GET /products/{id}` - Get product by ID
- `GET /products/popular/` - Get popular products
- `POST /products/` - Create new product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

#### Categories
- `GET /categories/` - List all categories
- `GET /categories/{id}` - Get category by ID
- `POST /categories/` - Create new category

#### Cart
- `GET /cart/?session_id={id}` - Get cart items
- `POST /cart/` - Add item to cart
- `PUT /cart/{id}?quantity={qty}` - Update cart item
- `DELETE /cart/{id}` - Remove item from cart
- `DELETE /cart/?session_id={id}` - Clear cart

#### Orders
- `GET /orders/` - List orders
- `POST /orders/` - Create new order
- `GET /orders/{id}` - Get order by ID
- `GET /orders/number/{number}` - Get order by number
- `PUT /orders/{id}/status` - Update order status

#### Users
- `GET /users/` - List users
- `POST /users/` - Create new user
- `GET /users/{id}` - Get user by ID

#### Utility
- `GET /session-id/` - Generate session ID

#### Chatbot (Legacy)
- `POST /api/chatbot` - AI chatbot endpoint

## Sample Data

The database comes pre-seeded with:

### Categories
- Signature (Our signature coffee blends)
- Specialty (Specialty coffee drinks)
- Alternative (Dairy-free and alternative milk options)
- Cold Brew (Cold-extracted coffee beverages)
- Frozen (Blended and frozen coffee drinks)
- Single Origin (Single-origin coffee varieties)

### Products
1. **BrewMaster Signature Blend** - Signature category, $4.99
2. **Caramel Macchiato** - Specialty category, $5.49
3. **Oat Milk Latte** - Alternative category, $4.79
4. **Cold Brew Concentrate** - Cold Brew category, $3.99
5. **Vanilla Bean Frappé** - Frozen category, $5.99
6. **Ethiopian Single Origin** - Single Origin category, $6.49

## Frontend Integration

The frontend includes a new API service (`src/services/api.ts`) that provides:

- Type-safe API calls
- Error handling
- Request/response interfaces
- Session management
- Cart operations
- Order management

### Usage Example

```typescript
import { apiService } from '@/services/api';

// Get all products
const { products } = await apiService.getProducts();

// Get popular products
const popularProducts = await apiService.getPopularProducts();

// Add to cart
await apiService.addToCart({
  session_id: 'user-session-123',
  product_id: 1,
  quantity: 2,
  selected_size: 'Large'
});

// Get cart
const cart = await apiService.getCart('user-session-123');
```

## Development Workflow

### 1. Database Changes
```bash
cd backend
# Edit models.py for schema changes
# Run test_db.py to verify changes
python test_db.py
```

### 2. API Development
```bash
cd backend
# Edit api.py for new endpoints
# Test with uvicorn
uvicorn main:app --reload
```

### 3. Frontend Development
```bash
# Edit components and services
npm run dev
```

### 4. Testing
```bash
# Backend tests
cd backend
python test_db.py

# Frontend tests
npm run test
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure SQLite is installed
   - Check file permissions for database creation
   - Run `python test_db.py` to diagnose

2. **API Connection Error**
   - Verify backend is running on port 8000
   - Check CORS settings
   - Ensure frontend is using correct API URL

3. **Missing Dependencies**
   - Run `pip install -r requirements.txt` in backend
   - Run `npm install` in frontend

4. **Environment Variables**
   - Create `.env` file in backend directory
   - Add `GEMINI_API_KEY=your_key_here`

### Debug Commands

```bash
# Test database
cd backend && python test_db.py

# Check API health
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs

# Check database file
ls -la backend/cafe_chat_corner.db
```

## Production Deployment

### Backend
1. Use PostgreSQL instead of SQLite
2. Set up proper environment variables
3. Configure CORS for production domain
4. Add authentication/authorization
5. Set up logging and monitoring

### Frontend
1. Build for production: `npm run build`
2. Serve static files
3. Configure API URL for production
4. Set up CDN for assets

## File Structure

```
cafe-chat-corner-main/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── database.py          # Database config
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Database operations
│   ├── api.py               # API routes
│   ├── seed_data.py         # Database seeder
│   ├── test_db.py           # Database tests
│   ├── requirements.txt     # Python deps
│   └── README.md           # Backend docs
├── src/
│   ├── services/
│   │   └── api.ts          # Frontend API service
│   ├── components/         # React components
│   ├── pages/             # Page components
│   └── types/             # TypeScript types
├── package.json           # Frontend deps
└── setup.md              # This file
```

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check console logs for errors
4. Verify database connectivity

The application is now fully set up with a proper SQLite database and comprehensive API integration! 