import { Heart, Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";

type Snippet = {
  title: string;
  author: string;
  lang: "HTML" | "CSS" | "JS";
  code: string;
  views: number;
  likes: number;
  desc: string;
};

const SNIPPETS: Snippet[] = [
  {
    title: "زر متحرك بتدرج لوني",
    author: "أحمد المصري",
    lang: "CSS",
    desc: "زر بتأثير hover ناعم وتدرّج لوني جذّاب.",
    views: 1240, likes: 312,
    code: `.btn-glow {
  background: linear-gradient(135deg, #FFD23F, #FF6B35);
  border-radius: 999px;
  padding: 12px 28px;
  transition: transform .3s;
}
.btn-glow:hover { transform: scale(1.05); }`,
  },
  {
    title: "تحقق من البريد الإلكتروني",
    author: "سارة بن علي",
    lang: "JS",
    desc: "دالة بسيطة وسريعة للتحقق من صحة الإيميل.",
    views: 890, likes: 201,
    code: `function isValidEmail(email) {
  const re = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
  return re.test(email);
}

console.log(isValidEmail("user@mansati.com"));`,
  },
  {
    title: "بطاقة منتج Responsive",
    author: "خالد الليبي",
    lang: "HTML",
    desc: "هيكل بطاقة منتج متجاوب مع جميع الشاشات.",
    views: 2103, likes: 540,
    code: `<article class="card">
  <img src="product.jpg" alt="منتج" />
  <h3>اسم المنتج</h3>
  <p>وصف قصير للمنتج.</p>
  <button>اشتري الآن</button>
</article>`,
  },
  {
    title: "تأثير hover على البطاقات",
    author: "ليلى عبدالله",
    lang: "CSS",
    desc: "تأثير ارتفاع ناعم عند تمرير المؤشر فوق البطاقة.",
    views: 1567, likes: 423,
    code: `.card {
  transition: transform .3s, box-shadow .3s;
}
.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 30px rgba(0,0,0,.12);
}`,
  },
  {
    title: "قائمة منسدلة بـ JS",
    author: "عمر الطرابلسي",
    lang: "JS",
    desc: "فتح وإغلاق قائمة منسدلة عند النقر.",
    views: 670, likes: 145,
    code: `const btn = document.querySelector('.menu-btn');
const menu = document.querySelector('.menu');
btn.addEventListener('click', () => {
  menu.classList.toggle('open');
});`,
  },
  {
    title: "Skeleton Loader أنيق",
    author: "نور الدين",
    lang: "CSS",
    desc: "تأثير تحميل بسيط وأنيق بدون مكتبات.",
    views: 980, likes: 278,
    code: `.skeleton {
  background: linear-gradient(
    90deg, #eee 25%, #f5f5f5 50%, #eee 75%
  );
  background-size: 200% 100%;
  animation: shine 1.4s infinite;
}
@keyframes shine {
  to { background-position: -200% 0; }
}`,
  },
];

const langStyles: Record<Snippet["lang"], string> = {
  HTML: "bg-cta/10 text-cta border-cta/20",
  CSS: "bg-primary-glow/15 text-primary-glow border-primary-glow/20",
  JS: "bg-secondary/30 text-primary border-secondary",
};

const filters = ["الكل", "HTML", "CSS", "JS"] as const;

export const SnippetsGrid = () => {
  const [active, setActive] = useState<(typeof filters)[number]>("الكل");
  const list = active === "الكل" ? SNIPPETS : SNIPPETS.filter((s) => s.lang === active);

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

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {list.map((s, i) => (
            <article
              key={s.title}
              className="group rounded-2xl bg-card border border-border overflow-hidden shadow-card-soft hover:shadow-elegant transition-smooth hover:-translate-y-1 animate-fade-up"
              style={{ animationDelay: `${i * 60}ms` }}
            >
              <header className="flex items-center justify-between px-5 py-3 bg-primary text-primary-foreground" dir="ltr">
                <div className="flex gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-destructive" />
                  <span className="w-2.5 h-2.5 rounded-full bg-secondary" />
                  <span className="w-2.5 h-2.5 rounded-full bg-success" />
                </div>
                <span className={`text-[10px] font-bold px-2 py-1 rounded border ${langStyles[s.lang]}`}>{s.lang}</span>
              </header>

              <pre dir="ltr" className="bg-primary/95 text-primary-foreground/90 p-5 text-xs leading-relaxed overflow-x-auto max-h-44 font-mono">
                <code>{s.code}</code>
              </pre>

              <div className="p-5 space-y-3">
                <h3 className="font-bold text-lg text-primary">{s.title}</h3>
                <p className="text-sm text-muted-foreground line-clamp-2">{s.desc}</p>
                <div className="flex items-center justify-between pt-2 border-t border-border text-xs text-muted-foreground">
                  <span className="flex items-center gap-1.5 font-semibold">
                    <Copy className="w-3.5 h-3.5" />
                    {s.views} نسخة
                  </span>
                  <span className="flex items-center gap-1.5 font-semibold">
                    <Heart className="w-3.5 h-3.5" />
                    {s.likes} تفاعل
                  </span>
                </div>
                <Button variant="outline" size="sm" className="w-full gap-2">
                  <Copy className="w-4 h-4" />
                  نسخ الكود
                </Button>
              </div>
            </article>
          ))}
        </div>

        <div className="text-center mt-12">
          <Button variant="hero" size="lg">عرض جميع الأكواد</Button>
        </div>
      </div>
    </section>
  );
};
