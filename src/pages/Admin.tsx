import { useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "@/hooks/use-toast";
import { supabase } from "@/integrations/supabase/client";
import { Trash2, Upload, Lock, Eye, Heart, Search, CheckCircle2, XCircle } from "lucide-react";

const STORAGE_KEY = "admin_code";

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
  published: boolean;
  created_at: string;
};

const Admin = () => {
  const [code, setCode] = useState(localStorage.getItem(STORAGE_KEY) || "");
  const [authed, setAuthed] = useState(false);
  const [list, setList] = useState<Snippet[]>([]);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<"all" | "published" | "draft">("all");

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [language, setLanguage] = useState<"HTML" | "CSS" | "JS">("HTML");
  const [snippetCode, setSnippetCode] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const callApi = async (action: string, payload?: unknown) => {
    const { data, error } = await supabase.functions.invoke("admin-snippets", {
      body: { code, action, payload },
    });
    if (error) throw error;
    if ((data as { error?: string })?.error) throw new Error((data as { error: string }).error);
    return data;
  };

  const refresh = async () => {
    setLoading(true);
    try {
      const res = (await callApi("list")) as { data: Snippet[] };
      setList(res.data || []);
    } catch (e) {
      toast({ title: "خطأ", description: (e as Error).message, variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  const verify = async () => {
    if (!code.trim()) return;
    try {
      await callApi("list");
      localStorage.setItem(STORAGE_KEY, code);
      setAuthed(true);
      toast({ title: "تم الدخول بنجاح" });
    } catch (e) {
      toast({ title: "رمز غير صحيح", description: (e as Error).message, variant: "destructive" });
    }
  };

  useEffect(() => {
    if (authed) refresh();
  }, [authed]);

  useEffect(() => {
    if (code) verify();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fileToBase64 = (f: File) =>
    new Promise<string>((resolve, reject) => {
      const r = new FileReader();
      r.onload = () => {
        const s = r.result as string;
        resolve(s.split(",")[1]);
      };
      r.onerror = reject;
      r.readAsDataURL(f);
    });

  const handlePublish = async () => {
    if (!title.trim() || (!snippetCode.trim() && !file)) {
      toast({ title: "أدخل عنوان وكود أو ملف", variant: "destructive" });
      return;
    }
    setLoading(true);
    try {
      let file_url: string | null = null;
      let file_name: string | null = null;
      if (file) {
        const base64 = await fileToBase64(file);
        const up = (await callApi("upload", {
          fileName: file.name,
          base64,
          contentType: file.type || "application/octet-stream",
        })) as { url: string };
        file_url = up.url;
        file_name = file.name;
      }
      await callApi("insert", {
        title,
        description,
        language,
        code: snippetCode || null,
        file_url,
        file_name,
        published: true,
      });
      setTitle("");
      setDescription("");
      setSnippetCode("");
      setFile(null);
      toast({ title: "تم النشر بنجاح" });
      refresh();
    } catch (e) {
      toast({ title: "فشل النشر", description: (e as Error).message, variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  const updateSnippet = async (id: string, patch: Partial<Snippet>) => {
    try {
      await callApi("update", { id, patch });
      refresh();
    } catch (e) {
      toast({ title: "فشل التعديل", description: (e as Error).message, variant: "destructive" });
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("حذف هذا الكود نهائياً؟")) return;
    try {
      await callApi("delete", { id });
      toast({ title: "تم الحذف" });
      refresh();
    } catch (e) {
      toast({ title: "فشل الحذف", description: (e as Error).message, variant: "destructive" });
    }
  };

  const filteredList = useMemo(() => {
    return list.filter((s) => {
      const textMatch = [s.title, s.description, s.language].join(" ").toLowerCase().includes(query.toLowerCase());
      const stateMatch = statusFilter === "all" || (statusFilter === "published" ? s.published : !s.published);
      return textMatch && stateMatch;
    });
  }, [list, query, statusFilter]);

  if (!authed) {
    return <div className="min-h-screen grid place-items-center bg-background p-6"><div className="w-full max-w-md rounded-2xl border border-border bg-card p-8 shadow-elegant"><div className="flex flex-col items-center text-center mb-6"><div className="w-14 h-14 rounded-2xl bg-primary text-primary-foreground grid place-items-center mb-3"><Lock /></div><h1 className="text-2xl font-black text-primary">لوحة الإدارة</h1><p className="text-sm text-muted-foreground mt-1">أدخل رمز الحماية للمتابعة</p></div><Input type="password" placeholder="رمز الحماية" value={code} onChange={(e) => setCode(e.target.value)} onKeyDown={(e) => e.key === "Enter" && verify()} className="text-center tracking-widest font-bold" /><Button className="w-full mt-4" variant="cta" onClick={verify}>دخول</Button></div></div>;
  }

  return (
    <div className="min-h-screen bg-muted/20">
      <header className="border-b border-border bg-card/95 backdrop-blur sticky top-0 z-20">
        <div className="container py-4 flex items-center justify-between gap-4">
          <h1 className="text-xl font-black text-primary">لوحة إدارة منصتي</h1>
          <Button variant="outline" size="sm" onClick={() => { localStorage.removeItem(STORAGE_KEY); setAuthed(false); setCode(""); }}>خروج</Button>
        </div>
      </header>
      <main className="container py-8 grid xl:grid-cols-[1.1fr_1.4fr] gap-8">
        <section className="rounded-2xl border border-border bg-card p-6 shadow-card-soft">
          <h2 className="text-lg font-bold text-primary mb-4">نشر كود جديد</h2>
          <div className="space-y-3">
            <Input placeholder="العنوان" value={title} onChange={(e) => setTitle(e.target.value)} />
            <Textarea placeholder="وصف مختصر" value={description} onChange={(e) => setDescription(e.target.value)} />
            <div className="flex gap-2">{(["HTML", "CSS", "JS"] as const).map((l) => <button key={l} onClick={() => setLanguage(l)} className={`flex-1 py-2 rounded-lg text-sm font-bold border transition-smooth ${language === l ? "bg-primary text-primary-foreground border-primary" : "bg-background border-border hover:border-primary"}`}>{l}</button>)}</div>
            <Textarea dir="ltr" placeholder="الصق الكود هنا..." value={snippetCode} onChange={(e) => setSnippetCode(e.target.value)} className="font-mono min-h-40" />
            <label className="flex items-center gap-2 px-3 py-2 border border-dashed border-border rounded-lg cursor-pointer hover:border-primary transition-smooth"><Upload className="w-4 h-4" /><span className="text-sm">{file ? file.name : "أو ارفع ملف (اختياري)"}</span><input type="file" className="hidden" onChange={(e) => setFile(e.target.files?.[0] || null)} /></label>
            <Button variant="cta" className="w-full" onClick={handlePublish} disabled={loading}>{loading ? "جاري النشر..." : "نشر"}</Button>
          </div>
        </section>

        <section className="rounded-2xl border border-border bg-card p-6 shadow-card-soft">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-3 mb-4">
            <h2 className="text-lg font-bold text-primary">الأكواد ({filteredList.length}/{list.length})</h2>
            <div className="flex flex-wrap gap-2">
              <div className="relative"><Search className="w-4 h-4 absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground" /><Input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="بحث..." className="pr-9 w-52" /></div>
              {(["all", "published", "draft"] as const).map((mode) => <Button key={mode} size="sm" variant={statusFilter === mode ? "default" : "outline"} onClick={() => setStatusFilter(mode)}>{mode === "all" ? "الكل" : mode === "published" ? "منشور" : "مسودة"}</Button>)}
            </div>
          </div>
          <div className="space-y-3 max-h-[620px] overflow-y-auto">
            {filteredList.map((s) => (
              <div key={s.id} className="border border-border rounded-lg p-4 space-y-3">
                <div className="flex items-start justify-between gap-2"><div><div className="flex items-center gap-2 mb-1"><span className="text-[10px] font-bold px-2 py-0.5 rounded bg-primary/10 text-primary">{s.language}</span><h3 className="font-bold">{s.title}</h3></div><p className="text-xs text-muted-foreground line-clamp-1">{s.description}</p></div><Button variant="ghost" size="icon" onClick={() => handleDelete(s.id)} className="text-destructive hover:text-destructive"><Trash2 className="w-4 h-4" /></Button></div>
                <div className="grid sm:grid-cols-2 gap-2 text-xs">
                  <label className="space-y-1"><span className="text-muted-foreground">المشاهدات</span><Input type="number" min={0} value={s.views} onChange={(e) => updateSnippet(s.id, { views: Number(e.target.value) || 0 })} /></label>
                  <label className="space-y-1"><span className="text-muted-foreground">الإعجابات</span><Input type="number" min={0} value={s.likes} onChange={(e) => updateSnippet(s.id, { likes: Number(e.target.value) || 0 })} /></label>
                </div>
                <div className="flex items-center justify-between"><div className="flex gap-3 text-xs text-muted-foreground"><span className="flex items-center gap-1"><Eye className="w-3 h-3" /> {s.views}</span><span className="flex items-center gap-1"><Heart className="w-3 h-3" /> {s.likes}</span></div><Button size="sm" variant={s.published ? "outline" : "default"} onClick={() => updateSnippet(s.id, { published: !s.published })}>{s.published ? <><CheckCircle2 className="w-4 h-4 ml-1" /> منشور</> : <><XCircle className="w-4 h-4 ml-1" /> مسودة</>}</Button></div>
              </div>
            ))}
            {!filteredList.length && <p className="text-sm text-muted-foreground text-center py-8">لا توجد نتائج مطابقة</p>}
          </div>
        </section>
      </main>
    </div>
  );
};

export default Admin;
