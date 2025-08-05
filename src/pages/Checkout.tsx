import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Textarea } from '@/components/ui/textarea';
import { CreditCard, Truck } from 'lucide-react';
import { Product } from '@/components/ProductCard';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn, formatINR } from '@/lib/utils';
import { useToast } from '@/hooks/use-toast';
import { apiService } from '@/services/api';
// import { useAuth } from '@/hooks/use-auth'; // Example: Import your auth hook

interface CartItem extends Product {
  cartId: string;
  selectedSize?: string;
  customizations?: string[];
}

interface CheckoutProps {
  cartItems: CartItem[];
  onClearCart: () => void;
}

interface CheckoutForm {
  // Shipping Information
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
  
  // Payment Information
  paymentMethod: 'card' | 'paypal' | 'cash';
  
  // Order Notes
  notes: string;
}

const Checkout = ({ cartItems, onClearCart }: CheckoutProps) => {
  const [form, setForm] = useState<CheckoutForm>({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zipCode: '',
    country: 'United States', // Or your default country
    paymentMethod: 'card',
    notes: '',
  });

  const [isProcessing, setIsProcessing] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();
  // const { user } = useAuth(); // Example: Get the authenticated user object

  // Redirect if not logged in or cart is empty
  useEffect(() => {
    console.log('Checkout useEffect - cartItems:', cartItems);
    console.log('Checkout useEffect - isLoggedIn:', isLoggedIn());
    
    if (!isLoggedIn()) {
      console.log('Not logged in, redirecting to login');
      navigate('/login');
    } else if (cartItems.length === 0) {
      console.log('Cart is empty, redirecting to cart');
      navigate('/cart');
    }
  }, [navigate, cartItems]);

  const handleInputChange = (field: keyof CheckoutForm, value: string) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  // Group cart items by product ID and sum quantities
  const productMap = new Map<number, CartItem & { quantity: number }>();
  cartItems.forEach(item => {
    if (productMap.has(item.id)) {
      productMap.get(item.id)!.quantity += 1;
    } else {
      productMap.set(item.id, { ...item, quantity: 1 });
    }
  });
  const uniqueItems = Array.from(productMap.values());

  // Calculate subtotal, tax, delivery fee, and total
  const subtotalINR = uniqueItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  const tax = subtotalINR * 0.18;
  const deliveryFee = subtotalINR > 500 ? 0 : 49;
  const totalPayable = subtotalINR + tax + deliveryFee;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Checkout form submitted');
    console.log('Form data:', form);
    console.log('Cart items:', cartItems);
    
    setIsProcessing(true);
    
    // NOTE: You need a way to get the logged-in user's ID and a session ID.
    // This often comes from an authentication context or a global state.
    const MOCK_USER_ID = 1; // Replace with actual user.id
    const MOCK_SESSION_ID = 'session_xyz123'; // Replace with actual session ID

    try {
      // 1. Build orderData to match backend expectations
      const orderData = {
        // --- Required IDs ---
        user_id: MOCK_USER_ID, 
        session_id: MOCK_SESSION_ID,

        // --- Financials ---
        total_amount: subtotalINR,
        tax_amount: tax,
        discount_amount: 0,
        final_amount: totalPayable,

        // --- Payment & Notes ---
        payment_method: form.paymentMethod,
        notes: form.notes,
        
        // --- Addresses ---
        shipping_address: {
          first_name: form.firstName,
          last_name: form.lastName,
          address: form.address,
          city: form.city,
          state: form.state,
          zip_code: form.zipCode,
          country: form.country,
          phone: form.phone
        },
        // Assuming billing is the same as shipping, as it's not collected separately
        billing_address: {
          first_name: form.firstName,
          last_name: form.lastName,
          address: form.address,
          city: form.city,
          state: form.state,
          zip_code: form.zipCode,
          country: form.country,
          phone: form.phone
        },
      };

      console.log('orderData being sent:', orderData);

      const token = localStorage.getItem('access_token') || localStorage.getItem('token');
      if (!token) throw new Error('User not authenticated');

      // 2. Call backend to place order
      await apiService.checkout(orderData, token);

      // 3. On success, clear cart and show message
      onClearCart();
      toast({
        title: "Order Placed Successfully!",
        description: "Thank you for your order. You will receive a confirmation email shortly.",
      });
      navigate('/');

    } catch (error) {
      console.error('Order error:', error);
      toast({
        title: "Order Failed",
        description: "There was an error processing your order. Please check the details and try again.",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-background py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">Checkout</h1>
            <p className="text-muted-foreground">Complete your order</p>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Checkout Form */}
              <div className="lg:col-span-2 space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Truck className="h-5 w-5" />
                      <span>Shipping Information</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="firstName">First Name *</Label>
                        <Input id="firstName" value={form.firstName} onChange={(e) => handleInputChange('firstName', e.target.value)} required />
                      </div>
                      <div>
                        <Label htmlFor="lastName">Last Name *</Label>
                        <Input id="lastName" value={form.lastName} onChange={(e) => handleInputChange('lastName', e.target.value)} required />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="email">Email *</Label>
                        <Input id="email" type="email" value={form.email} onChange={(e) => handleInputChange('email', e.target.value)} required />
                      </div>
                      <div>
                        <Label htmlFor="phone">Phone *</Label>
                        <Input id="phone" type="tel" value={form.phone} onChange={(e) => handleInputChange('phone', e.target.value)} required />
                      </div>
                    </div>
                    
                    <div>
                      <Label htmlFor="address">Address *</Label>
                      <Input id="address" value={form.address} onChange={(e) => handleInputChange('address', e.target.value)} required />
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <Label htmlFor="city">City *</Label>
                        <Input id="city" value={form.city} onChange={(e) => handleInputChange('city', e.target.value)} required />
                      </div>
                      <div>
                        <Label htmlFor="state">State *</Label>
                        <Input id="state" value={form.state} onChange={(e) => handleInputChange('state', e.target.value)} required />
                      </div>
                      <div>
                        <Label htmlFor="zipCode">ZIP Code *</Label>
                        <Input id="zipCode" value={form.zipCode} onChange={(e) => handleInputChange('zipCode', e.target.value)} required />
                      </div>
                    </div>
                    
                    <div>
                      <Label htmlFor="country">Country *</Label>
                      <Input id="country" value={form.country} onChange={(e) => handleInputChange('country', e.target.value)} required />
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <CreditCard className="h-5 w-5" />
                      <span>Payment Method</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <RadioGroup value={form.paymentMethod} onValueChange={(value) => handleInputChange('paymentMethod', value as 'card' | 'paypal' | 'cash')}>
                        <div className="flex items-center space-x-2"><RadioGroupItem value="card" id="card" /><Label htmlFor="card">Credit/Debit Card</Label></div>
                        <div className="flex items-center space-x-2"><RadioGroupItem value="paypal" id="paypal" /><Label htmlFor="paypal">PayPal</Label></div>
                        <div className="flex items-center space-x-2"><RadioGroupItem value="cash" id="cash" /><Label htmlFor="cash">Cash on Delivery</Label></div>
                    </RadioGroup>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardHeader><CardTitle>Order Notes</CardTitle></CardHeader>
                  <CardContent>
                    <Textarea placeholder="Any special instructions for your order..." value={form.notes} onChange={(e) => handleInputChange('notes', e.target.value)} rows={3} />
                  </CardContent>
                </Card>
              </div>

              {/* Order Summary */}
              <div className="lg:col-span-1">
                <Card className="sticky top-4">
                  <CardHeader>
                    <CardTitle>Order Summary</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-3">
                      {uniqueItems.map((item) => (
                        <div key={item.cartId} className="flex items-center space-x-3">
                          <img src={item.image} alt={item.name} className="w-12 h-12 object-cover rounded" />
                          <div className="flex-1">
                            <p className="font-medium text-sm">{item.name}</p>
                            <p className="text-xs text-muted-foreground">
                              {/* CORRECTED: Use item.quantity directly */}
                              Qty: {item.quantity}
                            </p>
                          </div>
                          <p className="font-medium text-sm">
                            {formatINR(item.price * item.quantity)}
                          </p>
                        </div>
                      ))}
                    </div>

                    <Separator />

                    <div className="space-y-2">
                      <div className="flex justify-between text-sm"><span>Subtotal</span><span>{formatINR(subtotalINR)}</span></div>
                      <div className="flex justify-between text-sm"><span>GST (18%)</span><span>{formatINR(tax)}</span></div>
                      <div className="flex justify-between text-sm"><span>Delivery Fee</span><span>{deliveryFee === 0 ? 'Free' : formatINR(deliveryFee)}</span></div>
                      <Separator />
                      <div className="flex justify-between font-semibold"><span>Total Payable</span><span>{formatINR(totalPayable)}</span></div>
                    </div>

                    <Button type="submit" className="w-full" size="lg" disabled={isProcessing}>
                      {isProcessing ? 'Processing...' : `Place Order - ${formatINR(totalPayable)}`}
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Checkout;