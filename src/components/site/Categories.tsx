import { FileCode2, Palette, Braces } from "lucide-react";
import { useEffect, useState } from "react";
import { supabase } from "@/integrations/supabase/client";

const baseCats = [
  { name: "HTML", key: "HTML", icon: FileCode2, color: "bg-cta/10 text-cta" },
  { name: "CSS", key: "CSS", icon: Palette, color: "bg-primary-glow/15 text-primary-glow" },
  { name: "JavaScript", key: "JS", icon: Braces, color: "bg-secondary/30 text-primary" },
];

export const Categories = () => {
  const [counts, setCounts] = useState<Record<string, number>>({});

  useEffect(() => {
    (async () => {
      const { data } = await supabase
        .from("snippets")
        .select("language")
        .eq("published", true);
      const c: Record<string, number> = {};
      (data || []).forEach((r) => {
        c[r.language] = (c[r.language] || 0) + 1;
      });
      setCounts(c);
    })();
  }, []);

  return (
    <section id="categories" className="py-20 bg-muted/40">
      <div className="container">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <p className="text-sm font-bold text-cta mb-2">التصنيفات</p>
          <h2 className="text-3xl md:text-4xl font-black text-primary mb-3">تصفّح الأكواد حسب اللغة</h2>
          <p className="text-muted-foreground">المنصة مخصصة للغات الويب الأساسية: HTML و CSS و JavaScript فقط.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl mx-auto">
          {baseCats.map((c) => {
            const Icon = c.icon;
            const count = counts[c.key] || 0;
            return (
              <a
                href="#snippets"
                key={c.name}
                className="group bg-background rounded-2xl p-5 text-right shadow-card-soft hover:shadow-elegant hover:-translate-y-1 transition-smooth border border-border/60"
              >
                <div className={`w-12 h-12 rounded-xl grid place-items-center mb-4 ${c.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
                <div className="font-bold text-primary text-lg">{c.name}</div>
                <div className="text-xs text-muted-foreground mt-1">{count} كود</div>
              </a>
            );
          })}
        </div>
      </div>
    </section>
  );
};
