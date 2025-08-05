
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, Star } from 'lucide-react';
import { ExtendedProduct } from '@/types/product';
import { formatINR } from '@/lib/utils';

interface ProductDetailHeaderProps {
  product: ExtendedProduct;
}

const ProductDetailHeader = ({ product }: ProductDetailHeaderProps) => {
  return (
    <>
      {/* Back button */}
      <Link to="/" className="inline-flex items-center space-x-2 text-muted-foreground hover:text-foreground mb-6">
        <ArrowLeft className="h-4 w-4" />
        <span>Back to Menu</span>
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Product Image */}
        <div className="space-y-4">
          <div className="relative overflow-hidden rounded-lg">
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-96 object-cover"
            />
            {product.isPopular && (
              <Badge className="absolute top-4 left-4 bg-accent text-accent-foreground">
                Popular Choice
              </Badge>
            )}
          </div>
        </div>

        {/* Product Details */}
        <div className="space-y-6">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <Badge variant="secondary">{product.category}</Badge>
              <div className="flex items-center space-x-1">
                <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                <span className="text-sm font-medium">{product.rating}</span>
              </div>
            </div>
            
            <h1 className="text-3xl font-bold mb-4">{product.name}</h1>
            <p className="text-lg text-muted-foreground mb-4">{product.description}</p>
            <p className="text-muted-foreground leading-relaxed mb-4">{product.fullDescription}</p>
            
            {/* Price Display */}
            <div className="flex items-center space-x-2">
              <span className="text-3xl font-bold text-primary">
                {formatINR(product.price)}
              </span>
              <span className="text-sm text-muted-foreground">(Medium size)</span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ProductDetailHeader;
