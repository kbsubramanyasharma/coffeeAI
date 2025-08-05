
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { AlertTriangle, Leaf, Award } from 'lucide-react';
import { ExtendedProduct } from '@/types/product';

interface ProductInfoCardsProps {
  product: ExtendedProduct;
}

const ProductInfoCards = ({ product }: ProductInfoCardsProps) => {
  return (
    <div className="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {/* Ingredients */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center space-x-2 mb-4">
            <Leaf className="h-5 w-5 text-green-600" />
            <h3 className="font-semibold">Ingredients</h3>
          </div>
          <ul className="space-y-2 text-sm text-muted-foreground">
            {product.ingredients.map((ingredient, index) => (
              <li key={index} className="flex items-center space-x-2">
                <span className="w-1.5 h-1.5 bg-primary rounded-full"></span>
                <span>{ingredient}</span>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      {/* Allergens */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center space-x-2 mb-4">
            <AlertTriangle className="h-5 w-5 text-orange-600" />
            <h3 className="font-semibold">Allergen Information</h3>
          </div>
          {product.allergens && product.allergens.length > 0 ? (
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground mb-2">Contains:</p>
              <div className="flex flex-wrap gap-2">
                {product.allergens.map((allergen, index) => (
                  <Badge key={index} variant="destructive" className="text-xs">
                    {allergen}
                  </Badge>
                ))}
              </div>
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No common allergens</p>
          )}
        </CardContent>
      </Card>

      {/* Nutrition */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center space-x-2 mb-4">
            <Award className="h-5 w-5 text-blue-600" />
            <h3 className="font-semibold">Nutrition Facts</h3>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Calories:</span>
              <span>{product.nutritionInfo.calories}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Caffeine:</span>
              <span>{product.nutritionInfo.caffeine}</span>
            </div>
            <Separator />
            <div className="flex justify-between">
              <span className="text-muted-foreground">Fat:</span>
              <span>{product.nutritionInfo.fat}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Carbs:</span>
              <span>{product.nutritionInfo.carbs}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Protein:</span>
              <span>{product.nutritionInfo.protein}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ProductInfoCards;
