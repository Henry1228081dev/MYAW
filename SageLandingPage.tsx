import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Scissors, FileText, Sparkles, CheckCircle2, ChevronRight, Volume2 } from 'lucide-react';

/**
 * SAGE — THE VANGUARD DIVINE IMPLEMENTATION (v3.0)
 * 
 * Aesthetic: Luminous Vellum (Editorial)
 * Palette: Amber Warmth (#F59E0B)
 * Hook: Inline Image Typography
 */

// --- 1. CORE INFRASTRUCTURE & TEXTURE ---

const GrainOverlay = () => (
  <div className="fixed inset-0 pointer-events-none z-[999] opacity-[0.03] mix-blend-multiply overflow-hidden">
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
      <filter id="noise">
        <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch" />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width="100%" height="100%" filter="url(#noise)" />
    </svg>
  </div>
);

// --- 2. THE DIVINE HERO (INLINE TYPOGRAPHY) ---

const Hero = () => {
  const [currentWord, setCurrentWord] = useState(0);
  const words = ['mark schemes.', 'bad grades.', 'exam stress.', 'calculus.', 'confusion.'];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentWord((prev) => (prev + 1) % words.length);
    }, 2500);
    return () => clearInterval(timer);
  }, []);

  const springConfig = { type: "spring", stiffness: 100, damping: 20 };

  return (
    <section className="relative min-h-[100dvh] flex flex-col items-center justify-center pt-32 px-6 overflow-hidden bg-[#fdfbf7]">
      {/* Decorative Botanical Journal Elements */}
      <motion.img
        src="https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&q=80&w=400"
        initial={{ opacity: 0, x: -100, rotate: 30 }}
        whileInView={{ opacity: 0.1, x: 0, rotate: 45 }}
        transition={{ duration: 1.5, ease: [0.32, 0.72, 0, 1] }}
        className="absolute top-0 -left-20 w-64 grayscale sepia-[0.2] pointer-events-none select-none"
      />

      <div className="relative z-10 max-w-5xl w-full text-center space-y-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={springConfig}
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-[#F59E0B]/20 bg-[#F59E0B]/5 mb-4"
        >
          <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-[#F59E0B] font-mono">
            Adaptive Learning / 2025 Release
          </span>
        </motion.div>

        <h1 className="font-serif text-6xl md:text-[7rem] text-[#2f3327] leading-[0.85] tracking-tighter max-w-4xl mx-auto">
          <motion.span 
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...springConfig, delay: 0.1 }}
            className="flex flex-wrap justify-center items-center gap-x-4"
          >
            Stop
            <motion.div className="w-16 h-16 md:w-24 md:h-24 rounded-full overflow-hidden bg-[#F59E0B]/10 border border-[#F59E0B]/20 inline-block align-middle">
              <img src="https://images.unsplash.com/photo-1544377193-33dcf4d68fb5?auto=format&fit=crop&q=80&w=200" alt="" className="w-full h-full object-cover grayscale sepia-[0.3]" />
            </motion.div>
            crying over
          </motion.span>
          
          <div className="relative h-[1.1em] overflow-hidden mt-4">
            <AnimatePresence mode="wait">
              <motion.span
                key={currentWord}
                initial={{ y: "100%", opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                exit={{ y: "-100%", opacity: 0 }}
                transition={springConfig}
                className="absolute inset-0 italic text-[#F59E0B]"
              >
                {words[currentWord]}
              </motion.span>
            </AnimatePresence>
          </div>
        </h1>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.8 }}
          transition={{ duration: 1, delay: 0.5 }}
          className="max-w-xl mx-auto text-xl text-[#2f3327]/70 font-light leading-relaxed font-sans"
        >
          Sage is the AI tutor that nudges you toward the answer, 
          preserving the "aha!" moment. No spoilers. Just growth.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ ...springConfig, delay: 0.7 }}
          className="flex flex-wrap items-center justify-center gap-6 pt-8"
        >
          <button className="group relative px-10 py-4 rounded-full bg-[#F59E0B] text-[#fdfbf7] font-medium shadow-[0_20px_40px_-10px_rgba(245,158,11,0.3)] hover:scale-[1.05] active:scale-[0.98] transition-all duration-300 overflow-hidden">
            <span className="relative z-10 flex items-center gap-2">
              Start Studying <ChevronRight size={18} />
            </span>
          </motion.div>
          <button className="px-10 py-4 rounded-full bg-white/40 backdrop-blur-md text-[#2f3327] border border-[#2f3327]/10 font-medium hover:bg-white/60 transition-all duration-300">
            View Demo
          </button>
        </motion.div>
      </div>
    </section>
  );
};

// --- 3. THE DOUBLE-BEZEL SNIP TOOL ---

const SnipPreview = () => {
  return (
    <section className="py-24 px-6 flex flex-center bg-[#fdfbf7]">
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true }}
        transition={{ type: "spring", stiffness: 100, damping: 20 }}
        className="w-full max-w-5xl group"
      >
        {/* Outer Shell (Doppelrand Layer 1) */}
        <div className="bg-black/5 p-3 rounded-[3rem] border border-black/5 shadow-sm">
          {/* Inner Core (Doppelrand Layer 2) */}
          <div className="relative bg-white rounded-[calc(3rem-0.75rem)] overflow-hidden shadow-[inset_0_1px_1px_rgba(0,0,0,0.05),0_20px_40px_-10px_rgba(0,0,0,0.1)] min-h-[600px] flex items-center justify-center">
            <div className="absolute inset-0 opacity-20 pointer-events-none" 
                 style={{ backgroundImage: `radial-gradient(#F59E0B 1px, transparent 1px)`, backgroundSize: '24px 24px' }} />
            
            <div className="relative text-center space-y-6">
              <div className="w-20 h-20 rounded-full bg-[#F59E0B]/10 flex items-center justify-center mx-auto text-[#F59E0B]">
                <Scissors size={32} />
              </div>
              <p className="font-mono text-xs uppercase tracking-[0.2em] text-[#2f3327]/40">
                Visual Hint Engine v1.0
              </p>
              <h3 className="font-serif text-3xl text-[#2f3327]">
                Snip any question.<br />Get a nudge.
              </h3>
            </div>
            
            {/* Interaction Cursor Simulation */}
            <motion.div 
              animate={{ 
                x: [0, 100, -50, 0],
                y: [0, -50, 100, 0]
              }}
              transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
              className="absolute w-12 h-12 border-2 border-dashed border-[#F59E0B] flex items-center justify-center pointer-events-none"
            >
              <div className="w-1 h-1 bg-[#F59E0B] rounded-full" />
            </motion.div>
          </div>
        </div>
      </motion.div>
    </section>
  );
};

// --- 4. THE AMBER PRICING ENGINE ---

const Pricing = () => {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  const plans = [
    { title: "Cram Pass", price: "$5", features: ["50 Visual Snips", "Socratic Hints"] },
    { title: "Sage Mode", price: "$10", features: ["Unlimited Snips", "Deep Logic"], popular: true }
  ];

  return (
    <section className="bg-[#2f3327] py-32 px-6 overflow-hidden">
      <div className="max-w-5xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {plans.map((plan, idx) => (
            <motion.div
              key={idx}
              onHoverStart={() => setHoveredIndex(idx)}
              onHoverEnd={() => setHoveredIndex(null)}
              animate={{
                opacity: hoveredIndex !== null && hoveredIndex !== idx ? 0.4 : 1,
                scale: hoveredIndex !== null && hoveredIndex !== idx ? 0.95 : 1,
                filter: hoveredIndex !== null && hoveredIndex !== idx ? "blur(4px)" : "blur(0px)"
              }}
              className={`relative p-12 rounded-[2.5rem] border border-white/10 ${
                plan.popular ? 'bg-white/10' : 'bg-transparent'
              } transition-all duration-500`}
            >
              <h4 className="font-serif text-3xl text-[#fdfbf7] mb-2">{plan.title}</h4>
              <div className="flex items-baseline gap-2 mb-8">
                <span className="text-5xl font-semibold text-[#fdfbf7]">{plan.price}</span>
                <span className="text-[#fdfbf7]/40 font-mono text-xs tracking-widest uppercase">/ month</span>
              </div>
              <ul className="space-y-4 mb-12">
                {plan.features.map((f, i) => (
                  <li key={i} className="flex items-center gap-3 text-[#fdfbf7]/60 font-light text-sm">
                    <CheckCircle2 size={16} className="text-[#F59E0B]" />
                    {f}
                  </li>
                ))}
              </ul>
              <button className={`w-full py-4 rounded-full font-medium transition-all ${
                plan.popular ? 'bg-[#F59E0B] text-white shadow-xl' : 'bg-white/5 text-white border border-white/10'
              }`}>
                Select Plan
              </button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default function SageDivinePage() {
  return (
    <div className="selection:bg-[#F59E0B] selection:text-white">
      <GrainOverlay />
      <Hero />
      <SnipPreview />
      <Pricing />
      <footer className="py-20 text-center bg-[#fdfbf7]">
        <p className="font-serif italic text-3xl text-[#2f3327]">Sage</p>
        <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-[#2f3327]/30 mt-6">
          © 2025 SAGE EDUCATIONAL ANALYTICS
        </p>
      </footer>
    </div>
  );
}
