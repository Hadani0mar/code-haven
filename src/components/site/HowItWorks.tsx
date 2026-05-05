import { UserPlus, Search, Code2, Share2 } from "lucide-react";

const steps = [
  { icon: UserPlus, title: "أنشئ حسابك", desc: "سجّل مجاناً وانضم إلى مجتمع المطورين العرب." },
  { icon: Search, title: "ابحث عن الكود", desc: "تصفّح آلاف الأكواد المصنّفة حسب اللغة والتقنية." },
  { icon: Code2, title: "انسخ واستخدم", desc: "انسخ الكود مباشرة أو نزّل الملف وادمجه في مشروعك." },
  { icon: Share2, title: "شارك إبداعك", desc: "ارفع أكوادك الخاصة وساهم في إثراء المحتوى العربي." },
];

export const HowItWorks = () => (
  <section id="community" className="py-20 bg-muted/40">
    <div className="container">
      <div className="text-center max-w-2xl mx-auto mb-12">
        <p className="text-sm font-bold text-cta mb-2">كيف تعمل المنصة</p>
        <h2 className="text-3xl md:text-4xl font-black text-primary">ابدأ في 4 خطوات بسيطة</h2>
      </div>
      <div className="grid md:grid-cols-4 gap-6">
        {steps.map((s, i) => {
          const Icon = s.icon;
          return (
            <div key={s.title} className="relative bg-background rounded-2xl p-6 shadow-card-soft border border-border/60">
              <div className="absolute -top-4 right-6 w-9 h-9 rounded-full bg-secondary text-secondary-foreground grid place-items-center font-black text-sm shadow-glow">
                {i + 1}
              </div>
              <div className="w-12 h-12 rounded-xl bg-primary text-primary-foreground grid place-items-center mb-4">
                <Icon className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-lg text-primary mb-2">{s.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{s.desc}</p>
            </div>
          );
        })}
      </div>
    </div>
  </section>
);
