import { Navbar } from "@/components/site/Navbar";
import { Hero } from "@/components/site/Hero";
import { Categories } from "@/components/site/Categories";
import { SnippetsGrid } from "@/components/site/SnippetsGrid";
import { Stats } from "@/components/site/Stats";
import { CTA } from "@/components/site/CTA";
import { Footer } from "@/components/site/Footer";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main>
        <Hero />
        <Stats />
        <Categories />
        <SnippetsGrid />
        <CTA />
      </main>
      <Footer />
    </div>
  );
};

export default Index;
