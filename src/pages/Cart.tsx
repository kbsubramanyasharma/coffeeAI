import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { ShoppingCart, Plus, Minus, X, Coffee, CreditCard } from 'lucide-react';
import { Product } from '@/components/ProductCard';
import { Link, useNavigate } from 'react-router-dom';
import { isLoggedIn, formatINR } from '@/lib/utils';
import { Label } from '@/components/ui/label';

interface CartItem extends Product {
  cartId: string;
  selectedSize?: string;
  customizations?: string[];
  quantity: number;
}

interface CartProps {
  cartItems: CartItem[];
  onUpdateQuantity: (cartId: string, newQuantity: number) => void;
  onRemoveItem: (cartId: string) => void;
  onClearCart: () => void;
}

const Cart = ({ cartItems, onUpdateQuantity, onRemoveItem, onClearCart }: CartProps) => {
  const [promoCode, setPromoCode] = useState('');
  const [discount, setDiscount] = useState(0);
  const navigate = useNavigate();

  // Redirect to login if not logged in
  if (!isLoggedIn()) {
    navigate('/login');
    return null;
  }

  // Calculate subtotal, GST, delivery fee, and total
  const subtotalINR = cartItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  const tax = subtotalINR * 0.18;
  const deliveryFee = subtotalINR > 500 ? 0 : 49;
  const totalPayable = subtotalINR + tax + deliveryFee - discount;

  const handleApplyPromo = () => {
    // Simple promo code logic
    if (promoCode.toLowerCase() === 'brew10') {
      setDiscount(subtotalINR * 0.1);
    } else if (promoCode.toLowerCase() === 'first20') {
      setDiscount(Math.min(subtotalINR * 0.2, 10));
    } else {
      setDiscount(0);
    }
  };

  if (cartItems.length === 0) {
    return (
      <div className="min-h-screen bg-background py-8">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto text-center py-16">
            <ShoppingCart className="h-24 w-24 text-muted-foreground mx-auto mb-6" />
            <h1 className="text-3xl font-bold mb-4">Your Cart is Empty</h1>
            <p className="text-muted-foreground mb-8">
              Looks like you haven't added any coffee to your cart yet. 
              Discover our amazing selection of premium coffee!
            </p>
            <Link to="/">
              <Button size="lg" className="flex items-center space-x-2">
                <Coffee className="h-5 w-5" />
                <span>Browse Coffee</span>
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-3xl font-bold">Shopping Cart</h1>
            <Badge variant="secondary" className="text-sm">
              {cartItems.length} item{cartItems.length !== 1 ? 's' : ''}
            </Badge>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Cart Items */}
            <div className="lg:col-span-2 space-y-4">
              {cartItems.map((item) => (
                <Card key={item.cartId}>
                  <CardContent className="p-6">
                    <div className="flex items-start space-x-4">
                      <img
                        src={item.image}
                        alt={item.name}
                        className="w-20 h-20 object-cover rounded-lg"
                      />
                      
                      <div className="flex-1">
                        <div className="flex items-start justify-between">
                          <div>
                            <h3 className="font-semibold text-lg">{item.name}</h3>
                            <p className="text-muted-foreground text-sm mb-2">
                              {item.description}
                            </p>
                            
                            <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                              {item.selectedSize && (
                                <span>Size: {item.selectedSize}</span>
                              )}
                              <Badge variant="outline" className="text-xs">
                                {item.category}
                              </Badge>
                            </div>
                          </div>
                          
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => onRemoveItem(item.cartId)}
                            className="text-muted-foreground hover:text-destructive"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                        
                        <div className="flex items-center justify-between mt-4">
                          <div className="flex items-center space-x-3">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => onUpdateQuantity(item.cartId, item.quantity - 1)}
                            >
                              <Minus className="h-3 w-3" />
                            </Button>
                            
                            <span className="font-medium w-8 text-center">{item.quantity}</span>
                            
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => onUpdateQuantity(item.cartId, item.quantity + 1)}
                            >
                              <Plus className="h-3 w-3" />
                            </Button>
                          </div>
                          
                          <div className="text-right">
                            <p className="font-semibold text-lg">
                              {formatINR(item.price * item.quantity)}
                            </p>
                            <p className="text-sm text-muted-foreground">
                              {formatINR(item.price)} each
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
              
              <div className="flex justify-between items-center pt-4">
                <Link to="/">
                  <Button variant="outline">Continue Shopping</Button>
                </Link>
                
                <Button 
                  variant="destructive" 
                  onClick={() => {
                    onClearCart();
                    navigate('/');
                  }}
                  className="text-sm"
                >
                  Clear Cart
                </Button>
              </div>
            </div>

            {/* Order Summary */}
            <div className="lg:col-span-1">
              <Card className="sticky top-4">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <CreditCard className="h-5 w-5" />
                    <span>Order Summary</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Cart Items Summary */}
                  <div className="space-y-2">
                    {cartItems.map((item) => (
                      <div key={item.cartId} className="flex justify-between text-sm">
                        <span className="flex-1 truncate">{item.name} × {item.quantity}</span>
                        <span className="font-medium">{formatINR(item.price * item.quantity)}</span>
                      </div>
                    ))}
                  </div>

                  <Separator />

                  {/* Totals */}
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Subtotal</span>
                      <span>{formatINR(subtotalINR)}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>GST (18%)</span>
                      <span>{formatINR(tax)}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Delivery Fee</span>
                      <span>{deliveryFee === 0 ? 'Free' : formatINR(deliveryFee)}</span>
                    </div>
                    <Separator />
                    <div className="flex justify-between font-semibold text-lg">
                      <span>Total Payable</span>
                      <span>{formatINR(totalPayable)}</span>
                    </div>
                  </div>

                  {/* Promo Code */}
                  <div className="space-y-2">
                    <Label htmlFor="promo">Promo Code</Label>
                    <div className="flex space-x-2">
                      <Input
                        id="promo"
                        placeholder="Enter code"
                        value={promoCode}
                        onChange={(e) => setPromoCode(e.target.value)}
                      />
                      <Button onClick={handleApplyPromo} variant="outline" size="sm">
                        Apply
                      </Button>
                    </div>
                    {discount > 0 && (
                      <p className="text-sm text-green-600">
                        Discount applied: -{new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(discount)}
                      </p>
                    )}
                  </div>

                  {/* Proceed to Checkout Button */}
                  <Button 
                    onClick={() => {
                      console.log('Proceed to Checkout clicked');
                      console.log('Current cart items:', cartItems);
                      navigate('/checkout');
                    }}
                    className="w-full"
                    size="lg"
                  >
                    Proceed to Checkout
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
