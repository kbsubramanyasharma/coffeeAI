import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Star, Plus, ShoppingCart } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Tooltip, TooltipTrigger, TooltipContent } from '@/components/ui/tooltip';
import { useToast } from '@/hooks/use-toast';
import { formatINR } from '@/lib/utils';

export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  image: string;
  rating: number;
  category: string;
  isPopular?: boolean;
  allergens?: string[];
  ingredients?: string[];
}

interface ProductCardProps {
  product: Product;
  onAddToCart: (product: Product) => void;
  isLoggedIn: boolean;
}

const ProductCard = ({ product, onAddToCart, isLoggedIn }: ProductCardProps) => {
  const { toast } = useToast();

  const handleAddToCart = () => {
    console.log('Add to Cart button clicked', product);
    if (!isLoggedIn) {
      toast({
        title: "Login Required",
        description: "Please log in to add items to your cart.",
        variant: "destructive",
      });
      return;
    }
    console.log('Calling onAddToCart from ProductCard', product);
    onAddToCart(product);
  };

  return (
    <Card className="group hover:shadow-lg transition-all duration-300 hover:-translate-y-1 bg-card border-border">
      <div className="relative overflow-hidden rounded-t-lg">
        <img
          src={product.image}
          alt={product.name}
          className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
        />
        {product.isPopular && (
          <Badge className="absolute top-2 left-2 bg-accent text-accent-foreground">
            Popular
          </Badge>
        )}
        <div className="absolute top-2 right-2 flex items-center space-x-1 bg-black/70 text-white px-2 py-1 rounded-full text-xs">
          <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
          <span>{product.rating}</span>
        </div>
      </div>
      
      <CardContent className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="font-semibold text-lg group-hover:text-primary transition-colors">
            {product.name}
          </h3>
          <span className="text-lg font-bold text-primary">
            {formatINR(product.price)}
          </span>
        </div>
        
        <p className="text-muted-foreground text-sm mb-3 line-clamp-2">
          {product.description}
        </p>
        
        <div className="flex items-center justify-between">
          <Badge variant="secondary" className="text-xs">
            {product.category}
          </Badge>
          
          {product.allergens && product.allergens.length > 0 && (
            <span className="text-xs text-muted-foreground">
              Contains allergens
            </span>
          )}
        </div>
      </CardContent>
      
      <CardFooter className="p-4 pt-0 flex space-x-2">
        <Link to={`/product/${product.id}`} className="flex-1">
          <Button variant="outline" className="w-full">
            View Details
          </Button>
        </Link>
        
        <Tooltip>
          <TooltipTrigger asChild>
            <span>
              <Button
                onClick={handleAddToCart}
                className="flex items-center space-x-1 bg-primary hover:bg-primary/90"
              >
                <ShoppingCart className="h-4 w-4" />
                <span>Add</span>
              </Button>
            </span>
          </TooltipTrigger>
        </Tooltip>
      </CardFooter>
    </Card>
  );
};

export default ProductCard;
