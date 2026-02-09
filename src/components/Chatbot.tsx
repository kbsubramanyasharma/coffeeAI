// chatbox.tsx
import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { MessageCircle, X, Send, Coffee, ShoppingCart, Plus, Minus } from 'lucide-react';
import { v4 as uuidv4 } from 'uuid'; // Import uuid for session ID generation
import { useNavigate } from 'react-router-dom'; // Add navigation hook
import { useUser } from '@/context/UserContext'; // Import user context
import { useCart } from '@/context/CartContext'; // Import cart context
import { useToast } from '@/hooks/use-toast';
import { formatINR } from '@/lib/utils';

interface ChatProduct {
  id: string;
  name: string;
  price: number;
  buy_link: string;
  image_url: string;
  description?: string;
  unit_of_measure?: string;
  category?: string;
}

interface Message {
  id: string;
  text: string;
  isBot: boolean;
  timestamp: Date;
  products?: ChatProduct[]; // Add products to message interface
}

interface ChatbotProps {
  isOpen: boolean;
  onToggle: () => void;
}

const Chatbot: React.FC<ChatbotProps> = ({ isOpen, onToggle }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const [historyLoaded, setHistoryLoaded] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const navigate = useNavigate();
  const { user } = useUser();
  const { addToCart, updateQuantity, getProductQuantityInCart } = useCart();
  const { toast } = useToast();  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Initialize session ID and fetch chat history
  useEffect(() => {
    const initializeSession = () => {
      // Get existing session ID from localStorage or create new one
      let existingSessionId = localStorage.getItem('chatbotSessionId');
      
      if (!existingSessionId) {
        existingSessionId = uuidv4();
        localStorage.setItem('chatbotSessionId', existingSessionId);
      }
      
      setSessionId(existingSessionId);
      
      // Fetch chat history when session is initialized
      if (existingSessionId && !historyLoaded) {
        fetchChatHistory(existingSessionId);
      }
    };

    initializeSession();
  }, [historyLoaded]);

  // Fetch chat history from backend
  const fetchChatHistory = async (currentSessionId: string) => {
    try {
      console.log('Fetching chat history for session:', currentSessionId);
      setLoading(true);
      
      const response = await fetch(`http://localhost:8000/api/chat/history/${currentSessionId}`);
      
      if (!response.ok) {
        if (response.status === 404) {
          // No chat history exists yet, that's fine
          console.log('No chat history found for session:', currentSessionId);
          setHistoryLoaded(true);
          return;
        }
        throw new Error('Failed to fetch chat history');
      }

      const data = await response.json();
      console.log('Fetched chat history:', data);

      // Convert backend format to frontend format
      const fetchedMessages: Message[] = data.messages.map((msg: any) => {
        // Parse timestamp - handle both ISO format and SQLite datetime format
        let timestamp = new Date();
        if (msg.timestamp) {
          // SQLite CURRENT_TIMESTAMP format: "YYYY-MM-DD HH:MM:SS"
          // Add "Z" to treat as UTC if no timezone info present
          const timestampStr = msg.timestamp.includes('T') || msg.timestamp.includes('Z') 
            ? msg.timestamp 
            : msg.timestamp.replace(' ', 'T') + 'Z';
          timestamp = new Date(timestampStr);
        }
        
        return {
          id: msg.id || Date.now().toString(),
          text: msg.text || '',
          isBot: msg.isBot || false,
          timestamp: timestamp,
          products: [], // Products aren't stored in history, only in current responses
        };
      });

      setMessages(fetchedMessages);
      setHistoryLoaded(true);
      
      // Show a welcome message if no history exists
      if (fetchedMessages.length === 0) {
        const welcomeMessage: Message = {
          id: 'welcome-' + Date.now(),
          text: "Hello! I'm BrewMaster, your coffee assistant. I can help you find the perfect coffee, take orders, and answer any questions about our products. What can I help you with today? ☕",
          isBot: true,
          timestamp: new Date(),
        };
        setMessages([welcomeMessage]);
      }

    } catch (error) {
      console.error('Error fetching chat history:', error);
      setHistoryLoaded(true);
      
      // Show welcome message on error too
      const welcomeMessage: Message = {
        id: 'welcome-' + Date.now(),
        text: "Hello! I'm BrewMaster, your coffee assistant. I can help you find the perfect coffee, take orders, and answer any questions about our products. What can I help you with today? ☕",
        isBot: true,
        timestamp: new Date(),
      };
      setMessages([welcomeMessage]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !sessionId) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      isBot: false,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputMessage;
    setInputMessage('');
    setIsTyping(true);

    try {
      // Use the correct endpoint that matches the backend
      const response = await fetch('http://localhost:8000/api/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: currentInput, 
          session_id: sessionId,
          user_id: user?.id || null  // Include user_id if user is logged in
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      const botMessage: Message = {
        id: Date.now().toString(),
        text: data.reply, // Backend returns 'reply' field
        isBot: true,
        timestamp: new Date(),
        products: data.products || [], // Include products from backend response
      };
      setMessages(prev => [...prev, botMessage]);

      // 🛒 **CART REDIRECT LOGIC** - Check if item was added to cart
      if (data.order_processing && data.order_processing.has_order_action) {
        const cartResult = data.order_processing.cart_result;
        
        if (cartResult && cartResult.success && cartResult.cart_updated) {
          // Redirect immediately after showing cart summary
          setTimeout(() => {
            console.log('🛒 Item added to cart! Redirecting to cart page...');
            
            // Close the chatbot
            onToggle();
            
            // Redirect to cart page
            navigate('/cart');
          }, 1000); // 1 second delay to let user see the cart summary
        }
      }

    } catch (error) {
      console.error('Error sending message to chatbot backend:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: 'Sorry, I seem to be having trouble connecting to the assistant. Please try again later.',
        isBot: true,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleAddToCart = async (product: ChatProduct) => {
    if (!user) {
      toast({
        title: "Login Required",
        description: "Please log in to add items to your cart.",
        variant: "destructive",
      });
      return;
    }

    try {
      // Convert ChatProduct to Product format expected by cart context
      const productForCart = {
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image_url || '',
        category: 'Coffee', // Default category
        description: '',
        rating: 0,
        is_popular: false
      };

      await addToCart(productForCart);

      toast({
        title: "Added to Cart! 🛒",
        description: `${product.name} has been added to your cart.`,
        variant: "default",
      });

      // Optional: Navigate to cart after a brief delay
      setTimeout(() => {
        navigate('/cart');
      }, 1500);

    } catch (error) {
      console.error('Error adding to cart:', error);
      toast({
        title: "Error",
        description: "Failed to add item to cart. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleUpdateCartQuantity = async (product: ChatProduct, newQuantity: number) => {
    if (!user) {
      toast({
        title: "Login Required",
        description: "Please log in to modify your cart.",
        variant: "destructive",
      });
      return;
    }

    try {
      // For quantity updates, we need to find the cart item
      // This is a simplified approach - in a real app you'd need the cart item ID
      const productForCart = {
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image_url || '',
        category: 'Coffee',
        description: '',
        rating: 0,
        is_popular: false
      };

      if (newQuantity > 0) {
        await addToCart(productForCart);
        toast({
          title: "Cart Updated! 🛒",
          description: `${product.name} quantity updated.`,
          variant: "default",
        });
      }

    } catch (error) {
      console.error('Error updating cart:', error);
      toast({
        title: "Error",
        description: "Failed to update cart. Please try again.",
        variant: "destructive",
      });
    }
  };

  // Component to render product recommendations
  const ProductRecommendations = ({ products }: { products: ChatProduct[] }) => {
    if (!products || products.length === 0) return null;

    return (
      <div className="mt-3 space-y-2">
        <p className="text-xs font-medium text-muted-foreground mb-2">
          🌟 Recommended for you:
        </p>
        <div className="grid gap-2">
          {products.map((product) => (
            <Card key={product.id} className="p-3 bg-background/50 border border-border/50">
              <div className="flex items-start gap-3">
                <img
                  src={product.image_url}
                  alt={product.name}
                  className="w-12 h-12 rounded-md object-cover flex-shrink-0"
                  onError={(e) => {
                    e.currentTarget.src = 'https://images.pexels.com/photos/312418/pexels-photo-312418.jpeg';
                  }}
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <h4 className="font-medium text-sm text-foreground truncate">
                        {product.name}
                      </h4>
                      {product.description && (
                        <p className="text-xs text-muted-foreground mt-1 max-h-8 overflow-hidden">
                          {product.description.length > 80 
                            ? product.description.substring(0, 80) + "..." 
                            : product.description}
                        </p>
                      )}
                      <div className="flex items-center gap-2 mt-1">
                        <span className="font-semibold text-sm text-primary">
                          {formatINR(product.price)}
                        </span>
                        {product.unit_of_measure && (
                          <Badge variant="secondary" className="text-xs">
                            {product.unit_of_measure}
                          </Badge>
                        )}
                      </div>
                    </div>
                    {(() => {
                      const quantityInCart = getProductQuantityInCart(product.id);
                      if (quantityInCart > 0) {
                        return (
                          <div className="flex items-center gap-1">
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => handleUpdateCartQuantity(product, quantityInCart - 1)}
                              className="h-8 w-8 p-0"
                            >
                              <Minus className="h-3 w-3" />
                            </Button>
                            <span className="text-xs font-medium px-2 py-1 bg-secondary rounded">
                              {quantityInCart}
                            </span>
                            <Button
                              size="sm"
                              onClick={() => handleUpdateCartQuantity(product, quantityInCart + 1)}
                              className="h-8 w-8 p-0"
                            >
                              <Plus className="h-3 w-3" />
                            </Button>
                          </div>
                        );
                      } else {
                        return (
                          <Button
                            size="sm"
                            onClick={() => handleAddToCart(product)}
                            className="h-8 px-3 text-xs shrink-0"
                          >
                            <Plus className="h-3 w-3 mr-1" />
                            Add
                          </Button>
                        );
                      }
                    })()}
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    );
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-card border rounded-none shadow-2xl flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b coffee-gradient text-white rounded-none">
        <div className="flex items-center space-x-2">
          <Coffee className="h-5 w-5" />
          <div>
            <h3 className="font-semibold">BrewMaster Assistant</h3>
            <p className="text-xs opacity-90">Online now</p>
          </div>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={onToggle}
          className="text-white hover:bg-white/20"
        >
          <X className="h-4 w-4" />
        </Button>
      </div>

      {/* Messages */}
      <ScrollArea className="flex-1 p-4">
        <div className="space-y-4">
          {loading && !historyLoaded && (
            <div className="flex justify-center items-center py-8">
              <div className="flex items-center space-x-2 text-muted-foreground">
                <div className="w-4 h-4 rounded-full border-2 border-current border-t-transparent animate-spin"></div>
                <span className="text-sm">Loading chat history...</span>
              </div>
            </div>
          )}
          
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.isBot ? 'justify-start' : 'justify-end'}`}
            >
              <div
                className={`max-w-[85%] rounded-lg p-3 ${
                  message.isBot
                    ? 'bg-muted text-muted-foreground'
                    : 'bg-primary text-primary-foreground'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{message.text}</p>
                
                {/* Product Recommendations */}
                {message.isBot && message.products && message.products.length > 0 && (
                  <ProductRecommendations products={message.products} />
                )}
                
                <p className="text-xs opacity-70 mt-2">
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-muted text-muted-foreground rounded-lg p-3">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-current rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-current rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-current rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </ScrollArea>

      {/* Input */}
      <div className="p-4 border-t">
        <div className="flex space-x-2">
          <Input
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={!sessionId ? "Initializing chat..." : "Ask me anything about our coffee..."}
            className="flex-1"
            disabled={!sessionId || loading}
          />
          <Button 
            onClick={handleSendMessage} 
            size="sm" 
            className="px-3"
            disabled={!sessionId || loading || !inputMessage.trim()}
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;