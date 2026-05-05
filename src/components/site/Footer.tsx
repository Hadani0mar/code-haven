import { Code2, Github, Twitter, Send } from "lucide-react";

export const Footer = () => (
  <footer className="bg-primary text-primary-foreground">
    <div className="container py-14 grid md:grid-cols-4 gap-10">
      <div className="md:col-span-2">
        <div className="flex items-center gap-2.5 mb-4">
          <div className="w-10 h-10 rounded-xl bg-secondary grid place-items-center">
            <Code2 className="w-5 h-5 text-primary" />
          </div>
          <div>
            <div className="font-extrabold text-lg">منصتي</div>
            <div className="text-[11px] text-primary-foreground/70">منصة ليبية لتبادل الأكواد</div>
          </div>
        </div>
        <p className="text-primary-foreground/75 text-sm max-w-md leading-relaxed">
          منصتي هي بوابة عربية لتبادل الأكواد البرمجية بين المطورين، حيث يمكنك نشر أكوادك أو
          الاستفادة من أكواد الآخرين بكل سهولة وبواجهة بسيطة وسريعة.
        </p>
      </div>

      <div>
        <h4 className="font-bold text-secondary mb-4">روابط سريعة</h4>
        <ul className="space-y-2 text-sm text-primary-foreground/80">
          <li><a href="#snippets" className="hover:text-secondary">الأكواد</a></li>
          <li><a href="#categories" className="hover:text-secondary">التصنيفات</a></li>
          <li><a href="#community" className="hover:text-secondary">المجتمع</a></li>
          <li><a href="#about" className="hover:text-secondary">عن المنصة</a></li>
        </ul>
      </div>

      <div>
        <h4 className="font-bold text-secondary mb-4">تابعنا</h4>
        <div className="flex gap-3">
          {[Github, Twitter, Send].map((Icon, i) => (
            <a key={i} href="#" className="w-10 h-10 rounded-full bg-primary-foreground/10 hover:bg-secondary hover:text-primary grid place-items-center transition-smooth">
              <Icon className="w-4 h-4" />
            </a>
          ))}
        </div>
        <p className="text-xs text-primary-foreground/60 mt-6">www.mansati.com</p>
      </div>
    </div>
    <div className="border-t border-primary-foreground/10">
      <div className="container py-5 text-center text-xs text-primary-foreground/70">
        © {new Date().getFullYear()} منصتي. جميع الحقوق محفوظة.
      </div>
    </div>
  </footer>
);
