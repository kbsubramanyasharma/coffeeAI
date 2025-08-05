// API service for connecting to the Cafe Chat Corner backend

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Types for API responses
export interface ApiProduct {
  id: number;
  name: string;
  description: string;
  full_description?: string;
  price: number;
  retail_price?: number;
  image?: string;
  image_url?: string;
  rating: number;
  category_id: number;
  is_popular: boolean;
  is_active: boolean;
  allergens?: string[];
  ingredients?: string[];
  nutrition_info?: {
    calories: number;
    caffeine: string;
    fat: string;
    carbs: string;
    protein: string;
    sugar: string;
  };
  brewing_notes?: string;
  created_at: string;
  updated_at?: string;
  category: {
    id: number;
    name: string;
    description?: string;
  };
}

export interface ApiCategory {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at?: string;
}

export interface ApiCartItem {
  id: number;
  session_id: string;
  user_id?: number;
  product_id: number;
  quantity: number;
  selected_size?: string;
  customizations?: Record<string, any>;
  created_at: string;
  updated_at?: string;
  product: ApiProduct;
}

export interface ApiCartResponse {
  items: ApiCartItem[];
  total_items: number;
  total_amount: number;
}

export interface ApiOrderItem {
  id: number;
  order_id: number;
  product_id: number;
  quantity: number;
  unit_price: number;
  total_price: number;
  selected_size?: string;
  customizations?: Record<string, any>;
  notes?: string;
  created_at: string;
  product: ApiProduct;
}

export interface ApiOrder {
  id: number;
  user_id?: number;
  order_number: string;
  status: string;
  total_amount: number;
  tax_amount: number;
  discount_amount: number;
  final_amount: number;
  payment_status: string;
  payment_method?: string;
  notes?: string;
  created_at: string;
  updated_at?: string;
  order_items: ApiOrderItem[];
}

// API service class
class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    // Always set Content-Type to application/json for JSON requests
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Cart endpoint used in the app
  async addToCart(data: {
    session_id: string;
    user_id?: number;
    product_id: number;
    quantity: number;
    selected_size?: string;
    customizations?: Record<string, any>;
  }, token?: string): Promise<ApiCartItem> {
    return this.request('/cart/', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
  }

  // Session endpoint used in the app
  async generateSessionId(): Promise<{ session_id: string }> {
    return this.request('/session-id/');
  }

  // Product endpoint used in the app
  async getProducts(params?: {
    skip?: number;
    limit?: number;
    category_id?: number;
    is_popular?: boolean;
    is_active?: boolean;
    search?: string;
  }): Promise<{ products: ApiProduct[]; total: number; page: number; per_page: number }> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    const queryString = searchParams.toString();
    const endpoint = `/products/${queryString ? `?${queryString}` : ''}`;
    return this.request(endpoint);
  }

  // Get a single product by ID
  async getProductById(productId: string | number): Promise<ApiProduct> {
    return this.request(`/products/${productId}`);
  }

  // Cart endpoint to fetch cart items
  async getCart(sessionId?: string, userId?: number): Promise<ApiCartResponse> {
    const params = new URLSearchParams();
    if (sessionId) params.append('session_id', sessionId);
    if (userId) params.append('user_id', userId.toString());
    return this.request(`/cart/?${params.toString()}`);
  }

  // User login
  async login(email: string, password: string): Promise<{ access_token: string; user_id: number }> {
    return this.request('/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  // Get user profile
  async getUserProfile(token: string): Promise<{ id: number; email: string; first_name: string; last_name: string }> {
    return this.request('/users/me', {
      headers: { Authorization: `Bearer ${token}` },
    });
  }

  // Place order (checkout)
  async checkout(orderData: any, token?: string): Promise<ApiOrder> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return this.request('/orders/', {
      method: 'POST',
      body: JSON.stringify(orderData),
      headers,
    });
  }

  // Get order history for the logged-in user
  async getOrders(token: string): Promise<ApiOrder[]> {
    return this.request('/orders/', {
      headers: { Authorization: `Bearer ${token}` },
    });
  }

  // Get a specific order by ID
  async getOrderById(orderId: number, token: string): Promise<ApiOrder> {
    return this.request(`/orders/${orderId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
  }

  // Update cart item quantity
  async updateCartItemQuantity(cartItemId: number, quantity: number, token?: string): Promise<void> {
    return this.request(`/cart/${cartItemId}?quantity=${quantity}`, {
      method: 'PUT',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
  }

  // Remove item from cart
  async removeFromCart(cartItemId: number, token?: string): Promise<void> {
    return this.request(`/cart/${cartItemId}`, {
      method: 'DELETE',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
  }

  // Clear entire cart
  async clearCart(sessionId?: string, userId?: number, token?: string): Promise<void> {
    const params = new URLSearchParams();
    if (sessionId) params.append('session_id', sessionId);
    if (userId) params.append('user_id', userId.toString());
    
    return this.request(`/cart/?${params.toString()}`, {
      method: 'DELETE',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
  }

  // Forgot password - send reset email
  async forgotPassword(email: string): Promise<{ message: string; reset_token?: string }> {
    return this.request('/forgot-password', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
  }

  // Reset password with token
  async resetPassword(token: string, newPassword: string): Promise<{ message: string }> {
    return this.request('/reset-password', {
      method: 'POST',
      body: JSON.stringify({ token, new_password: newPassword }),
    });
  }
}

export const apiService = new ApiService();

// Export the class for testing or custom instances
export default ApiService; 