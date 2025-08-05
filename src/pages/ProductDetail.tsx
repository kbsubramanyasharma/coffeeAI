import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Product } from '@/components/ProductCard';
import { ExtendedProduct, SizeOption } from '@/types/product';
import ProductDetailHeader from '@/components/ProductDetailHeader';
import ProductOptions from '@/components/ProductOptions';
import ProductInfoCards from '@/components/ProductInfoCards';
import BrewingNotes from '@/components/BrewingNotes';
import { isLoggedIn } from '@/lib/utils';
import { apiService, ApiProduct } from '@/services/api';
import { formatINR } from '@/lib/utils';
import { Coffee, ArrowLeft } from 'lucide-react';

interface ProductDetailProps {
  onAddToCart: (product: Product) => void;
}

const ProductDetail = ({ onAddToCart }: ProductDetailProps) => {
  const { id } = useParams<{ id: string }>();
  const [quantity, setQuantity] = useState(1);
  const [size, setSize] = useState('Medium');
  const [product, setProduct] = useState<ExtendedProduct | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProduct = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError('');
        
        const apiProduct: ApiProduct = await apiService.getProductById(id);
        
        // Convert ApiProduct to ExtendedProduct
        const extendedProduct: ExtendedProduct = {
          id: apiProduct.id.toString(),
          name: apiProduct.name,
          description: apiProduct.description,
          fullDescription: apiProduct.full_description || apiProduct.description,
          price: apiProduct.retail_price || apiProduct.price || 0, // Price is already in INR from database
          image: apiProduct.image_url || apiProduct.image || '/placeholder.svg',
          rating: apiProduct.rating || 4.5,
          category: apiProduct.category?.name || 'Coffee',
          isPopular: apiProduct.is_popular || false,
          allergens: apiProduct.allergens || [],
          ingredients: apiProduct.ingredients || [],
          nutritionInfo: apiProduct.nutrition_info || {
            calories: 5,
            caffeine: '95mg',
            fat: '0g',
            carbs: '1g',
            protein: '0g',
            sugar: '0g'
          },
          brewingNotes: apiProduct.brewing_notes || null
        };
        
        setProduct(extendedProduct);
      } catch (error) {
        console.error('Error fetching product:', error);
        setError('Failed to load product details');
      } finally {
        setLoading(false);
      }
    };
    
    fetchProduct();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading product details...</p>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Coffee className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
          <h1 className="text-2xl font-bold mb-4">Product Not Found</h1>
          <p className="text-muted-foreground mb-6">{error || 'The product you are looking for does not exist.'}</p>
          <Link to="/">
            <Button className="flex items-center gap-2">
              <ArrowLeft className="h-4 w-4" />
              Return Home
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  // Generate size options based on product price
  const basePrice = product.price;
  const sizes: SizeOption[] = [
    { name: 'Small', price: Math.round(basePrice * 0.8) },
    { name: 'Medium', price: basePrice },
    { name: 'Large', price: Math.round(basePrice * 1.3) }
    ];

  const getCurrentPrice = () => {
    const selectedSize = sizes.find(s => s.name === size);
    return selectedSize ? selectedSize.price * quantity : product.price * quantity;
  };

  const handleAddToCart = () => {
    const productWithOptions = {
      ...product,
      price: getCurrentPrice() / quantity,
      selectedSize: size,
      quantity
    };
    
    for (let i = 0; i < quantity; i++) {
      onAddToCart(productWithOptions);
    }
  };

  return (
    <div className="min-h-screen bg-background py-8">
      <div className="container mx-auto px-4">
        <div className="mb-6">
          {/*<Link to="/" className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
            <ArrowLeft className="h-4 w-4" />
            Back to Products
          </Link>*/}
        </div>
        
        <ProductDetailHeader product={product} />
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div></div> {/* Empty div to maintain layout */}
          <ProductOptions
            product={product}
            sizes={sizes}
            size={size}
            setSize={setSize}
            quantity={quantity}
            setQuantity={setQuantity}
            getCurrentPrice={getCurrentPrice}
            onAddToCart={handleAddToCart}
            isLoggedIn={isLoggedIn()}
          />
        </div>

        <ProductInfoCards product={product} />
        <BrewingNotes product={product} />
      </div>
    </div>
  );
};

export default ProductDetail;
