import { Heart, Copy, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "@/hooks/use-toast";

const SkeletonCard = () => (
  <div className="rounded-2xl bg-card border border-border overflow-hidden shadow-card-soft animate-pulse">
    <div className="h-10 bg-primary/80" />
    <div className="h-44 bg-primary/10" />
    <div className="p-5 space-y-3">
      <div className="h-5 w-2/3 rounded bg-muted" />
      <div className="h-3 w-full rounded bg-muted" />
      <div className="h-3 w-4/5 rounded bg-muted" />
      <div className="flex justify-between pt-2 border-t border-border">
        <div className="h-3 w-16 rounded bg-muted" />
        <div className="h-3 w-16 rounded bg-muted" />
      </div>
      <div className="h-8 w-full rounded-lg bg-muted" />
    </div>
  </div>
);

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
  FULL: "bg-success/15 text-success border-success/20",
};

const filters = ["الكل", "HTML", "CSS", "JS", "FULL"] as const;

const buildFullHtml = (title: string, html: string, css: string, js: string) =>
  `<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>${title}</title>\n<style>\n${css}\n</style>\n</head>\n<body>\n${html}\n<script>\n${js}\n<\/script>\n</body>\n</html>`;

export const SnippetsGrid = () => {
  const [active, setActive] = useState<(typeof filters)[number]>("الكل");
  const [items, setItems] = useState<Snippet[]>([]);
  const [loadingSnippets, setLoadingSnippets] = useState(true);
  const [liked, setLiked] = useState<Set<string>>(
    () => new Set(JSON.parse(localStorage.getItem("liked_snippets") || "[]")),
  );

  const load = async () => {
    setLoadingSnippets(true);
    const { data } = await supabase
      .from("snippets")
      .select("id,title,description,language,code,file_url,file_name,views,likes")
      .eq("published", true)
      .order("created_at", { ascending: false });
    setItems((data as Snippet[]) || []);
    setLoadingSnippets(false);
  };

  useEffect(() => {
    load();
  }, []);

  const list = active === "الكل" ? items : items.filter((s) => s.language === active);

  const handleDownloadFull = async (s: Snippet) => {
    try {
      const parts = JSON.parse(s.code || "{}");
      const fullHtml = buildFullHtml(s.title, parts.html || "", parts.css || "", parts.js || "");
      const blob = new Blob([fullHtml], { type: "text/html" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${s.title}.html`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      await supabase.rpc("increment_snippet_views", { snippet_id: s.id });
      setItems((prev) => prev.map((x) => (x.id === s.id ? { ...x, views: x.views + 1 } : x)));
      toast({ title: "تم تحميل الملف" });
    } catch {
      toast({ title: "فشل التحميل", variant: "destructive" });
    }
  };

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

  const handleDownload = async (s: Snippet) => {
    if (!s.file_url) return;
    try {
      const res = await fetch(s.file_url);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = s.file_name || `${s.title}.txt`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      await supabase.rpc("increment_snippet_views", { snippet_id: s.id });
      setItems((prev) => prev.map((x) => (x.id === s.id ? { ...x, views: x.views + 1 } : x)));
    } catch {
      window.open(s.file_url, "_blank");
    }
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

        {loadingSnippets && (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)}
          </div>
        )}

        {!loadingSnippets && !list.length && (
          <p className="text-center text-muted-foreground py-16">لا توجد أكواد بعد.</p>
        )}

        {!loadingSnippets && (
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

              {s.language === "FULL" ? (
                <div className="bg-primary/95 p-5 flex flex-col gap-1.5" dir="ltr">
                  {["html", "css", "js"].map((part) => {
                    try {
                      const parsed = JSON.parse(s.code || "{}");
                      const val = (parsed[part] || "").trim();
                      if (!val) return null;
                      return (
                        <div key={part} className="text-[10px] font-mono text-primary-foreground/60 truncate">
                          <span className="text-secondary font-bold mr-1">{part.toUpperCase()}</span>
                          {val.split("\n")[0]}
                        </div>
                      );
                    } catch { return null; }
                  })}
                </div>
              ) : s.code && (
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
                {s.language === "FULL" ? (
                  <Button variant="cta" size="sm" className="w-full gap-2" onClick={() => handleDownloadFull(s)}>
                    <Download className="w-4 h-4" />
                    تحميل الكود كاملاً (.html)
                  </Button>
                ) : (
                  <>
                    {s.code && (
                      <Button variant="outline" size="sm" className="w-full gap-2" onClick={() => handleCopy(s)}>
                        <Copy className="w-4 h-4" />
                        نسخ الكود
                      </Button>
                    )}
                    {s.file_url && (
                      <Button variant="outline" size="sm" className="w-full gap-2" onClick={() => handleDownload(s)}>
                        <Download className="w-4 h-4" />
                        تحميل الملف
                      </Button>
                    )}
                  </>
                )}
              </div>
            </article>
          ))}
        </div>
        )}
      </div>
    </section>
  );
};
