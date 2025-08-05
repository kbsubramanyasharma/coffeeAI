
import { Product } from '@/components/ProductCard';

export interface ExtendedProduct extends Product {
  fullDescription: string;
  nutritionInfo: {
    calories: number;
    caffeine: string;
    fat: string;
    carbs: string;
    protein: string;
    sugar: string;
  };
  brewingNotes?: string;
}

export interface SizeOption {
  name: string;
  price: number;
}
