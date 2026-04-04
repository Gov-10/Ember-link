"use client";

import { useFloodSocket } from "@/app/hooks/useFloodSockets";
import { useState } from "react";
import { signOut } from "aws-amplify/auth";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const router = useRouter();
  const [region, setRegion] = useState("haridwar");
  
  const handleLogout = async () => {
    await signOut();
    router.push("/");
  };

  // 🔥 CRITICAL: Yahan destructuring zaroori hai!
  const { data, isConnected } = useFloodSocket(region);

  return (
    <div className="p-6 text-white bg-slate-900 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">🚨 Live Flood Dashboard</h1>
        <div className="flex items-center gap-4">
          <span className={isConnected ? "text-green-400" : "text-red-400"}>
            {isConnected ? "● Connected" : "● Offline"}
          </span>
          <button 
            onClick={handleLogout}
            className="bg-red-600 px-4 py-2 rounded hover:bg-red-700"
          >
            Logout
          </button>
        </div>
      </div>

      <select
        value={region}
        onChange={(e) => setRegion(e.target.value)}
        className="mb-8 text-black px-4 py-2 rounded-lg w-full max-w-xs"
      >
        <option value="dehradun">Dehradun</option>
        <option value="rishikesh">Rishikesh</option>
        <option value="haridwar">Haridwar</option>
      </select>

      {data ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Main Alert Card */}
          <div className="bg-gray-800 p-6 rounded-xl border-l-4 border-yellow-500 shadow-lg">
            <h2 className="text-xl font-semibold mb-4 text-yellow-500">Evacuation Details</h2>
            <div className="space-y-3">
              <p><strong>Risk Level:</strong> <span className="text-orange-400">{data.risk_level}</span></p>
              <p><strong>Target Shelter:</strong> {data.target_shelter}</p>
              <p><strong>Distance:</strong> {data.distance_m ? `${data.distance_m.toFixed(2)} meters` : "Calculating..."}</p>
              <div className="mt-4 p-3 bg-gray-700 rounded-lg italic text-gray-300">
                "{data.instructions}"
              </div>
            </div>
          </div>

          {/* NGO Action Card (The "aim" / AI Message) */}
          {data.ngo_data && data.ngo_data.length > 0 && (
            <div className="bg-gray-800 p-6 rounded-xl border-l-4 border-blue-500 shadow-lg">
              <h2 className="text-xl font-semibold mb-4 text-blue-400">NGO Mission (aim)</h2>
              {data.ngo_data.map((ngo: any, idx: number) => (
                <div key={idx} className="space-y-4">
                  <p className="text-sm text-gray-400">Phone: {ngo.ngo_phone}</p>
                  <div className="bg-slate-700 p-4 rounded text-sm whitespace-pre-wrap leading-relaxed">
                    {ngo.aim}
                  </div>
                  <div className="flex gap-4 text-xs font-bold uppercase tracking-wider">
                    <span className="bg-blue-900 px-2 py-1 rounded">Ambulances: {ngo.ambulances}</span>
                    <span className="bg-green-900 px-2 py-1 rounded">Food: {ngo.food_packets}</span>
                    <span className="bg-purple-900 px-2 py-1 rounded">Volunteers: {ngo.volunteers}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-20 bg-gray-800 rounded-xl animate-pulse">
          <p className="text-gray-400">📡 Listening for Haridwar flood sensors...</p>
        </div>
      )}
    </div>
  );
}
