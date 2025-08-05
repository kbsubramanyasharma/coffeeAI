import { useEffect, useState } from 'react';
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navigation from '@/components/Navigation';
import Chatbot from '@/components/Chatbot';
import Home from './pages/Home';
import ProductDetail from './pages/ProductDetail';
import Cart from './pages/Cart';
import Checkout from './pages/Checkout';
import NotFound from "./pages/NotFound";
import Login from './pages/Login';
import Register from './pages/Register';
import { Product } from '@/components/ProductCard';
import { isLoggedIn } from './lib/utils';
import { toast } from '@/hooks/use-toast';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import { useUser } from '@/context/UserContext';
import OurStory from './pages/OurStory';
import { apiService } from '@/services/api';
import { UserProvider } from '@/context/UserContext';
import { CartProvider, useCart } from '@/context/CartContext';

const queryClient = new QueryClient();

// Main app component that uses the UserContext and CartContext
const MainApp = () => {
  const { setUser, user } = useUser();
  const { cartItems, cartItemCount, addToCart, updateQuantity, removeItem, clearCart } = useCart();
  const [isChatOpen, setIsChatOpen] = useState(false);

  const handleAddToCart = async (product: Product) => {
    await addToCart(product);
  };

  const handleUpdateQuantity = async (cartId: string, newQuantity: number) => {
    await updateQuantity(cartId, newQuantity);
  };

  const handleRemoveItem = async (cartId: string) => {
    await removeItem(cartId);
  };

  const handleClearCart = async () => {
    await clearCart();
  };

  const toggleChat = () => {
    if (!isLoggedIn()) {
      toast({ title: 'Authentication Required', description: 'Please login or register to use this feature.' });
      return;
    }
    setIsChatOpen(!isChatOpen);
  };

  const handleLogout = () => {
    // Remove token and user_id from localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_name'); // Clear user name
    localStorage.removeItem('session_id'); // Clear session_id on logout
    localStorage.removeItem('chatbotSessionId'); // Clear chatbot session on logout
    setUser(null); // Clear user from context
    toast({ title: 'Logged out', description: 'You have been logged out.' });
    // Cart will be cleared automatically by the CartProvider when user changes
  };

  return (
    <div className="min-h-screen bg-background w-full">
      <Navigation 
        cartItemCount={cartItemCount}
        onChatToggle={toggleChat}
        onLogout={handleLogout}
      />
              
              <Routes>
                <Route 
                  path="/" 
                  element={<Home onAddToCart={handleAddToCart} />} 
                />
                <Route 
                  path="/product/:id" 
                  element={<ProductDetail onAddToCart={handleAddToCart} />} 
                />
                <Route 
                  path="/our-story" 
                  element={<OurStory />} 
                />
                <Route 
                  path="/cart" 
                  element={
                    <Cart 
                      cartItems={cartItems}
                      onUpdateQuantity={handleUpdateQuantity}
                      onRemoveItem={handleRemoveItem}
                      onClearCart={handleClearCart}
                    />
                  } 
                />
                <Route 
                  path="/checkout" 
                  element={
                    <Checkout 
                      cartItems={cartItems}
                      onClearCart={handleClearCart}
                    />
                  } 
                />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/forgot-password" element={<ForgotPassword />} />
                <Route path="/reset-password" element={<ResetPassword />} />
                <Route path="*" element={<NotFound />} />
              </Routes>

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

// App wrapper component that provides context
const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <UserProvider>
          <CartProvider>
            <BrowserRouter>
              <MainApp />
            </BrowserRouter>
          </CartProvider>
          <Toaster />
          <Sonner />
        </UserProvider>
      </TooltipProvider>
    </QueryClientProvider>
  );
};

export default App;
