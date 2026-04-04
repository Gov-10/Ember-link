"use client";

import { useFloodSocket } from "@/app/hooks/useFloodSockets";
import { useState } from "react";

export default function Dashboard() {
  const [region, setRegion] = useState("dehradun");
  const data = useFloodSocket(region);

  return (
    <div className="p-6 text-white">
      <h1 className="text-2xl mb-4">🚨 Live Flood Dashboard</h1>

      <select
        value={region}
        onChange={(e) => setRegion(e.target.value)}
        className="mb-4 text-black px-3 py-2 rounded"
      >
        <option value="dehradun">Dehradun</option>
        <option value="rishikesh">Rishikesh</option>
        <option value="haridwar">Haridwar</option>
      </select>

      {data ? (
        <div className="bg-gray-800 p-4 rounded-lg">
          <p><strong>Risk:</strong> {data.risk_level}</p>
          <p><strong>Shelter:</strong> {data.target_shelter}</p>
          <p><strong>Distance:</strong> {data.distance_m} m</p>
          <p><strong>Instructions:</strong> {data.instructions}</p>
        </div>
      ) : (
        <p>Waiting for live updates...</p>
      )}
    </div>
  );
}
