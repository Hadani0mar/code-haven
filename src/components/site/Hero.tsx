import { Button } from "@/components/ui/button";
import { Search, Check, Sparkles } from "lucide-react";

const features = [
  "آلاف المشاريع العربية مفتوحة المصدر",
  "مجتمع مطورين داعم ومتعاون",
  "واجهة مستخدم مبسطة وخفيفة جداً",
];

export const Hero = () => {
  return (
    <section className="relative overflow-hidden bg-gradient-hero text-primary-foreground">
      {/* decorative dots */}
      <div className="absolute inset-y-0 left-0 w-40 dot-pattern opacity-40" />
      <div className="absolute top-10 right-10 w-32 dot-pattern opacity-30 h-32" />
      <div className="absolute -bottom-24 -left-24 w-72 h-72 rounded-full bg-secondary/10 blur-3xl" />
      <div className="absolute top-1/3 right-1/4 w-80 h-80 rounded-full bg-primary-glow/30 blur-3xl" />

      <div className="container relative grid md:grid-cols-2 gap-10 items-center py-16 md:py-24">
        <div className="space-y-7 animate-fade-up">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-secondary/15 border border-secondary/30 text-secondary text-xs font-bold">
            <Sparkles className="w-3.5 h-3.5" />
            منصة ليبية مفتوحة للمطورين العرب
          </div>

          <h1 className="text-4xl md:text-5xl lg:text-6xl font-black leading-[1.15]">
            منصتي — بوابة تبادل
            <br />
            <span className="text-secondary">الأكواد العربية</span> المبسطة
          </h1>

          {/* Search bar */}
          <div className="relative max-w-xl">
            <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <input
              type="text"
              placeholder="ابحث عن الأكواد والمشاريع والمطورين…"
              className="w-full h-14 rounded-full pr-12 pl-6 bg-background text-foreground placeholder:text-muted-foreground/70 shadow-elegant outline-none focus:ring-4 focus:ring-secondary/40 transition-smooth"
            />
          </div>

          <ul className="space-y-3">
            {features.map((f) => (
              <li key={f} className="flex items-center gap-3 text-base md:text-lg font-semibold">
                <span className="w-7 h-7 rounded-md bg-secondary grid place-items-center text-secondary-foreground shrink-0">
                  <Check className="w-4 h-4" strokeWidth={3} />
                </span>
                {f}
              </li>
            ))}
          </ul>

          <div className="flex flex-wrap gap-3 pt-2">
            <Button variant="cta" size="xl" asChild>
              <a href="#snippets">تصفّح مكتبة الأكواد</a>
            </Button>
            <Button variant="outlineOnDark" size="xl" asChild>
              <a href="#categories">اعرف المزيد</a>
            </Button>
          </div>
        </div>

        {/* Visual phone-like card */}
        <div className="relative hidden md:block animate-fade-up [animation-delay:120ms]">
          <div className="relative mx-auto w-[340px] h-[560px] rounded-[3rem] bg-background/95 border-[10px] border-primary-foreground/90 shadow-elegant overflow-hidden">
            <div className="absolute top-0 inset-x-0 h-7 bg-primary-foreground/90" />
            <div className="p-5 pt-10 space-y-3 font-mono text-xs text-foreground" dir="ltr">
              <div className="flex gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-destructive" />
                <span className="w-2.5 h-2.5 rounded-full bg-secondary" />
                <span className="w-2.5 h-2.5 rounded-full bg-success" />
              </div>
              <div className="rounded-lg bg-muted p-3 leading-relaxed">
                <div><span className="text-primary-glow">const</span> <span className="text-cta">منصتي</span> = {'{'}</div>
                <div className="pl-4">name: <span className="text-success">"مشاركة"</span>,</div>
                <div className="pl-4">lang: <span className="text-success">"العربية"</span>,</div>
                <div className="pl-4">free: <span className="text-cta">true</span></div>
                <div>{'}'};</div>
              </div>
              <div className="rounded-lg bg-primary text-primary-foreground p-3">
                <div className="text-secondary"># تشغيل المشروع</div>
                <div>$ npm run dev</div>
                <div className="text-success">✓ ready in 1.2s</div>
              </div>
              <div className="rounded-lg border border-border p-3">
                <div className="text-muted-foreground">// مرحباً بك أيها المطوّر 👋</div>
                <div><span className="text-primary-glow">function</span> <span className="text-cta">share</span>(code) {'{'}</div>
                <div className="pl-4">return community.love;</div>
                <div>{'}'}</div>
              </div>
            </div>

            {/* floating badges */}
            <div className="absolute -left-6 top-24 px-3 py-2 rounded-xl bg-secondary text-secondary-foreground text-xs font-bold shadow-glow animate-float">
              HTML
            </div>
            <div className="absolute -right-4 top-48 px-3 py-2 rounded-xl bg-cta text-cta-foreground text-xs font-bold shadow-elegant animate-float [animation-delay:1s]">
              JS
            </div>
            <div className="absolute -left-4 bottom-24 px-3 py-2 rounded-xl bg-background text-primary text-xs font-bold shadow-elegant animate-float [animation-delay:2s]">
              CSS
            </div>
          </div>
        </div>
      </div>

    </section>
  );
};
