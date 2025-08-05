import { Coffee } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';

const OurStory = () => {
  return (
    <div className="min-h-screen bg-background py-12">
      <div className="container mx-auto px-4 max-w-3xl">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <Coffee className="mx-auto h-12 w-12 text-primary mb-4" />
          <h1 className="text-4xl font-bold mb-4">Our Story</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Welcome to BrewMaster, where every cup is a journey. Discover how our passion for coffee, quality, and community has shaped our story.
          </p>
        </div>

        {/* History Section */}
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-2">A Journey Rooted in Passion</h2>
          <p className="text-muted-foreground mb-4">
            BrewMaster began as a small neighborhood café with a big dream: to bring world-class coffee experiences to our community. From our humble beginnings, we have grown into a beloved destination for coffee lovers, known for our signature blends, artisanal single origins, and warm, welcoming atmosphere.
          </p>
          <p className="text-muted-foreground">
            Our founders, inspired by travels to coffee farms around the globe, set out to create a space where every cup tells a story—of quality, sustainability, and connection.
          </p>
        </section>

        {/* Mission & Values Section */}
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-2">Our Mission</h2>
          <p className="text-muted-foreground mb-4">
            We believe coffee is more than a beverage—it's a bridge between people, cultures, and ideas. Our mission is to craft exceptional coffee while fostering a sense of belonging and community.
          </p>
          <ul className="list-disc list-inside text-muted-foreground mb-4">
            <li>Source ethically and support sustainable farming</li>
            <li>Roast and brew with care and expertise</li>
            <li>Welcome everyone with warmth and respect</li>
            <li>Give back to our local and global communities</li>
          </ul>
        </section>

        {/* Quality & Community Section */}
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-2">Quality & Community</h2>
          <p className="text-muted-foreground mb-4">
            Every cup at BrewMaster is a testament to our commitment to quality. We partner with passionate farmers, roast in small batches, and train our baristas to the highest standards. But what truly sets us apart is our community—our guests, team, and partners who inspire us every day.
          </p>
        </section>

        <div className="text-center mt-12">
          <Link to="/">
            <Button size="lg" className="bg-primary text-white px-8">Back to Home</Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default OurStory; 