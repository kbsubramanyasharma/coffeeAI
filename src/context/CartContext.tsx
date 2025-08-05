import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiService } from '@/services/api';
import { isLoggedIn } from '@/lib/utils';
import { toast } from '@/hooks/use-toast';
import { Product } from '@/components/ProductCard';

interface CartItem extends Product {
  cartId: string;
  quantity: number;
  selectedSize?: string;
}

interface CartContextType {
  cartItems: CartItem[];
  cartItemCount: number;
  loading: boolean;
  addToCart: (product: Product) => Promise<void>;
  updateQuantity: (cartId: string, newQuantity: number) => Promise<void>;
  removeItem: (cartId: string) => Promise<void>;
  clearCart: () => Promise<void>;
  refreshCart: () => Promise<void>;
  getProductQuantityInCart: (productId: string) => number;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const useCart = () => {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');

  const loadCart = async () => {
    if (!(isLoggedIn() && userId && token)) return;
    
    try {
      setLoading(true);
      
      // Get or generate session ID
      let sessionId = localStorage.getItem('session_id');
      if (!sessionId) {
        const response = await apiService.generateSessionId();
        sessionId = response.session_id;
        localStorage.setItem('session_id', sessionId);
      }
      
      const response = await apiService.getCart(sessionId, parseInt(userId));
      const backendCartItems = response.items.map(item => ({
        ...item.product,
        id: String(item.product.id),
        cartId: `${item.product_id}-${item.id}`,
        selectedSize: item.selected_size,
        quantity: item.quantity,
        image: item.product.image || '',
        category: typeof item.product.category === 'object' && item.product.category?.name 
          ? item.product.category.name 
          : String(item.product.category),
      }));
      setCartItems(backendCartItems);
    } catch (error) {
      console.error('Failed to load cart:', error);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = async (product: Product) => {
    if (!(isLoggedIn() && userId && token)) {
      toast({ title: 'Authentication Required', description: 'Please login or register to use this feature.' });
      return;
    }
    
    try {
      console.log('Adding to cart via API:', product);
      
      // Get or generate session ID
      let sessionId = localStorage.getItem('session_id');
      if (!sessionId) {
        const response = await apiService.generateSessionId();
        sessionId = response.session_id;
        localStorage.setItem('session_id', sessionId);
      }
      
      await apiService.addToCart({
        session_id: sessionId,
        user_id: parseInt(userId),
        product_id: parseInt(product.id),
        quantity: 1,
      }, token);
      
      // Reload cart from backend
      await loadCart();
      
      toast({ title: 'Success', description: `${product.name} added to cart!` });
      console.log(`Added ${product.name} to cart`);
    } catch (error) {
      console.error('Failed to add to cart:', error);
      toast({ title: 'Error', description: 'Failed to add item to cart. Please try again.' });
    }
  };

  const updateQuantity = async (cartId: string, newQuantity: number) => {
    if (!(isLoggedIn() && userId && token)) return;
    
    try {
      const cartItemId = parseInt(cartId.split('-')[1]);
      
      if (newQuantity <= 0) {
        await apiService.removeFromCart(cartItemId, token);
      } else {
        await apiService.updateCartItemQuantity(cartItemId, newQuantity, token);
      }
      
      await loadCart();
    } catch (error) {
      console.error('Failed to update cart:', error);
      toast({ title: 'Error', description: 'Failed to update cart item. Please try again.' });
    }
  };

  const removeItem = async (cartId: string) => {
    if (!(isLoggedIn() && userId && token)) return;
    
    try {
      const cartItemId = parseInt(cartId.split('-')[1]);
      await apiService.removeFromCart(cartItemId, token);
      await loadCart();
      toast({ title: 'Success', description: 'Item removed from cart' });
    } catch (error) {
      console.error('Failed to remove item:', error);
      toast({ title: 'Error', description: 'Failed to remove item from cart. Please try again.' });
    }
  };

  const clearCart = async () => {
    if (!(isLoggedIn() && userId && token)) return;
    
    try {
      const sessionId = localStorage.getItem('session_id');
      await apiService.clearCart(sessionId, parseInt(userId), token);
      setCartItems([]);
      toast({ title: 'Success', description: 'Cart cleared successfully' });
    } catch (error) {
      console.error('Failed to clear cart:', error);
      toast({ title: 'Error', description: 'Failed to clear cart. Please try again.' });
    }
  };

  const refreshCart = async () => {
    await loadCart();
  };

  const getProductQuantityInCart = (productId: string): number => {
    const item = cartItems.find(item => item.id === productId);
    return item ? item.quantity : 0;
  };

  // Load cart on mount and when user changes
  useEffect(() => {
    loadCart();
  }, [userId, token]);

  const cartItemCount = cartItems.reduce((total, item) => total + item.quantity, 0);

  return (
    <CartContext.Provider value={{
      cartItems,
      cartItemCount,
      loading,
      addToCart,
      updateQuantity,
      removeItem,
      clearCart,
      refreshCart,
      getProductQuantityInCart,
    }}>
      {children}
    </CartContext.Provider>
  );
};