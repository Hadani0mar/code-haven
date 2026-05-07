import { Heart, Copy, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "@/hooks/use-toast";

type Snippet = {
  id: string;
  title: string;
  description: string | null;
  language: string;
  code: string | null;
  file_url: string | null;
  file_name: string | null;
  views: number;
  likes: number;
};

const langStyles: Record<string, string> = {
  HTML: "bg-cta/10 text-cta border-cta/20",
  CSS: "bg-primary-glow/15 text-primary-glow border-primary-glow/20",
  JS: "bg-secondary/30 text-primary border-secondary",
};

const filters = ["الكل", "HTML", "CSS", "JS"] as const;

export const SnippetsGrid = () => {
  const [active, setActive] = useState<(typeof filters)[number]>("الكل");
  const [items, setItems] = useState<Snippet[]>([]);
  const [liked, setLiked] = useState<Set<string>>(
    () => new Set(JSON.parse(localStorage.getItem("liked_snippets") || "[]")),
  );

  const load = async () => {
    const { data } = await supabase
      .from("snippets")
      .select("id,title,description,language,code,file_url,file_name,views,likes")
      .eq("published", true)
      .order("created_at", { ascending: false });
    setItems((data as Snippet[]) || []);
  };

  useEffect(() => {
    load();
  }, []);

  const list = active === "الكل" ? items : items.filter((s) => s.language === active);

  const handleCopy = async (s: Snippet) => {
    if (!s.code) return;
    await navigator.clipboard.writeText(s.code);
    await supabase.rpc("increment_snippet_views", { snippet_id: s.id });
    setItems((prev) => prev.map((x) => (x.id === s.id ? { ...x, views: x.views + 1 } : x)));
    toast({ title: "تم نسخ الكود" });
  };

  const handleLike = async (s: Snippet) => {
    if (liked.has(s.id)) return;
    await supabase.rpc("increment_snippet_likes", { snippet_id: s.id });
    const next = new Set(liked);
    next.add(s.id);
    setLiked(next);
    localStorage.setItem("liked_snippets", JSON.stringify([...next]));
    setItems((prev) => prev.map((x) => (x.id === s.id ? { ...x, likes: x.likes + 1 } : x)));
  };

  return (
    <section id="snippets" className="py-20">
      <div className="container">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-10">
          <div>
            <p className="text-sm font-bold text-cta mb-2">آخر الأكواد المنشورة</p>
            <h2 className="text-3xl md:text-4xl font-black text-primary">مكتبة أكواد المجتمع</h2>
          </div>
          <div className="flex flex-wrap gap-2">
            {filters.map((f) => (
              <button
                key={f}
                onClick={() => setActive(f)}
                className={`px-4 py-2 rounded-full text-sm font-bold border transition-smooth ${
                  active === f
                    ? "bg-primary text-primary-foreground border-primary"
                    : "bg-background text-foreground border-border hover:border-primary"
                }`}
              >
                {f}
              </button>
            ))}
          </div>
        </div>

        {!list.length && (
          <p className="text-center text-muted-foreground py-16">لا توجد أكواد بعد.</p>
        )}

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {list.map((s, i) => (
            <article
              key={s.id}
              className="group rounded-2xl bg-card border border-border overflow-hidden shadow-card-soft hover:shadow-elegant transition-smooth hover:-translate-y-1 animate-fade-up"
              style={{ animationDelay: `${i * 60}ms` }}
            >
              <header className="flex items-center justify-between px-5 py-3 bg-primary text-primary-foreground" dir="ltr">
                <div className="flex gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-destructive" />
                  <span className="w-2.5 h-2.5 rounded-full bg-secondary" />
                  <span className="w-2.5 h-2.5 rounded-full bg-success" />
                </div>
                <span className={`text-[10px] font-bold px-2 py-1 rounded border ${langStyles[s.language] || "bg-muted text-foreground border-border"}`}>
                  {s.language}
                </span>
              </header>

              {s.code && (
                <pre dir="ltr" className="bg-primary/95 text-primary-foreground/90 p-5 text-xs leading-relaxed overflow-x-auto max-h-44 font-mono">
                  <code>{s.code}</code>
                </pre>
              )}

              <div className="p-5 space-y-3">
                <h3 className="font-bold text-lg text-primary">{s.title}</h3>
                {s.description && (
                  <p className="text-sm text-muted-foreground line-clamp-2">{s.description}</p>
                )}
                <div className="flex items-center justify-between pt-2 border-t border-border text-xs text-muted-foreground">
                  <span className="flex items-center gap-1.5 font-semibold">
                    <Copy className="w-3.5 h-3.5" />
                    {s.views} نسخة
                  </span>
                  <button
                    onClick={() => handleLike(s)}
                    disabled={liked.has(s.id)}
                    className={`flex items-center gap-1.5 font-semibold transition-smooth ${
                      liked.has(s.id) ? "text-cta" : "hover:text-cta"
                    }`}
                  >
                    <Heart className={`w-3.5 h-3.5 ${liked.has(s.id) ? "fill-current" : ""}`} />
                    {s.likes} تفاعل
                  </button>
                </div>
                {s.code && (
                  <Button variant="outline" size="sm" className="w-full gap-2" onClick={() => handleCopy(s)}>
                    <Copy className="w-4 h-4" />
                    نسخ الكود
                  </Button>
                )}
                {s.file_url && (
                  <Button variant="outline" size="sm" className="w-full gap-2" asChild>
                    <a href={s.file_url} download={s.file_name || true} target="_blank" rel="noreferrer">
                      <Download className="w-4 h-4" />
                      تحميل الملف
                    </a>
                  </Button>
                )}
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
};
