"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { signUp, confirmSignUp } from "aws-amplify/auth";

export default function SignupPage() {
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [address, setAddress] = useState("");
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
        options: { userAttributes: { phone_number: phone, address: address } },
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
      className="min-h-screen bg-cover bg-center text-white px-4 relative"
      style={{ backgroundImage: "url('/background-image.jpg')" }}
    >
      <div className="absolute top-1/2 left-10 transform -translate-y-1/2 flex gap-6 items-start">
        <div
          className={`transition-all duration-700 ease-out ${
            animateIn ? "opacity-100 scale-100" : "opacity-0 scale-95"
          } w-full max-w-md`}
        >
          <div className="bg-gray-800/70 backdrop-blur-md p-8 rounded-xl shadow-2xl border border-gray-700 text-white transition-transform duration-300 hover:scale-105 hover:shadow-[0_0_25px_rgba(255,255,255,0.3)]">
            <h2 className="text-3xl font-bold text-center mb-6 tracking-wide">Create Account</h2>

            {step === "signup" && (
              <>
                <input
                  type="tel"
                  placeholder="Phone"
                  className="w-full px-4 py-2 mb-4 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                  onChange={(e) => setPhone(e.target.value)}
                  value={phone}
                />
                <input
                  type="password"
                  placeholder="Password"
                  className="w-full px-4 py-2 mb-4 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                  onChange={(e) => setPassword(e.target.value)}
                  value={password}
                />
                <input
  type="text"
  placeholder="Address (City / Region)"
  className="w-full px-4 py-2 mb-4 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
  onChange={(e) => setAddress(e.target.value)}
  value={address}
/>
                <button
                  onClick={handleSignup}
                  disabled={loading}
                  className={`w-full py-2 rounded-xl font-semibold text-white bg-gradient-to-r from-blue-700 via-blue-600 to-blue-500 
                              shadow-lg border border-white/10 backdrop-blur-md transition-all duration-300 
                              ${loading ? "cursor-not-allowed opacity-60" : "hover:scale-105 hover:-translate-y-1 hover:shadow-[0_0_30px_rgba(59,130,246,0.6)] hover:brightness-110"}`}
                >
                  {loading ? "Signing Up..." : "Sign Up"}
                </button>
              </>
            )}

            {step === "confirm" && (
              <>
                <p className="text-sm mb-4 text-center">
                  Enter the verification code sent to your phone.
                </p>
                <input
                  type="text"
                  placeholder="Verification Code"
                  className="w-full px-4 py-2 mb-4 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition"
                  onChange={(e) => setCode(e.target.value)}
                  value={code}
                />
                <button
                  onClick={handleConfirm}
                  disabled={loading}
                  className={`w-full py-2 rounded-xl font-semibold text-white bg-gradient-to-r from-green-900 via-green-700 to-green-600 
                              shadow-lg border border-white/10 backdrop-blur-md transition-all duration-300 
                              ${loading ? "cursor-not-allowed opacity-60" : "hover:scale-105 hover:-translate-y-1 hover:shadow-[0_0_30px_rgba(0,255,0,0.4)] hover:brightness-110"}`}
                >
                  {loading ? "Verifying..." : "Confirm Account"}
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
