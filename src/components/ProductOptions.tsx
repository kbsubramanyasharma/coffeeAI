import { Button } from '@/components/ui/button';
import { ShoppingCart } from 'lucide-react';
import { ExtendedProduct, SizeOption } from '@/types/product';
import { Tooltip, TooltipTrigger, TooltipContent } from '@/components/ui/tooltip';
import { formatINR } from '@/lib/utils';

interface ProductOptionsProps {
  product: ExtendedProduct;
  sizes: SizeOption[];
  size: string;
  setSize: (size: string) => void;
  quantity: number;
  setQuantity: (quantity: number) => void;
  getCurrentPrice: () => number;
  onAddToCart: () => void;
  isLoggedIn: boolean;
}

const ProductOptions = ({
  product,
  sizes,
  size,
  setSize,
  quantity,
  setQuantity,
  getCurrentPrice,
  onAddToCart,
  isLoggedIn
}: ProductOptionsProps) => {
  return (
    <div className="space-y-6">
      {/* Size Selection */}
      <div>
        <h3 className="font-semibold mb-3">Choose Size</h3>
        <div className="grid grid-cols-3 gap-2">
          {sizes.map((sizeOption) => (
            <Button
              key={sizeOption.name}
              variant={size === sizeOption.name ? "default" : "outline"}
              onClick={() => setSize(sizeOption.name)}
              className="flex flex-col py-4 h-auto"
            >
              <span className="font-medium">{sizeOption.name}</span>
              <span className="text-sm">{formatINR(sizeOption.price)}</span>
            </Button>
          ))}
        </div>
      </div>

      {/* Quantity */}
      <div>
        <h3 className="font-semibold mb-3">Quantity</h3>
        <div className="flex items-center space-x-3">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setQuantity(Math.max(1, quantity - 1))}
          >
            -
          </Button>
          <span className="font-medium text-lg w-8 text-center">{quantity}</span>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setQuantity(quantity + 1)}
          >
            +
          </Button>
        </div>
      </div>

      {/* Price and Add to Cart */}
      <div className="bg-muted/30 p-6 rounded-lg">
        <div className="flex items-center justify-between mb-4">
          <span className="text-lg font-medium">Total:</span>
          <span className="text-2xl font-bold text-primary">
            {formatINR(getCurrentPrice())}
          </span>
        </div>
        <Tooltip>
          <TooltipTrigger asChild>
            <span>
              <Button
                onClick={onAddToCart}
                className="w-full flex items-center justify-center space-x-2"
                size="lg"
                disabled={!isLoggedIn}
              >
                <ShoppingCart className="h-5 w-5" />
                <span>Add to Cart</span>
              </Button>
            </span>
          </TooltipTrigger>
        </Tooltip>
      </div>
    </div>
  );
};

export default ProductOptions;
