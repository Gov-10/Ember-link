import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white selection:bg-orange-500/30">
      {/* --- Navigation Bar --- */}
      <nav className="flex items-center justify-between px-8 py-6 backdrop-blur-md bg-black/50 sticky top-0 z-50 border-b border-white/10">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-orange-600 rounded-lg flex items-center justify-center font-bold text-white shadow-[0_0_15px_rgba(234,88,12,0.5)]">
            E
          </div>
          <span className="text-xl font-bold tracking-tighter">EMBERLINK</span>
        </div>
        <div className="flex gap-6 items-center">
          <Link href="/login" className="text-sm font-medium hover:text-orange-500 transition-colors">
            Login
          </Link>
          <Link 
            href="/signup" 
            className="bg-white text-black px-5 py-2 rounded-full text-sm font-bold hover:bg-orange-500 hover:text-white transition-all transform hover:scale-105 active:scale-95"
          >
            Get Started
          </Link>
        </div>
      </nav>

      {/* --- Hero Section --- */}
      <main className="relative flex flex-col items-center justify-center pt-24 pb-32 px-6 overflow-hidden">
        {/* Background Glows */}
        <div className="absolute top-1/4 -left-20 w-72 h-72 bg-orange-600/20 rounded-full blur-[120px]" />
        <div className="absolute bottom-0 -right-20 w-96 h-96 bg-blue-600/10 rounded-full blur-[150px]" />

        <div className="relative z-10 text-center max-w-4xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-500 text-xs font-bold mb-6 animate-pulse">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-orange-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-orange-500"></span>
            </span>
            LIVE: MONITORING HIMALAYAN REGION
          </div>

          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 leading-[1.1]">
            Minutes Matter in <br />
            <span className="bg-gradient-to-r from-orange-500 via-red-500 to-orange-600 bg-clip-text text-transparent">
              Disaster Response.
            </span>
          </h1>

          <p className="text-zinc-400 text-lg md:text-xl max-w-2xl mx-auto mb-12 leading-relaxed">
            EmberLink uses real-time sensor data and AI-driven route optimization to evacuate populations and coordinate NGOs during flood emergencies.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/signup"
              className="px-8 py-4 bg-orange-600 rounded-xl font-bold text-lg hover:bg-orange-700 shadow-[0_10px_20px_-10px_rgba(234,88,12,0.5)] transition-all"
            >
              Start Free Trial
            </Link>
            <Link 
              href="#features"
              className="px-8 py-4 bg-zinc-900 border border-white/10 rounded-xl font-bold text-lg hover:bg-zinc-800 transition-all"
            >
              Watch Demo
            </Link>
          </div>
        </div>

        {/* Mockup Preview */}
        <div className="mt-20 relative w-full max-w-5xl group">
          <div className="absolute inset-0 bg-orange-600/20 blur-3xl opacity-20 group-hover:opacity-40 transition-opacity" />
          <div className="relative border border-white/10 rounded-2xl bg-zinc-900/50 backdrop-blur-xl p-2 shadow-2xl">
            <div className="bg-zinc-950 rounded-xl overflow-hidden aspect-[16/9] flex items-center justify-center border border-white/5">
              {/* Placeholder for Dashboard Image/Video */}
              <div className="text-zinc-700 font-mono text-sm">
                [ LOADING REAL-TIME EVACUATION MAP... ]
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* --- Features Grid --- */}
      <section id="features" className="px-8 py-24 bg-zinc-950 border-t border-white/5">
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12">
          <div className="space-y-4">
            <div className="w-12 h-12 bg-orange-500/10 rounded-lg flex items-center justify-center text-orange-500">
              📍
            </div>
            <h3 className="text-xl font-bold">Dijkstra Mapping</h3>
            <p className="text-zinc-400 text-sm leading-relaxed">
              Real-time route calculation using OpenStreetMap data to find the safest path to shelters during floods.
            </p>
          </div>
          <div className="space-y-4">
            <div className="w-12 h-12 bg-blue-500/10 rounded-lg flex items-center justify-center text-blue-500">
              🤖
            </div>
            <h3 className="text-xl font-bold">AI Decision Maker</h3>
            <p className="text-zinc-400 text-sm leading-relaxed">
              LLMs automatically draft urgent SMS alerts and NGO logistics missions based on disaster severity.
            </p>
          </div>
          <div className="space-y-4">
            <div className="w-12 h-12 bg-green-500/10 rounded-lg flex items-center justify-center text-green-500">
              📡
            </div>
            <h3 className="text-xl font-bold">Live Sync</h3>
            <p className="text-zinc-400 text-sm leading-relaxed">
              Instant WebSocket updates ensure that NGOs and government officials stay synchronized in high-stress scenarios.
            </p>
          </div>
        </div>
      </section>

      {/* --- Footer --- */}
      <footer className="px-8 py-12 border-t border-white/5 text-center text-zinc-600 text-sm">
        <p>© 2026 EmberLink. Built for Global Disaster Resilience.</p>
      </footer>
    </div>
  );
}
