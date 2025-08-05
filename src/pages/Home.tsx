import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import ProductCard, { Product } from '@/components/ProductCard';
import { Search, Coffee, Star, Zap } from 'lucide-react';
import { isLoggedIn } from '@/lib/utils';
import { Link } from 'react-router-dom';
import { apiService, ApiProduct } from '@/services/api';

// Fallback products in case API fails
const fallbackProducts: Product[] = [
	{
		id: '1',
		name: 'BrewMaster Signature Blend',
		description:
			'Our signature dark roast with notes of chocolate and caramel, perfect for any time of day.',
		price: 1503, // Updated to INR price
		image:
			'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&h=300&fit=crop&auto=format',
		rating: 4.8,
		category: 'Signature',
		isPopular: true,
		allergens: ['milk'],
		ingredients: ['Arabica coffee beans', 'steamed milk', 'vanilla syrup'],
	},
	{
		id: '2',
		name: 'Caramel Macchiato',
		description:
			'Rich espresso with steamed milk, vanilla, and caramel drizzle for the perfect sweet indulgence.',
		price: 313, // Updated to INR price
		image:
			'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop&auto=format',
		rating: 4.7,
		category: 'Specialty',
		isPopular: true,
		allergens: ['milk'],
		ingredients: [
			'Espresso',
			'steamed milk',
			'vanilla syrup',
			'caramel sauce',
		],
	},
];

interface HomeProps {
	onAddToCart: (product: Product) => void;
}

const Home = ({ onAddToCart }: HomeProps) => {
	const [searchQuery, setSearchQuery] = useState('');
	const [selectedCategory, setSelectedCategory] = useState('All');
	const [products, setProducts] = useState<Product[]>([]);
	const [categories, setCategories] = useState<string[]>(['All']);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState('');
	const productGridRef = useRef<HTMLDivElement>(null);

	useEffect(() => {
		const fetchProducts = async () => {
			try {
				setLoading(true);
				setError('');

				// Fetch all products (increase limit to get all 88 products)
				const response = await apiService.getProducts({ limit: 100 });

				// Map ApiProduct to ProductCard's Product type
				const mappedProducts = response.products.map((apiProduct: ApiProduct) => ({
					id: apiProduct.id.toString(),
					name: apiProduct.name,
					description: apiProduct.full_description || apiProduct.description,
					price: apiProduct.retail_price || apiProduct.price || 0, // Price is already in INR from database
					image: apiProduct.image_url || apiProduct.image || '/placeholder.svg',
					rating: apiProduct.rating || 4.5,
					category: apiProduct.category?.name || 'Coffee',
					isPopular: apiProduct.is_popular || false,
					allergens: apiProduct.allergens || [],
					ingredients: apiProduct.ingredients || [],
					// Add additional fields if your Product interface supports them
					nutritionInfo: apiProduct.nutrition_info,
					brewingNotes: apiProduct.brewing_notes,
					isActive: apiProduct.is_active,
				}));

				setProducts(mappedProducts);

				// Extract unique categories from products
				const uniqueCategories = [
					'All',
					...Array.from(new Set(mappedProducts.map((p) => p.category))),
				];
				setCategories(uniqueCategories);
			} catch (error) {
				console.error('Error fetching products:', error);
				setError('Failed to load products');
				setProducts(fallbackProducts);
			} finally {
				setLoading(false);
			}
		};

		fetchProducts();
	}, []);

	const handleExploreMenu = () => {
		productGridRef.current?.scrollIntoView({ behavior: 'smooth' });
	};

	const filteredProducts = products.filter((product) => {
		const matchesSearch =
			product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
			product.description.toLowerCase().includes(searchQuery.toLowerCase());
		const matchesCategory =
			selectedCategory === 'All' || product.category === selectedCategory;
		return matchesSearch && matchesCategory;
	});

	return (
		<div className="min-h-screen bg-background">
			{/* Hero Section */}
			<section className="relative coffee-gradient text-white py-20 overflow-hidden">
				<div className="absolute inset-0 bg-black/20"></div>
				<div className="container mx-auto px-4 relative z-10">

					<div className="max-w-3xl mx-auto text-center">
						<div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full mb-6">
							<Coffee className="h-5 w-5" />
							<span className="text-sm font-medium">
								Premium Coffee Experience
							</span>
						</div>

						<h1 className="text-5xl md:text-6xl font-bold mb-6">
							Welcome to{' '}
							<span className="bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">
								Coffee Corner
							</span>
						</h1>

						<p className="text-xl mb-8 text-white/90">
							Discover exceptional coffee crafted with passion. From our
							signature blends to artisanal single origins, every cup tells a
							story of quality and care.
						</p>

						<div className="flex flex-col sm:flex-row gap-4 justify-center">
							<Button
								size="lg"
								className="bg-white text-gray-900 hover:bg-gray-100 px-8"
								onClick={handleExploreMenu}
							>
								Explore Menu
							</Button>
							<Button
								size="lg"
								variant="outline"
								className="border-black text-black hover:bg-white hover:text-gray-900"
								asChild
							>
								<Link to="/our-story">Our Story</Link>
							</Button>
						</div>
					</div>
				</div>

				{/* Floating coffee beans animation */}
				<div className="absolute top-20 left-10 animate-float">
					<Coffee className="h-8 w-8 text-white/30" />
				</div>
				<div className="absolute top-32 right-20 animate-float" style={{ animationDelay: '1s' }}>
					<Coffee className="h-6 w-6 text-white/20" />
				</div>
				<div className="absolute bottom-20 left-1/4 animate-float" style={{ animationDelay: '2s' }}>
					<Coffee className="h-10 w-10 text-white/25" />
				</div>
			</section>

			{/* Featured Stats */}
			<section className="py-12 bg-muted/30">
				<div className="container mx-auto px-4">
					<div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
						<div className="flex flex-col items-center">
							<div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
								<Star className="h-8 w-8 text-primary" />
							</div>
							<h3 className="text-2xl font-bold text-primary">4.8/5</h3>
							<p className="text-muted-foreground">Average Rating</p>
						</div>

						<div className="flex flex-col items-center">
							<div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mb-4">
								<Coffee className="h-8 w-8 text-accent" />
							</div>
							<h3 className="text-2xl font-bold text-accent">{products.length}+</h3>
							<p className="text-muted-foreground">Coffee Varieties</p>
						</div>

						<div className="flex flex-col items-center">
							<div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
								<Zap className="h-8 w-8 text-primary" />
							</div>
							<h3 className="text-2xl font-bold text-primary">15 min</h3>
							<p className="text-muted-foreground">Average Prep Time</p>
						</div>
					</div>
				</div>
			</section>

			{/* Search and Filter Section */}
			<section className="py-8 bg-background">
				<div className="container mx-auto px-4">
					<div className="max-w-4xl mx-auto">
						<div className="flex flex-col md:flex-row gap-4 mb-8">
							<div className="flex-1 relative">
								<Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
								<Input
									placeholder="Search for your perfect coffee..."
									value={searchQuery}
									onChange={(e) => setSearchQuery(e.target.value)}
									className="pl-10"
								/>
							</div>
						</div>
						<div className="flex flex-wrap gap-2 mb-8">
							{categories.map((category) => (
								<Button
									key={category}
									variant={
										selectedCategory === category ? 'default' : 'outline'
									}
									size="sm"
									onClick={() => setSelectedCategory(category)}
									className="text-sm"
								>
									{category}
								</Button>
							))}
						</div>
					</div>
				</div>
			</section>

			{/* Products Section */}
			<section className="py-12" ref={productGridRef}>
				<div className="container mx-auto px-4">
					<div className="text-center mb-12">
						<h2 className="text-3xl md:text-4xl font-bold mb-4">
							Our Coffee Collection
						</h2>
						<p className="text-lg text-muted-foreground max-w-2xl mx-auto">
							Discover our carefully curated selection of {products.length} premium
							coffee products, each crafted with passion and expertise.
						</p>
						{selectedCategory !== 'All' && (
							<p className="text-sm text-muted-foreground mt-2">
								Showing {filteredProducts.length} products in {selectedCategory}
							</p>
						)}
					</div>

					{loading && (
						<div className="text-center py-12">
							<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
							<p className="text-muted-foreground">Loading products...</p>
						</div>
					)}

					{error && !loading && (
						<div className="text-center py-12">
							<Coffee className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
							<h3 className="text-xl font-semibold mb-2">
								Error loading products
							</h3>
							<p className="text-muted-foreground">{error}</p>
						</div>
					)}

					{!loading && !error && (
						<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
							{filteredProducts.map((product) => (
								<ProductCard
									key={product.id}
									product={product}
									onAddToCart={onAddToCart}
									isLoggedIn={isLoggedIn()}
								/>
							))}
						</div>
					)}

					{!loading && !error && filteredProducts.length === 0 && (
						<div className="text-center py-12">
							<Coffee className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
							<h3 className="text-xl font-semibold mb-2">No products found</h3>
							<p className="text-muted-foreground">
								Try adjusting your search or filter criteria.
							</p>
						</div>
					)}
				</div>
			</section>
		</div>
	);
};

export default Home;
