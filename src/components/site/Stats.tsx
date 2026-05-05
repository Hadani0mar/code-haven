const stats = [
  { value: "+8,500", label: "كود منشور" },
  { value: "+2,300", label: "مطوّر مسجّل" },
  { value: "+150K", label: "تنزيل ونسخ" },
  { value: "24/7", label: "مجتمع نشط" },
];

export const Stats = () => (
  <section className="py-14 bg-primary text-primary-foreground relative overflow-hidden">
    <div className="absolute inset-0 dot-pattern opacity-10" />
    <div className="container relative grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
      {stats.map((s) => (
        <div key={s.label}>
          <div className="text-3xl md:text-4xl font-black text-secondary">{s.value}</div>
          <div className="text-sm md:text-base text-primary-foreground/80 mt-1">{s.label}</div>
        </div>
      ))}
    </div>
  </section>
);
