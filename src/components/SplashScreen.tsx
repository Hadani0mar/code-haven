import { useEffect, useState } from "react";
import splashLogo from "@/assets/splash-logo.jpg";

interface Props {
  onDone: () => void;
}

export const SplashScreen = ({ onDone }: Props) => {
  const [progress, setProgress] = useState(0);
  const [hiding, setHiding] = useState(false);

  useEffect(() => {
    const start = Date.now();
    const duration = 10000;

    const interval = setInterval(() => {
      const elapsed = Date.now() - start;
      const pct = Math.min((elapsed / duration) * 100, 100);
      setProgress(pct);
      if (pct >= 100) {
        clearInterval(interval);
        setHiding(true);
        setTimeout(onDone, 600);
      }
    }, 50);

    return () => clearInterval(interval);
  }, [onDone]);

  return (
    <div
      className={`fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-gradient-hero transition-opacity duration-600 ${
        hiding ? "opacity-0 pointer-events-none" : "opacity-100"
      }`}
    >
      {/* dot pattern overlay */}
      <div className="absolute inset-0 dot-pattern opacity-20" />

      {/* glow ring */}
      <div className="relative mb-10">
        <div className="absolute inset-0 rounded-full bg-secondary/30 blur-3xl scale-150 animate-pulse" />
        <img
          src={splashLogo}
          alt="منصتي"
          className="relative w-52 h-52 object-contain drop-shadow-2xl animate-float"
        />
      </div>

      {/* progress bar */}
      <div className="w-56 flex flex-col items-center gap-3">
        <div className="w-full h-1.5 rounded-full bg-primary-foreground/20 overflow-hidden">
          <div
            className="h-full rounded-full bg-gradient-accent transition-all duration-100 ease-linear"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* dots animation */}
        <div className="flex gap-2">
          {[0, 1, 2].map((i) => (
            <span
              key={i}
              className="w-2 h-2 rounded-full bg-secondary animate-bounce"
              style={{ animationDelay: `${i * 150}ms` }}
            />
          ))}
        </div>

        <p className="text-primary-foreground/70 text-sm font-semibold tracking-wider">
          جاري التحميل...
        </p>
      </div>
    </div>
  );
};
