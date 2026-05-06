import { FileCode2, Palette, Braces } from "lucide-react";

const cats = [
  { name: "HTML", icon: FileCode2, count: "1,240+", color: "bg-cta/10 text-cta" },
  { name: "CSS", icon: Palette, count: "980+", color: "bg-primary-glow/15 text-primary-glow" },
  { name: "JavaScript", icon: Braces, count: "2,150+", color: "bg-secondary/30 text-primary" },
];

export const Categories = () => {
  return (
    <section id="categories" className="py-20 bg-muted/40">
      <div className="container">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <p className="text-sm font-bold text-cta mb-2">التصنيفات</p>
          <h2 className="text-3xl md:text-4xl font-black text-primary mb-3">تصفّح الأكواد حسب التصنيف</h2>
          <p className="text-muted-foreground">اختر اللغة أو التقنية التي تهمك واستكشف آلاف الأكواد الجاهزة للاستخدام.</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {cats.map((c) => {
            const Icon = c.icon;
            return (
              <button key={c.name} className="group bg-background rounded-2xl p-5 text-right shadow-card-soft hover:shadow-elegant hover:-translate-y-1 transition-smooth border border-border/60">
                <div className={`w-12 h-12 rounded-xl grid place-items-center mb-4 ${c.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
                <div className="font-bold text-primary text-lg">{c.name}</div>
                <div className="text-xs text-muted-foreground mt-1">{c.count} كود</div>
              </button>
            );
          })}
        </div>
      </div>
    </section>
  );
};
