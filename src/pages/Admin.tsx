import { useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "@/hooks/use-toast";
import { supabase } from "@/integrations/supabase/client";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Trash2,
  Upload,
  Lock,
  Eye,
  Heart,
  Pencil,
  EyeOff,
  RotateCcw,
  X,
  FileCode2,
  CheckCircle2,
  Search,
  Copy,
  Download,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

const STORAGE_KEY = "admin_code";
const PAGE_SIZE = 8;

type Lang = "HTML" | "CSS" | "JS";
type Snippet = {
  id: string;
  title: string;
  description: string | null;
  category: string | null;
  language: Lang;
  code: string | null;
  file_url: string | null;
  file_name: string | null;
  views: number;
  likes: number;
  published: boolean;
  created_at: string;
};

type Stats = { total: number; published: number; drafts: number; views: number; likes: number };

const langStyles: Record<string, string> = {
  HTML: "bg-cta/10 text-cta border-cta/20",
  CSS: "bg-primary-glow/15 text-primary-glow border-primary-glow/20",
  JS: "bg-secondary/30 text-primary border-secondary",
};

const Admin = () => {
  const [code, setCode] = useState(localStorage.getItem(STORAGE_KEY) || "");
  const [authed, setAuthed] = useState(false);
  const [list, setList] = useState<Snippet[]>([]);
  const [stats, setStats] = useState<Stats>({ total: 0, published: 0, drafts: 0, views: 0, likes: 0 });
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<"all" | Lang>("all");
  const [page, setPage] = useState(1);

  // form state
  const [editingId, setEditingId] = useState<string | null>(null);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");
  const [language, setLanguage] = useState<Lang>("HTML");
  const [snippetCode, setSnippetCode] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [published, setPublished] = useState(true);

  // dialog state
  const [deleteTarget, setDeleteTarget] = useState<string | null>(null);
  const [resetTarget, setResetTarget] = useState<string | null>(null);
  const [previewSnippet, setPreviewSnippet] = useState<Snippet | null>(null);

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
      const [l, s] = await Promise.all([callApi("list"), callApi("stats")]);
      setList(((l as { data: Snippet[] }).data) || []);
      setStats(((s as { data: Stats }).data) || stats);
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

  useEffect(() => { if (authed) refresh(); }, [authed]);
  useEffect(() => {
    if (code) verify();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fileToBase64 = (f: File) =>
    new Promise<string>((resolve, reject) => {
      const r = new FileReader();
      r.onload = () => resolve((r.result as string).split(",")[1]);
      r.onerror = reject;
      r.readAsDataURL(f);
    });

  const resetForm = () => {
    setEditingId(null);
    setTitle("");
    setDescription("");
    setCategory("");
    setLanguage("HTML");
    setSnippetCode("");
    setFile(null);
    setPublished(true);
  };

  const startEdit = (s: Snippet) => {
    setEditingId(s.id);
    setTitle(s.title);
    setDescription(s.description || "");
    setCategory(s.category || "");
    setLanguage(s.language);
    setSnippetCode(s.code || "");
    setPublished(s.published);
    setFile(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleSubmit = async () => {
    if (!title.trim() || (!snippetCode.trim() && !file && !editingId)) {
      toast({ title: "أدخل عنوان وكود أو ملف", variant: "destructive" });
      return;
    }
    setLoading(true);
    try {
      let file_url: string | null | undefined = undefined;
      let file_name: string | null | undefined = undefined;
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

      if (editingId) {
        const payload: Record<string, unknown> = {
          id: editingId, title, description,
          category: category || null,
          language, code: snippetCode || null, published,
        };
        if (file_url !== undefined) { payload.file_url = file_url; payload.file_name = file_name; }
        await callApi("update", payload);
        toast({ title: "تم تحديث الكود" });
      } else {
        await callApi("insert", {
          title, description, category: category || null,
          language, code: snippetCode || null,
          file_url: file_url ?? null, file_name: file_name ?? null, published,
        });
        toast({ title: "تم النشر بنجاح" });
      }
      resetForm();
      refresh();
    } catch (e) {
      toast({ title: "فشل الحفظ", description: (e as Error).message, variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  const confirmDelete = async () => {
    if (!deleteTarget) return;
    try {
      await callApi("delete", { id: deleteTarget });
      toast({ title: "تم الحذف" });
      refresh();
    } catch (e) {
      toast({ title: "فشل الحذف", description: (e as Error).message, variant: "destructive" });
    } finally {
      setDeleteTarget(null);
    }
  };

  const confirmReset = async () => {
    if (!resetTarget) return;
    try {
      await callApi("resetCounters", { id: resetTarget });
      toast({ title: "تم التصفير" });
      refresh();
    } catch (e) {
      toast({ title: "فشل العملية", description: (e as Error).message, variant: "destructive" });
    } finally {
      setResetTarget(null);
    }
  };

  const handleToggle = async (id: string) => {
    try {
      await callApi("togglePublished", { id });
      refresh();
    } catch (e) {
      toast({ title: "فشل التحديث", description: (e as Error).message, variant: "destructive" });
    }
  };

  const filtered = useMemo(() => {
    setPage(1);
    return list.filter((s) => {
      if (filter !== "all" && s.language !== filter) return false;
      if (search && !`${s.title} ${s.description || ""} ${s.category || ""}`.toLowerCase().includes(search.toLowerCase()))
        return false;
      return true;
    });
  }, [list, filter, search]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const paginated = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  // preview uses current form values if no saved snippet passed
  const previewData = previewSnippet ?? {
    id: "preview",
    title: title || "عنوان الكود",
    description: description || null,
    language,
    code: snippetCode || null,
    file_url: null,
    file_name: null,
    views: 0,
    likes: 0,
    published,
    category: category || null,
    created_at: new Date().toISOString(),
  };

  if (!authed) {
    return (
      <div className="min-h-screen grid place-items-center bg-background p-6">
        <div className="w-full max-w-md rounded-2xl border border-border bg-card p-8 shadow-elegant">
          <div className="flex flex-col items-center text-center mb-6">
            <div className="w-14 h-14 rounded-2xl bg-primary text-primary-foreground grid place-items-center mb-3">
              <Lock />
            </div>
            <h1 className="text-2xl font-black text-primary">لوحة الإدارة</h1>
            <p className="text-sm text-muted-foreground mt-1">أدخل رمز الحماية للمتابعة</p>
          </div>
          <Input
            type="password"
            placeholder="رمز الحماية"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && verify()}
            className="text-center tracking-widest font-bold"
          />
          <Button className="w-full mt-4" variant="cta" onClick={verify}>دخول</Button>
        </div>
      </div>
    );
  }

  const statCards = [
    { label: "إجمالي الأكواد", value: stats.total, icon: FileCode2 },
    { label: "منشور", value: stats.published, icon: CheckCircle2 },
    { label: "مرات النسخ", value: stats.views, icon: Eye },
    { label: "تفاعل", value: stats.likes, icon: Heart },
  ];

  return (
    <div className="min-h-screen bg-background">

      {/* Delete confirmation */}
      <AlertDialog open={!!deleteTarget} onOpenChange={(o) => !o && setDeleteTarget(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>حذف الكود نهائياً؟</AlertDialogTitle>
            <AlertDialogDescription>
              لا يمكن التراجع عن هذا الإجراء. سيتم حذف الكود بشكل دائم.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter className="flex-row-reverse gap-2">
            <AlertDialogCancel>إلغاء</AlertDialogCancel>
            <AlertDialogAction onClick={confirmDelete} className="bg-destructive hover:bg-destructive/90 text-destructive-foreground">
              نعم، احذف
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Reset confirmation */}
      <AlertDialog open={!!resetTarget} onOpenChange={(o) => !o && setResetTarget(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>تصفير العدادات؟</AlertDialogTitle>
            <AlertDialogDescription>
              سيتم إعادة عدادَي النسخ والتفاعل إلى الصفر.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter className="flex-row-reverse gap-2">
            <AlertDialogCancel>إلغاء</AlertDialogCancel>
            <AlertDialogAction onClick={confirmReset}>تصفير</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Preview modal */}
      <Dialog open={!!previewSnippet} onOpenChange={(o) => !o && setPreviewSnippet(null)}>
        <DialogContent className="max-w-md p-0 overflow-hidden">
          <DialogHeader className="px-5 pt-5 pb-0">
            <DialogTitle className="text-base">معاينة الكود كما يظهر للزوار</DialogTitle>
          </DialogHeader>
          <div className="p-4">
            <article className="rounded-2xl bg-card border border-border overflow-hidden shadow-card-soft">
              <header className="flex items-center justify-between px-5 py-3 bg-primary text-primary-foreground" dir="ltr">
                <div className="flex gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-destructive" />
                  <span className="w-2.5 h-2.5 rounded-full bg-secondary" />
                  <span className="w-2.5 h-2.5 rounded-full bg-success" />
                </div>
                <span className={`text-[10px] font-bold px-2 py-1 rounded border ${langStyles[previewData.language] || "bg-muted text-foreground border-border"}`}>
                  {previewData.language}
                </span>
              </header>
              {previewData.code && (
                <pre dir="ltr" className="bg-primary/95 text-primary-foreground/90 p-5 text-xs leading-relaxed overflow-x-auto max-h-44 font-mono">
                  <code>{previewData.code}</code>
                </pre>
              )}
              <div className="p-5 space-y-3">
                <div>
                  <h3 className="font-bold text-lg text-primary">{previewData.title}</h3>
                  {previewData.category && (
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-accent/30 text-accent-foreground mt-1 inline-block">
                      {previewData.category}
                    </span>
                  )}
                </div>
                {previewData.description && (
                  <p className="text-sm text-muted-foreground line-clamp-2">{previewData.description}</p>
                )}
                <div className="flex items-center justify-between pt-2 border-t border-border text-xs text-muted-foreground">
                  <span className="flex items-center gap-1.5 font-semibold"><Copy className="w-3.5 h-3.5" /> 0 نسخة</span>
                  <span className="flex items-center gap-1.5 font-semibold"><Heart className="w-3.5 h-3.5" /> 0 تفاعل</span>
                </div>
                {previewData.code && (
                  <Button variant="outline" size="sm" className="w-full gap-2" disabled>
                    <Copy className="w-4 h-4" /> نسخ الكود
                  </Button>
                )}
                {previewData.file_url && (
                  <Button variant="outline" size="sm" className="w-full gap-2" disabled>
                    <Download className="w-4 h-4" /> تحميل الملف
                  </Button>
                )}
              </div>
            </article>
          </div>
        </DialogContent>
      </Dialog>

      <header className="border-b border-border bg-card sticky top-0 z-40">
        <div className="container py-4 flex items-center justify-between">
          <h1 className="text-xl font-black text-primary">لوحة إدارة منصتي</h1>
          <Button variant="outline" size="sm" onClick={() => { localStorage.removeItem(STORAGE_KEY); setAuthed(false); setCode(""); }}>
            خروج
          </Button>
        </div>
      </header>

      <main className="container py-8 space-y-8">
        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {statCards.map((c) => {
            const Icon = c.icon;
            return (
              <div key={c.label} className="rounded-xl border border-border bg-card p-4 flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-primary/10 text-primary grid place-items-center">
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-2xl font-black text-primary">{c.value}</div>
                  <div className="text-xs text-muted-foreground">{c.label}</div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Form */}
          <section className="rounded-2xl border border-border bg-card p-6 shadow-card-soft">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-primary">
                {editingId ? "تعديل كود" : "نشر كود جديد"}
              </h2>
              <div className="flex gap-2">
                {(title || snippetCode) && (
                  <Button variant="outline" size="sm" onClick={() => setPreviewSnippet(previewData)} className="gap-1 text-xs">
                    <Eye className="w-3 h-3" /> معاينة
                  </Button>
                )}
                {editingId && (
                  <Button variant="ghost" size="sm" onClick={resetForm} className="gap-1">
                    <X className="w-4 h-4" /> إلغاء
                  </Button>
                )}
              </div>
            </div>
            <div className="space-y-3">
              <Input placeholder="العنوان *" value={title} onChange={(e) => setTitle(e.target.value)} />
              <Input placeholder="التصنيف (مثال: نماذج، قوائم، تأثيرات...)" value={category} onChange={(e) => setCategory(e.target.value)} />
              <Textarea placeholder="وصف مختصر" value={description} onChange={(e) => setDescription(e.target.value)} />
              <div className="flex gap-2">
                {(["HTML", "CSS", "JS"] as const).map((l) => (
                  <button
                    key={l}
                    onClick={() => setLanguage(l)}
                    className={`flex-1 py-2 rounded-lg text-sm font-bold border transition-smooth ${
                      language === l ? "bg-primary text-primary-foreground border-primary" : "bg-background border-border hover:border-primary"
                    }`}
                  >
                    {l}
                  </button>
                ))}
              </div>
              <div className="relative rounded-lg border border-border overflow-hidden focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-0">
                <div className="flex" dir="ltr">
                  <div
                    aria-hidden
                    className="select-none bg-muted/50 text-muted-foreground text-xs font-mono px-2 py-3 leading-6 text-right min-w-[2.5rem] border-r border-border"
                  >
                    {(snippetCode || " ").split("\n").map((_, i) => (
                      <div key={i}>{i + 1}</div>
                    ))}
                  </div>
                  <textarea
                    dir="ltr"
                    placeholder="الصق الكود هنا..."
                    value={snippetCode}
                    onChange={(e) => setSnippetCode(e.target.value)}
                    spellCheck={false}
                    className="flex-1 resize-none bg-background font-mono text-sm px-3 py-3 leading-6 min-h-44 outline-none placeholder:text-muted-foreground"
                    onKeyDown={(e) => {
                      if (e.key === "Tab") {
                        e.preventDefault();
                        const t = e.currentTarget;
                        const s = t.selectionStart, en = t.selectionEnd;
                        const v = t.value;
                        t.value = v.substring(0, s) + "  " + v.substring(en);
                        t.selectionStart = t.selectionEnd = s + 2;
                        setSnippetCode(t.value);
                      }
                    }}
                  />
                </div>
              </div>
              <label className="flex items-center gap-2 px-3 py-2 border border-dashed border-border rounded-lg cursor-pointer hover:border-primary transition-smooth">
                <Upload className="w-4 h-4" />
                <span className="text-sm">{file ? file.name : "أو ارفع ملف (اختياري)"}</span>
                <input type="file" className="hidden" onChange={(e) => setFile(e.target.files?.[0] || null)} />
              </label>
              <label className="flex items-center gap-2 text-sm cursor-pointer select-none">
                <input type="checkbox" checked={published} onChange={(e) => setPublished(e.target.checked)} className="w-4 h-4" />
                نشر مباشر (يظهر للزوار)
              </label>
              <Button variant="cta" className="w-full" onClick={handleSubmit} disabled={loading}>
                {loading ? "جاري الحفظ..." : editingId ? "حفظ التعديلات" : "نشر"}
              </Button>
            </div>
          </section>

          {/* List */}
          <section className="rounded-2xl border border-border bg-card p-6 shadow-card-soft">
            <h2 className="text-lg font-bold text-primary mb-3">
              إدارة الأكواد ({filtered.length}/{list.length})
            </h2>

            <div className="space-y-2 mb-4">
              <div className="relative">
                <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input placeholder="بحث..." value={search} onChange={(e) => setSearch(e.target.value)} className="pr-9" />
              </div>
              <div className="flex gap-2">
                {(["all", "HTML", "CSS", "JS"] as const).map((f) => (
                  <button
                    key={f}
                    onClick={() => setFilter(f)}
                    className={`flex-1 py-1.5 rounded-md text-xs font-bold border transition-smooth ${
                      filter === f ? "bg-primary text-primary-foreground border-primary" : "bg-background border-border hover:border-primary"
                    }`}
                  >
                    {f === "all" ? "الكل" : f}
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-3 min-h-[200px]">
              {paginated.map((s) => (
                <div
                  key={s.id}
                  className={`border rounded-lg p-4 ${editingId === s.id ? "border-cta bg-cta/5" : "border-border"}`}
                >
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2 mb-1 flex-wrap">
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-primary/10 text-primary">{s.language}</span>
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${s.published ? "bg-success/15 text-success" : "bg-muted text-muted-foreground"}`}>
                          {s.published ? "منشور" : "مسودة"}
                        </span>
                        {s.category && (
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-accent/30 text-accent-foreground">{s.category}</span>
                        )}
                        <h3 className="font-bold truncate">{s.title}</h3>
                      </div>
                      <p className="text-xs text-muted-foreground line-clamp-1">{s.description}</p>
                      <div className="flex gap-3 mt-2 text-xs text-muted-foreground">
                        <span className="flex items-center gap-1"><Eye className="w-3 h-3" /> {s.views}</span>
                        <span className="flex items-center gap-1"><Heart className="w-3 h-3" /> {s.likes}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    <Button variant="outline" size="sm" onClick={() => setPreviewSnippet(s)} className="gap-1 h-7 text-xs">
                      <Eye className="w-3 h-3" /> معاينة
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => startEdit(s)} className="gap-1 h-7 text-xs">
                      <Pencil className="w-3 h-3" /> تعديل
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => handleToggle(s.id)} className="gap-1 h-7 text-xs">
                      {s.published ? <><EyeOff className="w-3 h-3" /> إخفاء</> : <><Eye className="w-3 h-3" /> نشر</>}
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => setResetTarget(s.id)} className="gap-1 h-7 text-xs">
                      <RotateCcw className="w-3 h-3" /> تصفير
                    </Button>
                    <Button variant="ghost" size="sm" onClick={() => setDeleteTarget(s.id)} className="gap-1 h-7 text-xs text-destructive hover:text-destructive">
                      <Trash2 className="w-3 h-3" /> حذف
                    </Button>
                  </div>
                </div>
              ))}
              {!filtered.length && (
                <p className="text-sm text-muted-foreground text-center py-8">لا توجد نتائج</p>
              )}
            </div>

            {totalPages > 1 && (
              <div className="flex items-center justify-between mt-4 pt-4 border-t border-border">
                <span className="text-xs text-muted-foreground">
                  صفحة {page} من {totalPages}
                </span>
                <div className="flex gap-1">
                  <Button variant="outline" size="sm" disabled={page === 1} onClick={() => setPage(p => p - 1)} className="h-7 w-7 p-0">
                    <ChevronRight className="w-4 h-4" />
                  </Button>
                  <Button variant="outline" size="sm" disabled={page === totalPages} onClick={() => setPage(p => p + 1)} className="h-7 w-7 p-0">
                    <ChevronLeft className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
};

export default Admin;
