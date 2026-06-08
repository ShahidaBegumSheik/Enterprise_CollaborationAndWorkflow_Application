import { Bell } from "lucide-react";
import { useEffect, useState } from "react";
import { useNotificationsContext } from "../../context/NotificationContext";
import {
  getNotifications,
  markNotificationRead,
  markAllNotificationsRead,
} from "../../api/notificationApi";

export default function NotificationBell() {
  const [open, setOpen] = useState(false);

  const {
    notifications,
    setNotifications,
    loadNotifications,
  } = useNotificationsContext();

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  useEffect(() => {
    loadNotifications();
  }, []);

  async function handleOpenNotifications() {
    const nextOpen = !open;
    setOpen(nextOpen);

    if (nextOpen) {
      const data = await getNotifications({ page: 1, size: 20 });
      setNotifications(data.items || []);
    }
  }

  async function handleMarkRead(notificationId) {
    await markNotificationRead(notificationId);

    setNotifications((prev) =>
      prev.map((n) =>
        n.id === notificationId ? { ...n, is_read: true } : n
      )
    );
  }

  async function handleMarkAllRead() {
    await markAllNotificationsRead();

    setNotifications((prev) =>
      prev.map((n) => ({ ...n, is_read: true }))
    );
  }

  return (
    <div className="relative">
      <button
        type="button"
        onClick={handleOpenNotifications}
        className="relative rounded-xl bg-slate-100 p-2 hover:bg-slate-200"
      >
        <Bell size={20} />

        {unreadCount > 0 && (
          <span className="absolute -right-2 -top-2 flex h-5 min-w-5 items-center justify-center rounded-full bg-red-600 px-1 text-xs font-bold text-white">
            {unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 z-50 mt-3 w-80 rounded-2xl border bg-white p-4 shadow-xl">
          <div className="mb-3 flex items-center justify-between">
            <h3 className="font-bold text-slate-900">Notifications</h3>

            {unreadCount > 0 && (
              <button
                type="button"
                onClick={handleMarkAllRead}
                className="text-xs font-semibold text-indigo-600 hover:underline"
              >
                Mark all as read
              </button>
            )}
          </div>

          {notifications.length === 0 ? (
            <p className="text-sm text-slate-500">No notifications</p>
          ) : (
            <div className="max-h-80 overflow-y-auto">
              {notifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`mb-2 rounded-xl p-3 ${
                    notification.is_read ? "bg-slate-50" : "bg-indigo-50"
                  }`}
                >
                  <p className="text-sm font-semibold text-slate-900">
                    {notification.title}
                  </p>

                  <p className="mt-1 text-xs text-slate-600">
                    {notification.message}
                  </p>

                  {!notification.is_read && (
                    <button
                      type="button"
                      onClick={() => handleMarkRead(notification.id)}
                      className="mt-2 text-xs font-semibold text-indigo-600 hover:underline"
                    >
                      Mark as read
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

