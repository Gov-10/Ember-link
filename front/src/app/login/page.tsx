"use client";

import { useState, useEffect } from "react";
import { signIn, fetchAuthSession } from "aws-amplify/auth";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LoginPage() {
  const router = useRouter();
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [animateIn, setAnimateIn] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setAnimateIn(true), 100);
    return () => clearTimeout(timer);
  }, []);

  const handleLogin = async () => {
    try {
      setLoading(true);
      await signIn({ username: phone, password });
      
      // 🔥 Getting the session to verify everything is synced
      const session = await fetchAuthSession();
      const token = session.tokens?.accessToken?.toString();

      // LocalStorage is fine for a hackathon, but session is handled by Amplify automatically
      if (token) localStorage.setItem("cognito_token", token);

      router.push("/dashboard");
    } catch (err: any) {
      alert(err.message || "Unauthorized Access: Invalid Credentials");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center text-white px-4 relative font-sans"
      style={{ backgroundImage: "url('/background-image.jpg')" }}
    >
      {/* Dark Overlay for that Tactical look */}
      <div className="absolute inset-0 bg-black/60 backdrop-blur-[2px]"></div>

      <div className="absolute top-1/2 left-10 transform -translate-y-1/2 flex flex-row gap-6 items-start z-10">
        <div
          className={`transition-all duration-1000 ease-in-out ${
            animateIn ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-20"
          } w-full max-w-md`}
        >
          {/* Header Branding */}
          <div className="mb-8 ml-2">
            <div className="flex items-center gap-3 mb-2">
                <div className="w-12 h-12 bg-red-700 rounded-lg flex items-center justify-center font-black text-2xl shadow-[0_0_30px_rgba(185,28,28,0.5)]">E</div>
                <h1 className="text-4xl font-black italic tracking-tighter uppercase">EmberLink</h1>
            </div>
            <p className="text-[10px] font-mono text-zinc-400 tracking-[0.3em] uppercase">Disaster Management Command</p>
          </div>

          {/* Login Card */}
          <div className="bg-zinc-900/90 backdrop-blur-2xl p-10 rounded-3xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] border border-white/10 transition-all hover:border-red-600/30">
            <h2 className="text-xl font-black uppercase tracking-widest mb-8 text-zinc-100 border-l-4 border-red-600 pl-4">Terminal Access</h2>

            <div className="space-y-5">
              <div>
                <label className="text-[10px] font-bold text-zinc-500 uppercase ml-1 mb-2 block">Operator Phone</label>
                <input
                  type="tel"
                  placeholder="+91 XXXXX XXXXX"
                  className="w-full px-5 py-4 bg-zinc-800/50 text-white rounded-2xl focus:outline-none focus:ring-2 focus:ring-red-600 border border-white/5 transition-all font-mono"
                  onChange={(e) => setPhone(e.target.value)}
                  value={phone}
                />
              </div>

              <div>
                <label className="text-[10px] font-bold text-zinc-500 uppercase ml-1 mb-2 block">Access Key</label>
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full px-5 py-4 bg-zinc-800/50 text-white rounded-2xl focus:outline-none focus:ring-2 focus:ring-red-600 border border-white/5 transition-all"
                  onChange={(e) => setPassword(e.target.value)}
                  value={password}
                />
              </div>

              <button
                onClick={handleLogin}
                disabled={loading}
                className={`w-full py-4 mt-4 rounded-2xl font-black uppercase tracking-[0.2em] text-white transition-all shadow-xl ${
                  loading
                    ? "bg-zinc-700 cursor-not-allowed opacity-50"
                    : "bg-red-700 hover:bg-red-600 hover:shadow-red-900/40 active:scale-95"
                }`}
              >
                {loading ? "Authorizing..." : "Initiate Session"}
              </button>

              <div className="pt-4 text-center">
                <p className="text-xs text-zinc-500">
                  New unit?{" "}
                  <Link href="/signup" className="text-red-500 font-bold hover:underline underline-offset-4">
                    Register Node
                  </Link>
                </p>
              </div>
            </div>
          </div>

          {/* Footer Info */}
          <div className="mt-8 flex gap-6 ml-4">
              <div className="flex flex-col">
                  <span className="text-[9px] text-zinc-600 font-bold uppercase">System Auth</span>
                  <span className="text-[10px] text-zinc-400 font-mono">v4.0.2-SECURE</span>
              </div>
              <div className="flex flex-col">
                  <span className="text-[9px] text-zinc-600 font-bold uppercase">Encryption</span>
                  <span className="text-[10px] text-zinc-400 font-mono">AES-256-GCM</span>
              </div>
          </div>
        </div>
      </div>
    </div>
  );
}
