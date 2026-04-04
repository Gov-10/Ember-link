"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { signUp, confirmSignUp } from "aws-amplify/auth";

export default function SignupPage() {
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [address, setAddress] = useState("");
  const [isNgo, setIsNgo] = useState(false); // 🔥 New state for Role
  const [code, setCode] = useState("");
  const [step, setStep] = useState<"signup" | "confirm">("signup");
  const [loading, setLoading] = useState(false);
  const [animateIn, setAnimateIn] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const timer = setTimeout(() => setAnimateIn(true), 100);
    return () => clearTimeout(timer);
  }, []);

  const handleSignup = async () => {
    try {
      setLoading(true);
      await signUp({
        username: phone,
        password,
        options: { 
          userAttributes: { 
            phone_number: phone, 
            address: address,
            "custom:role": isNgo ? "ngo" : "user" // 🔥 Sending role to Cognito
          } 
        },
      });
      setStep("confirm");
    } catch (err: any) {
      alert(err.message || "Error signing up");
    } finally {
      setLoading(false);
    }
  };

  const handleConfirm = async () => {
    try {
      setLoading(true);
      await confirmSignUp({ username: phone, confirmationCode: code });
      alert("✅ Signup confirmed! Redirecting to login...");
      setTimeout(() => router.push("/login"), 1500);
    } catch (err: any) {
      alert(err.message || "Error confirming signup");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center text-white px-4 relative font-sans"
      style={{ backgroundImage: "url('/background-image.jpg')" }}
    >
      {/* Overlay for better readability */}
      <div className="absolute inset-0 bg-black/40 backdrop-grayscale-[0.5]"></div>

      <div className="absolute top-1/2 left-10 transform -translate-y-1/2 flex gap-6 items-start z-10">
        <div
          className={`transition-all duration-700 ease-out ${
            animateIn ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-10"
          } w-full max-w-md`}
        >
          <div className="bg-gray-900/80 backdrop-blur-xl p-8 rounded-2xl shadow-[0_0_50px_rgba(0,0,0,0.5)] border border-white/10 text-white">
            <div className="mb-8">
                <h2 className="text-4xl font-black tracking-tighter italic uppercase text-red-600">Join EmberLink</h2>
                <p className="text-xs text-gray-400 font-mono tracking-widest mt-1">ESTABLISHING_NEW_NODE...</p>
            </div>

            {step === "signup" && (
              <div className="space-y-4">
                <input
                  type="tel"
                  placeholder="Phone (e.g. +91...)"
                  className="w-full px-4 py-3 bg-gray-800/50 border border-white/5 text-white rounded-xl focus:ring-2 focus:ring-red-600 outline-none transition-all"
                  onChange={(e) => setPhone(e.target.value)}
                  value={phone}
                />
                <input
                  type="password"
                  placeholder="Password"
                  className="w-full px-4 py-3 bg-gray-800/50 border border-white/5 text-white rounded-xl focus:ring-2 focus:ring-red-600 outline-none transition-all"
                  onChange={(e) => setPassword(e.target.value)}
                  value={password}
                />
                <input
                  type="text"
                  placeholder="Address (City / Region)"
                  className="w-full px-4 py-3 bg-gray-800/50 border border-white/5 text-white rounded-xl focus:ring-2 focus:ring-red-600 outline-none transition-all"
                  onChange={(e) => setAddress(e.target.value)}
                  value={address}
                />

                {/* 🔥 Role Selection Toggle */}
                <div className="py-2">
                    <label className="flex items-center gap-3 cursor-pointer group">
                        <div className="relative">
                            <input 
                                type="checkbox" 
                                className="sr-only" 
                                checked={isNgo}
                                onChange={(e) => setIsNgo(e.target.checked)}
                            />
                            <div className={`w-12 h-6 rounded-full transition-colors ${isNgo ? 'bg-red-600' : 'bg-gray-700'}`}></div>
                            <div className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${isNgo ? 'translate-x-6' : 'translate-x-0'}`}></div>
                        </div>
                        <span className="text-xs font-bold uppercase tracking-widest text-gray-300 group-hover:text-white transition-colors">
                            {isNgo ? "Registering as NGO / Responder" : "Registering as Citizen"}
                        </span>
                    </label>
                </div>

                <button
                  onClick={handleSignup}
                  disabled={loading}
                  className={`w-full py-4 rounded-xl font-black uppercase tracking-widest text-white shadow-2xl transition-all
                    ${loading ? "bg-gray-700 cursor-not-allowed" : "bg-red-700 hover:bg-red-600 hover:scale-[1.02] active:scale-95 shadow-red-900/20"}`}
                >
                  {loading ? "Initializing..." : "Create Node"}
                </button>
              </div>
            )}

            {step === "confirm" && (
              <div className="space-y-6">
                <div className="text-center">
                    <p className="text-xs font-mono text-red-500 mb-2 tracking-widest animate-pulse">VERIFICATION_REQUIRED</p>
                    <p className="text-sm text-gray-400">Enter the code sent to your device.</p>
                </div>
                <input
                  type="text"
                  placeholder="6-Digit Code"
                  className="w-full px-4 py-4 bg-gray-800/50 border border-white/5 text-center text-2xl font-black tracking-[0.5em] text-white rounded-xl focus:ring-2 focus:ring-green-600 outline-none transition-all"
                  onChange={(e) => setCode(e.target.value)}
                  value={code}
                />
                <button
                  onClick={handleConfirm}
                  disabled={loading}
                  className={`w-full py-4 rounded-xl font-black uppercase tracking-widest text-white shadow-2xl transition-all
                    ${loading ? "bg-gray-700 cursor-not-allowed" : "bg-green-700 hover:bg-green-600 hover:scale-[1.02] shadow-green-900/20"}`}
                >
                  {loading ? "Verifying..." : "Confirm Node"}
                </button>
              </div>
            )}
          </div>
          
          <p className="mt-6 text-center text-[10px] text-gray-500 font-mono tracking-tighter uppercase">
            EmberLink v2.0 // Secure Distributed Disaster Response Network
          </p>
        </div>
      </div>
    </div>
  );
}
