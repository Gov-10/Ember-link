"use client";

import { useFloodSocket } from "@/app/hooks/useFloodSockets";
import { useState, useEffect } from "react";
import { signOut, fetchAuthSession } from "aws-amplify/auth";
import { useRouter } from "next/navigation";
import dynamicImport from "next/dynamic";
// 🔥 Toast Import
import toast, { Toaster } from "react-hot-toast";

const MapContainer = dynamicImport(() => import("react-leaflet").then((m) => m.MapContainer), { ssr: false });
const TileLayer = dynamicImport(() => import("react-leaflet").then((m) => m.TileLayer), { ssr: false });
const Marker = dynamicImport(() => import("react-leaflet").then((m) => m.Marker), { ssr: false });
const Popup = dynamicImport(() => import("react-leaflet").then((m) => m.Popup), { ssr: false });
const Polyline = dynamicImport(() => import("react-leaflet").then((m) => m.Polyline), { ssr: false });

import "leaflet/dist/leaflet.css";

export default function Dashboard() {
  const router = useRouter();
  const region = "haridwar"; 
  const [userProfile, setUserProfile] = useState<any>(null);
  const [allShelters, setAllShelters] = useState<any[]>([]);
  const [allNgos, setAllNgos] = useState([]);
  const [isClient, setIsClient] = useState(false);
  const [nearestShelter, setNearestShelter] = useState<any>(null);
  const [userCoords, setUserCoords] = useState<[number, number] | null>(null);
  const [distanceText, setDistanceText] = useState("Calculating...");

  const { data, isConnected } = useFloodSocket(region);
  const haridwarCenter: [number, number] = [29.9457, 78.1642];

  const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number) => {
    const R = 6371; 
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  };

  // 🔥 SMS Simulation Logic
  useEffect(() => {
    if (data && data.risk_level === "HIGH") {
      // 1. Alert Toast
      toast.error(`EMERGENCY: High Risk Detected in ${region.toUpperCase()}!`, {
        duration: 4000,
        style: { background: '#7f1d1d', color: '#fff', fontWeight: 'bold', border: '1px solid #dc2626' }
      });

      // 2. Simulate SMS Sending after a small delay
      setTimeout(() => {
        toast.success(`SMS Alert Dispatched to regional units via Twilio Gateway`, {
            icon: '📡',
            duration: 3000,
            style: { background: '#18181b', color: '#10b981', fontSize: '12px', border: '1px solid #065f46' }
        });
      }, 1500);
    }
  }, [data]);

  useEffect(() => {
    setIsClient(true);
    const fixIcons = async () => {
      const L = (await import("leaflet")).default;
      // @ts-ignore
      delete L.Icon.Default.prototype._getIconUrl;
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
        iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
        shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
      });
    };
    fixIcons();

    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition((pos) => {
        setUserCoords([pos.coords.latitude, pos.coords.longitude]);
      });
    }

    const fetchData = async () => {
      try {
        const session = await fetchAuthSession();
        const token = session.tokens?.accessToken?.toString();
        const baseUrl = "http://127.0.0.1:8000/api";
        const headers = { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" };

        const [pRes, sRes, nRes] = await Promise.all([
          fetch(`${baseUrl}/profile`, { method: "GET", headers }),
          fetch(`${baseUrl}/shelters?region=${region}`, { method: "GET" }),
          fetch(`${baseUrl}/ngos`, { method: "GET" })
        ]);

        if (pRes.ok) setUserProfile(await pRes.json());
        if (sRes.ok) setAllShelters(await sRes.json());
        if (nRes.ok) setAllNgos(await nRes.json());
      } catch (err) { console.error(err); }
    };
    fetchData();
  }, []);

  useEffect(() => {
    if (userCoords && allShelters.length > 0) {
      const sorted = allShelters.map(s => ({
        ...s,
        dist: calculateDistance(userCoords[0], userCoords[1], s.latitude, s.longitude)
      })).sort((a, b) => a.dist - b.dist);
      setNearestShelter(sorted[0]);
      setDistanceText(`${sorted[0].dist.toFixed(2)} KM`);
    }
  }, [userCoords, allShelters]);

  const handleLogout = async () => {
    await signOut();
    router.push("/");
  };

  if (!isClient) return <div className="h-screen bg-black flex items-center justify-center">...</div>;

  return (
    <div className="flex flex-col h-screen bg-black text-white overflow-hidden">
      {/* 🔥 Toast Container */}
      <Toaster position="top-right" reverseOrder={false} />

      {/* HEADER */}
      <header className="flex justify-between items-center px-8 py-4 border-b border-white/5 bg-zinc-950 z-30">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-red-700 rounded-xl flex items-center justify-center font-black text-xl shadow-[0_0_20px_rgba(185,28,28,0.4)]">E</div>
          <div>
            <h1 className="text-sm font-black tracking-tighter uppercase italic">EmberLink Live Intel</h1>
            <p className="text-[10px] text-zinc-500 font-mono italic">
                {isConnected ? ">>> SYSTEM_ONLINE" : ">>> LINK_OFFLINE"}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-6">
            <button onClick={handleLogout} className="bg-zinc-800 hover:bg-red-600 px-4 py-2 rounded-lg text-[10px] font-black transition-all uppercase">Abort Session</button>
        </div>
      </header>

      <main className="flex-1 flex overflow-hidden">
        {/* SIDEBAR */}
        <aside className="w-80 bg-zinc-950 border-r border-white/5 p-6 overflow-y-auto z-20">
          <div className="space-y-8">
            <section>
              <h3 className="text-[10px] font-bold text-zinc-600 uppercase mb-4 tracking-widest italic underline decoration-red-600/50 underline-offset-4">Live Threat Analyser</h3>
              <div className="p-5 bg-red-950/20 border border-red-600/30 rounded-3xl relative overflow-hidden group">
                <div className="absolute inset-0 bg-red-600/5 animate-pulse group-hover:bg-red-600/10 transition-all"></div>
                <p className="text-xs text-red-500 font-bold mb-1 uppercase tracking-tighter relative z-10">Risk Level</p>
                <p className="text-5xl font-black text-red-600 tracking-tighter relative z-10">{data?.risk_level || "STABLE"}</p>
              </div>
            </section>

            <section className="space-y-4">
              <div className="bg-zinc-900/80 p-5 rounded-2xl border border-white/5 hover:border-green-500/30 transition-all">
                <p className="text-[10px] text-zinc-500 font-bold uppercase mb-2">Extraction Point</p>
                <p className="text-xl font-black text-green-500 tracking-tight leading-none truncate">
                  {nearestShelter ? nearestShelter.name.toUpperCase() : "SCANNING..."}
                </p>
                <div className="flex items-center gap-2 mt-3">
                    <span className="text-[10px] bg-green-900/30 text-green-400 px-2 py-0.5 rounded font-mono border border-green-500/20">
                        {distanceText}
                    </span>
                    <span className="text-[10px] text-zinc-600 font-bold uppercase tracking-widest">Calculated</span>
                </div>
              </div>
              
              {/* Protocol Section */}
              <div className="p-5 bg-blue-900/10 border border-blue-500/20 rounded-2xl">
                <p className="text-[10px] font-black text-blue-500 uppercase mb-2">AI Protocol Agent</p>
                <p className="text-[11px] leading-relaxed text-blue-100/80 font-medium italic">
                  "{data?.instructions || "Monitoring satellite feed for anomalies. Standby for routing."}"
                </p>
              </div>
            </section>

            {/* NGO Section */}
            <section>
              <h3 className="text-[10px] font-bold text-zinc-600 uppercase mb-4 italic">Active Response Units</h3>
              <div className="space-y-2">
                {allNgos.length > 0 ? allNgos.slice(0, 3).map((n: any, i) => (
                  <div key={i} className="p-3 bg-zinc-900/30 rounded-xl border border-white/5 flex justify-between items-center group hover:bg-zinc-800/50 transition-all">
                    <span className="text-[10px] font-bold text-zinc-400 group-hover:text-white transition-colors uppercase">{n.org_name}</span>
                    <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></div>
                  </div>
                )) : <p className="text-[10px] text-zinc-700 italic font-mono uppercase tracking-widest">No units in range...</p>}
              </div>
            </section>
          </div>
        </aside>

        {/* MAP SECTION */}
        <section className="flex-1 relative bg-zinc-900 overflow-hidden">
          <MapContainer 
            center={haridwarCenter} 
            zoom={14} 
            className="h-full w-full"
            style={{ filter: "invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%)" }}
          >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            
            <Marker position={haridwarCenter}>
              <Popup>Impacted Area: Haridwar Hub</Popup>
            </Marker>

            {nearestShelter && (
              <Marker position={[nearestShelter.latitude, nearestShelter.longitude]}>
                <Popup className="font-bold">SAFE ZONE: {nearestShelter.name}</Popup>
              </Marker>
            )}

            <Polyline 
              positions={data?.route || (nearestShelter ? [haridwarCenter, [nearestShelter.latitude, nearestShelter.longitude]] : [])} 
              color="#dc2626" 
              weight={8} 
              opacity={0.8} 
              dashArray="10, 10"
            />
          </MapContainer>

          {/* HUD OVERLAY */}
          <div className="absolute bottom-8 left-8 bg-black/90 backdrop-blur-xl border-l-4 border-red-600 p-5 rounded-2xl z-[1000] max-w-xs shadow-2xl">
             <div className="flex items-center gap-2 mb-2 text-red-500 animate-pulse">
                <div className="w-2 h-2 bg-red-600 rounded-full"></div>
                <p className="text-[10px] font-black uppercase tracking-widest">Dijkstra Routing Active</p>
             </div>
             <p className="text-xs text-zinc-400 font-medium leading-relaxed">
                Calculating the safest path to <span className="text-white font-bold">{nearestShelter?.name || "Target"}</span> using Dijkstra's Algorithm on OSM data.
             </p>
          </div>
        </section>
      </main>
    </div>
  );
}
