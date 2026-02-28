import { useNavigate } from "react-router-dom";
import { ArrowRight, Eye, Microscope, Activity, Cpu, Dna } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import AmbientGrid from "@/components/landing/AmbientGrid";
import ThemeToggle from "@/components/ThemeToggle";
import Typewriter from "typewriter-effect";

const Index = () => {
  const navigate = useNavigate();
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), 200);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="relative min-h-screen bg-background overflow-hidden flex flex-col">
      <AmbientGrid />

      {/* Scan line effect */}
      <div className="absolute inset-0 pointer-events-none z-[1]" style={{
        backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, hsl(var(--primary) / 0.01) 2px, hsl(var(--primary) / 0.01) 4px)',
      }} />

      {/* Top bar */}
      <header className="relative z-10 flex items-center justify-between px-8 py-5">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-2.5 h-2.5 rounded-full bg-primary animate-pulse-slow" />
            <div className="absolute inset-0 w-2.5 h-2.5 rounded-full bg-primary/30 animate-ping" />
          </div>
          <span className="font-mono text-xs tracking-[0.15em] text-muted-foreground uppercase">
            ELL Research System
          </span>
        </div>
        <div className="flex items-center gap-4">
          <ThemeToggle />
          <span className="research-badge">
            <span className="w-1.5 h-1.5 rounded-full bg-current" />
            Research Prototype · Phase 1
          </span>
        </div>
      </header>

      {/* Hero */}
      <main className="relative z-10 flex-1 flex flex-col items-center justify-center px-6 -mt-10">
        <div className={`max-w-4xl mx-auto text-center space-y-10 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>

          {/* Orbiting icons */}
          <div className="relative w-32 h-32 mx-auto mb-8">
            <div className="absolute inset-0 rounded-full border border-border/30 animate-[spin_20s_linear_infinite]">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 glass-panel p-2 rounded-lg glow-border">
                <Microscope className="w-4 h-4 text-primary" />
              </div>
              <div className="absolute -bottom-3 left-1/2 -translate-x-1/2 glass-panel p-2 rounded-lg">
                <Activity className="w-4 h-4 text-muted-foreground" />
              </div>
            </div>
            <div className="absolute inset-4 rounded-full border border-primary/10 animate-[spin_15s_linear_infinite_reverse]">
              <div className="absolute -right-3 top-1/2 -translate-y-1/2 glass-panel p-2 rounded-lg">
                <Eye className="w-4 h-4 text-muted-foreground" />
              </div>
              <div className="absolute -left-3 top-1/2 -translate-y-1/2 glass-panel p-2 rounded-lg">
                <Cpu className="w-4 h-4 text-muted-foreground" />
              </div>
            </div>
            <div className="absolute inset-[42%] rounded-full bg-primary/20 animate-pulse-slow" />
          </div>

          {/* Title with typewriter */}
          <div className="space-y-6">
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight leading-[1.05]">
              <span className="text-gradient-primary">Endoscopic Lesion</span>
              <br />
              <span className="text-foreground">Localization</span>
            </h1>

            <div className="h-8 flex items-center justify-center">
              <span className="font-mono text-sm text-muted-foreground">
                <Typewriter
                  options={{
                    strings: [
                      "Spatial Reasoning in Endoscopic Imaging",
                      "CLIP + SAM2 · Zero-Shot Detection",
                      "Visual Analysis · Dataset Exploration",
                      "Research Prototype · ITB Mucosal Lesion Detection",
                      "Unimodal → Multimodal Pipeline",
                    ],
                    autoStart: true,
                    loop: true,
                    delay: 40,
                    deleteSpeed: 20,
                  }}
                />
              </span>
            </div>

            <p className="text-base text-muted-foreground max-w-xl mx-auto leading-relaxed">
              An exploratory research interface for visual analysis and spatial
              reasoning in endoscopic imaging datasets.
            </p>
          </div>

          {/* Actions */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
            <button
              onClick={() => navigate("/workspace")}
              className="group relative glass-panel-strong glow-border-intense px-8 py-4 flex items-center gap-3 text-sm font-semibold text-primary hover:bg-primary/10 transition-all duration-500 overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <span className="relative z-10">Enter Research Workspace</span>
              <ArrowRight className="relative z-10 w-4 h-4 transition-transform duration-300 group-hover:translate-x-1.5" />
            </button>
            <button
              onClick={() => navigate("/workspace?tab=overview")}
              className="glass-panel px-8 py-4 flex items-center gap-3 text-sm font-medium text-muted-foreground hover:text-foreground hover:border-primary/20 transition-all duration-300"
            >
              <Dna className="w-4 h-4" />
              View System Overview
            </button>
          </div>

          {/* Disclaimer */}
          <p className="text-xs text-muted-foreground/50 font-mono pt-6 max-w-md mx-auto">
            For research and educational use only. Not intended for clinical
            diagnosis or medical decision-making.
          </p>
        </div>

        {/* Bottom decorative */}
        <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex items-center gap-6">
          <div className="w-20 h-px bg-gradient-to-r from-transparent to-primary/20" />
          <div className="flex items-center gap-3">
            {["Visual Analysis", "Spatial Reasoning", "Dataset Exploration"].map((t, i) => (
              <span key={t} className="font-mono text-[9px] tracking-[0.2em] text-muted-foreground/30 uppercase">
                {i > 0 && <span className="mr-3 text-primary/20">·</span>}
                {t}
              </span>
            ))}
          </div>
          <div className="w-20 h-px bg-gradient-to-l from-transparent to-primary/20" />
        </div>
      </main>
    </div>
  );
};

export default Index;
