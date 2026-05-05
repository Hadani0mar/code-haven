import { Code2, Search, Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";

const links = [
  { href: "#snippets", label: "الأكواد" },
  { href: "#categories", label: "التصنيفات" },
  { href: "#community", label: "المجتمع" },
  { href: "#about", label: "عن المنصة" },
];

export const Navbar = () => {
  const [open, setOpen] = useState(false);
  return (
    <header className="sticky top-0 z-50 backdrop-blur-lg bg-background/75 border-b border-border/60">
      <div className="container flex items-center justify-between h-16 md:h-20">
        <a href="#" className="flex items-center gap-2.5 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-hero grid place-items-center shadow-card-soft group-hover:shadow-glow transition-smooth">
            <Code2 className="w-5 h-5 text-secondary" />
          </div>
          <div className="leading-tight">
            <div className="font-extrabold text-lg text-primary">منصتي</div>
            <div className="text-[10px] text-muted-foreground -mt-0.5">منصة ليبية لتبادل الأكواد</div>
          </div>
        </a>

        <nav className="hidden md:flex items-center gap-7">
          {links.map((l) => (
            <a key={l.href} href={l.href} className="text-sm font-semibold text-foreground/80 hover:text-primary transition-smooth">
              {l.label}
            </a>
          ))}
        </nav>

        <div className="hidden md:flex items-center gap-3">
          <Button variant="ghost" size="icon" aria-label="بحث">
            <Search className="w-5 h-5" />
          </Button>
          <Button variant="cta" size="sm">اشترك الآن</Button>
        </div>

        <Button variant="ghost" size="icon" className="md:hidden" onClick={() => setOpen(!open)} aria-label="القائمة">
          <Menu />
        </Button>
      </div>

      {open && (
        <div className="md:hidden border-t border-border bg-background">
          <div className="container py-4 flex flex-col gap-3">
            {links.map((l) => (
              <a key={l.href} href={l.href} onClick={() => setOpen(false)} className="text-sm font-semibold py-2">
                {l.label}
              </a>
            ))}
            <Button variant="cta">اشترك الآن</Button>
          </div>
        </div>
      )}
    </header>
  );
};
