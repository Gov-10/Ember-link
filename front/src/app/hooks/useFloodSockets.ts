"use client";

import { useEffect, useRef, useState } from "react";

export const useFloodSocket = (region: string) => {
  const [data, setData] = useState<any>(null);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!region) return;

    const token = localStorage.getItem("access_token"); // JWT from Cognito

    const wsUrl = `ws://localhost:8000/ws/flood/${region}/?token=${token}`;

    const socket = new WebSocket(wsUrl);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("✅ WebSocket connected");
    };

    socket.onmessage = (event) => {
      const parsed = JSON.parse(event.data);
      console.log("📩 Incoming:", parsed);
      setData(parsed);
    };

    socket.onerror = (err) => {
      console.error("❌ WebSocket error:", err);
    };

    socket.onclose = () => {
      console.log("🔌 WebSocket closed");
    };

    return () => {
      socket.close();
    };
  }, [region]);

  return data;
};
