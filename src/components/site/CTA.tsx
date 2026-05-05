import { Button } from "@/components/ui/button";

export const CTA = () => (
  <section id="about" className="py-20">
    <div className="container">
      <div className="relative overflow-hidden rounded-3xl bg-gradient-hero text-primary-foreground p-10 md:p-16 shadow-elegant">
        <div className="absolute inset-y-0 left-0 w-40 dot-pattern opacity-30" />
        <div className="absolute -bottom-20 -left-20 w-72 h-72 rounded-full bg-secondary/20 blur-3xl" />
        <div className="relative max-w-2xl">
          <h2 className="text-3xl md:text-5xl font-black leading-tight mb-4">
            جاهز لمشاركة <span className="text-secondary">إبداعك البرمجي</span> مع العالم؟
          </h2>
          <p className="text-primary-foreground/85 text-lg mb-8">
            انضم إلى آلاف المطورين العرب وابدأ بنشر أكوادك، ساعد غيرك واستفد من خبرات المجتمع.
          </p>
          <div className="flex flex-wrap gap-3">
            <Button variant="cta" size="xl">اشترك الآن لبدء المشاركة</Button>
            <Button variant="outlineOnDark" size="xl">تعرّف على المنصة</Button>
          </div>
        </div>
      </div>
    </div>
  </section>
);
