import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navigation from '../components/Navigation';
import Chatbot from '../components/Chatbot';
import Home from './Home';
import { Product } from '../components/ProductCard';
import { apiService } from '../services/api';

interface CartItem extends Product {
  id: string;
  cartId: string;
  selectedSize?: string;
  customizations?: string[];
  quantity: number;
}

const Index = () => {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const navigate = useNavigate();

  // Helper to check if user is logged in
  const isLoggedIn = !!localStorage.getItem('token') && !!localStorage.getItem('user_id');
  const userId = localStorage.getItem('user_id');
  const token = localStorage.getItem('token');

  // Fetch cart from backend if logged in
  useEffect(() => {
    const fetchCart = async () => {
      if (isLoggedIn && userId && token) {
        try {
          console.log('Fetching cart from BACKEND for user', userId);
          const response = await apiService.getCart(undefined, parseInt(userId));
          const backendCartItems = response.items.map(item => ({
            ...item.product,
            id: String(item.product.id),
            cartId: `${item.product_id}-${item.id}`,
            selectedSize: item.selected_size,
            quantity: item.quantity,
            image: item.product.image || '',
            category: typeof item.product.category === 'object' && item.product.category?.name ? item.product.category.name : String(item.product.category),
          }));
          setCartItems(backendCartItems);
        } catch (error) {
          console.error('Failed to fetch cart from backend:', error);
        }
      }
    };
    fetchCart();
  }, [isLoggedIn, userId, token]);

  const handleAddToCart = async (product: Product) => {
    if (!(isLoggedIn && userId && token)) {
      console.log('Not logged in, cannot add to cart');
      return;
    }
    try {
      console.log('Using BACKEND cart logic for add');
      await apiService.addToCart({
        user_id: parseInt(userId),
        product_id: parseInt(product.id),
        quantity: 1,
      }, token);
      const response = await apiService.getCart(undefined, parseInt(userId));
      const backendCartItems = response.items.map(item => ({
        ...item.product,
        id: String(item.product.id),
        cartId: `${item.product_id}-${item.id}`,
        selectedSize: item.selected_size,
        quantity: item.quantity,
        image: item.product.image || '',
        category: typeof item.product.category === 'object' && item.product.category?.name ? item.product.category.name : String(item.product.category),
      }));
      setCartItems(backendCartItems);
      navigate('/cart');
      console.log(`Added ${product.name} to cart`);
    } catch (error) {
      console.error('Failed to add to cart:', error);
    }
  };

  // For brevity, update/remove/clear handlers for backend can be added similarly
  // For now, keep guest cart logic as is for those actions

  const handleUpdateQuantity = async (cartId: string, newQuantity: number) => {
    if (!(isLoggedIn && userId && token)) return;
    const item = cartItems.find(item => item.cartId === cartId);
    if (!item) return;
    try {
      console.log('Using BACKEND cart logic for update');
      await apiService.updateCartItem({
        user_id: parseInt(userId),
        product_id: parseInt(item.id),
        quantity: newQuantity,
      }, token);
      const response = await apiService.getCart(undefined, parseInt(userId));
      const backendCartItems = response.items.map(item => ({
        ...item.product,
        cartId: `${item.product_id}-${item.id}`,
        selectedSize: item.selected_size,
        quantity: item.quantity,
        id: String(item.product.id),
        category: typeof item.product.category === 'object' && item.product.category?.name ? item.product.category.name : String(item.product.category),
        image: item.product.image || item.product.image_url || '',
      }));
      setCartItems(backendCartItems);
    } catch (error) {
      console.error('Failed to update cart item in backend:', error);
    }
  };

  const handleRemoveItem = async (cartId: string) => {
    if (!(isLoggedIn && userId && token)) return;
    const item = cartItems.find(item => item.cartId === cartId);
    if (!item) return;
    try {
      console.log('Using BACKEND cart logic for remove');
      await apiService.removeFromCart({
        user_id: parseInt(userId),
        product_id: parseInt(item.id),
      }, token);
      const response = await apiService.getCart(undefined, parseInt(userId));
      const backendCartItems = response.items.map(item => ({
        ...item.product,
        cartId: `${item.product_id}-${item.id}`,
        selectedSize: item.selected_size,
        quantity: item.quantity,
        id: String(item.product.id),
        category: typeof item.product.category === 'object' && item.product.category?.name ? item.product.category.name : String(item.product.category),
        image: item.product.image || item.product.image_url || '',
      }));
      setCartItems(backendCartItems);
    } catch (error) {
      console.error('Failed to remove cart item in backend:', error);
    }
  };

  const handleClearCart = async () => {
    if (!(isLoggedIn && userId && token)) return;
    try {
      console.log('Using BACKEND cart logic for clear');
      await apiService.clearCart({
        user_id: parseInt(userId),
      }, token);
      setCartItems([]);
    } catch (error) {
      console.error('Failed to clear cart in backend:', error);
    }
  };

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navigation 
        cartItemCount={cartItems.length}
        onChatToggle={toggleChat}
        onLogout={() => {}}
      />
      <main>
        <Home onAddToCart={handleAddToCart} />
      </main>
      <Chatbot 
        isOpen={isChatOpen}
        onToggle={toggleChat}
      />
      {/* Footer */}
      <footer className="bg-muted/30 py-12 mt-16">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                  <span className="text-primary-foreground font-bold text-sm">B</span>
                </div>
                <span className="font-bold text-lg">BrewMaster</span>
              </div>
              <p className="text-muted-foreground text-sm">
                Crafting exceptional coffee experiences since 2020. 
                Every cup tells a story of quality and passion.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Quick Links</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">Menu</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Locations</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Careers</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Contact Us</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Shipping Info</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Returns</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Connect</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">Newsletter</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Instagram</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Twitter</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Facebook</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t mt-8 pt-8 text-center text-sm text-muted-foreground">
            <p>&copy; 2024 BrewMaster. All rights reserved. Made with ❤️ for coffee lovers.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
