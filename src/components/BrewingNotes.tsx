
import { Card, CardContent } from '@/components/ui/card';
import { Coffee } from 'lucide-react';
import { ExtendedProduct } from '@/types/product';

interface BrewingNotesProps {
  product: ExtendedProduct;
}

const BrewingNotes = ({ product }: BrewingNotesProps) => {
  if (!product.brewingNotes) {
    return null;
  }

  return (
    <Card className="mt-6">
      <CardContent className="p-6">
        <h3 className="font-semibold mb-3 flex items-center space-x-2">
          <Coffee className="h-5 w-5 text-primary" />
          <span>Brewing Notes</span>
        </h3>
        <p className="text-muted-foreground">{product.brewingNotes}</p>
      </CardContent>
    </Card>
  );
};

export default BrewingNotes;
