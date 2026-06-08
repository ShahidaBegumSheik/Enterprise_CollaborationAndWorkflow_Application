import { useEffect } from "react";

export default function useNotifications(onMessage) {
    useEffect(() => {
        const token = localStorage.getItem("enterprise_access_token");

        if (!token) return;

        const wsUrl = `ws://127.0.0.1:8000/api/v1/ws/notifications?token=${token}`;
        const socket = new WebSocket(wsUrl);

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            onMessage?.(data);
        };

        socket.onerror = (error) => {
            console.error("Websocket error:", error);
        };

        return () => {
            socket.close();
        };
    }, [onMessage]);
}