"use client";
import { fetchAuthSession } from "aws-amplify/auth";
import { useState, useRef, useEffect } from "react";

export const useFloodSocket = (region: string) => {
  const [data, setData] = useState<any>(null);
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!region) return;

    let isMounted = true;
    let reconnectionTimeout: NodeJS.Timeout;

    const connectSocket = async () => {
      try {
        // 1. Wait for the session to be truly ready
        const session = await fetchAuthSession({ forceRefresh: false });
        const token = session.tokens?.accessToken?.toString();
        console.log(token);

        if (!token) {
          console.warn("⏳ Auth session not ready, retrying...");
          reconnectionTimeout = setTimeout(connectSocket, 1000); // Retry in 1s
          return;
        }

        // 2. Prevent duplicate cleanup
        if (socketRef.current?.readyState === WebSocket.OPEN) return;

        const wsUrl = `ws://localhost:8000/ws/flood/${region}/?token=${token}`;
        const socket = new WebSocket(wsUrl);
        socketRef.current = socket;

        socket.onopen = () => {
          console.log("✅ WebSocket connected to", region);
          setIsConnected(true);
        };

        socket.onmessage = (event) => {
          if (!isMounted) return;
          console.log("📥 Raw event data:", event.data);
          try {
    const parsed = JSON.parse(event.data);
    console.log("✅ Parsed JSON:", parsed);
    setData(parsed);
  } catch (e) {
    console.error("❌ JSON Parse error:", e);
  }
        };

        socket.onclose = () => {
          setIsConnected(false);
          // Optional: Auto-reconnect logic here
        };

      } catch (err) {
        console.error("❌ Socket Auth Error:", err);
      }
    };

    connectSocket();

    return () => {
      isMounted = false;
      clearTimeout(reconnectionTimeout);
      socketRef.current?.close();
    };
  }, [region]);

  return { data, isConnected };
};
