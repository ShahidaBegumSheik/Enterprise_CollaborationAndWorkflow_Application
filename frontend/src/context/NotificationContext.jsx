import { createContext, useContext, useEffect, useState } from "react";
import {
  getNotifications,
  markAllNotificationsRead,
} from "../api/notificationApi";

const NotificationContext = createContext();

export function NotificationProvider({ children }) {
  const [notifications, setNotifications] = useState([]);

  async function loadNotifications() {
    try {
      const data = await getNotifications({ page: 1, size: 20 });
      setNotifications(data.items || []);
    } catch (err) {
      console.error("Unable to load notifications", err);
    }
  }

  useEffect(() => {
    const token = localStorage.getItem("enterprise_access_token");

    if (!token) return;

    loadNotifications();

    const socket = new WebSocket(
      `ws://127.0.0.1:8000/api/v1/ws/notifications?token=${token}`
    );

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      setNotifications((prev) => [
        {
          id: data.id || Date.now(),
          title: data.title || "Notification",
          message: data.message,
          category: data.category || data.type,
          created_at: data.created_at || new Date().toISOString(),
          is_read: false,
        },
        ...prev,
      ]);
    };

    socket.onerror = (err) => {
      console.error("WebSocket error", err);
    };

    return () => {
      socket.close();
    };
  }, []);

  async function markAllAsRead() {
    try {
      await markAllNotificationsRead();
      setNotifications((prev) =>
        prev.map((n) => ({ ...n, is_read: true }))
      );
    } catch (err) {
      console.error("Unable to mark notifications read", err);
    }
  }

  return (
    <NotificationContext.Provider
      value={{
        notifications,
        setNotifications,
        markAllAsRead,
        loadNotifications,
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
}

export function useNotificationsContext() {
  return useContext(NotificationContext);
}

