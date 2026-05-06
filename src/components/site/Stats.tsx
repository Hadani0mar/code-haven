import { useEffect, useState } from "react";
import { supabase } from "@/integrations/supabase/client";

export const Stats = () => {
  const [data, setData] = useState({ snippets: 0, views: 0, likes: 0 });

  useEffect(() => {
    (async () => {
      const { data: rows, count } = await supabase
        .from("snippets")
        .select("views,likes", { count: "exact" })
        .eq("published", true);
      const views = (rows || []).reduce((a, r) => a + (r.views || 0), 0);
      const likes = (rows || []).reduce((a, r) => a + (r.likes || 0), 0);
      setData({ snippets: count || 0, views, likes });
    })();
  }, []);

  const stats = [
    { value: data.snippets.toLocaleString("ar-EG"), label: "كود منشور" },
    { value: data.views.toLocaleString("ar-EG"), label: "مرات النسخ" },
    { value: data.likes.toLocaleString("ar-EG"), label: "تفاعل" },
    { value: "24/7", label: "مجتمع نشط" },
  ];

  return (
    <section className="py-14 bg-primary text-primary-foreground relative overflow-hidden">
      <div className="absolute inset-0 dot-pattern opacity-10" />
      <div className="container relative grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
        {stats.map((s) => (
          <div key={s.label}>
            <div className="text-3xl md:text-4xl font-black text-secondary">{s.value}</div>
            <div className="text-sm md:text-base text-primary-foreground/80 mt-1">{s.label}</div>
          </div>
        ))}
      </div>
    </section>
  );
};
