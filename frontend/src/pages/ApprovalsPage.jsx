import { useEffect, useState } from "react";
import AppLayout from "../components/layout/AppLayout";
import {
  createApprovalRequest,
  getApprovals,
  takeApprovalAction,
} from "../api/approvalApi";

const emptyForm = {
  request_type: "leave",
  title: "",
  description: "",
  amount: "",
  leave_from_date: "",
  leave_to_date: "",
  leave_duration: "full_day",
  leave_session: "forenoon",
};

function statusClass(status) {
  if (status === "approved") return "bg-emerald-100 text-emerald-700";
  if (status === "rejected") return "bg-rose-100 text-rose-700";
  if (status === "on_hold") return "bg-amber-100 text-amber-700";
  if (status === "pending_admin") return "bg-violet-100 text-violet-700";
  return "bg-sky-100 text-sky-700";
}

function formatDate(dateStr) {
  if (!dateStr || dateStr === "N/A") return "N/A";

  const date = new Date(dateStr);
  if (Number.isNaN(date.getTime())) return "N/A";

  return date.toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

function getLeaveDetail(description, label) {
  if (!description) return "N/A";

  const line = description
    .split("\n")
    .find((l) => l.trim().toLowerCase().startsWith(label.toLowerCase()));

  if (!line || !line.includes(":")) return "N/A";

  return line.substring(line.indexOf(":") + 1).trim();
}

function calculateDays(fromDate, toDate) {
  if (!fromDate || !toDate) return 1;

  const start = new Date(fromDate);
  const end = new Date(toDate);

  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) {
    return 1;
  }

  const diff = Math.floor((end - start) / (1000 * 60 * 60 * 24)) + 1;
  return diff > 0 ? diff : 1;
}

export default function ApprovalsPage() {
  const currentUser = JSON.parse(
    localStorage.getItem("enterprise_user") || "{}"
  );

  const [items, setItems] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadItems();
  }, []);

  useEffect(() => {
    if (
      form.leave_from_date &&
      form.leave_to_date &&
      form.leave_from_date !== form.leave_to_date
    ) {
      setForm((prev) => ({
        ...prev,
        leave_duration: "full_day",
      }));
    }
  }, [form.leave_from_date, form.leave_to_date]);



  async function loadItems() {
    try {
      const data = await getApprovals();
      setItems(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setError("Unable to load approvals");
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (form.request_type === "leave") {
      if (!form.leave_from_date) {
        setError("Please select leave from date");
        return;
      }

      if (!form.leave_to_date) {
        setError("Please select leave to date");
        return;
      }

      if (new Date(form.leave_to_date) < new Date(form.leave_from_date)) {
        setError("Leave to date cannot be before leave from date");
        return;
      }
    }

    const leaveDays = calculateDays(form.leave_from_date, form.leave_to_date);

    const leaveDescription =
      form.request_type === "leave"
        ? `${form.description}
Leave From Date: ${form.leave_from_date}
Leave To Date: ${form.leave_to_date}
Leave Duration: ${form.leave_duration}
Session: ${
            form.leave_duration === "half_day"
              ? form.leave_session
              : "Full Day"
          }`
        : form.description;

    const payload = {
      request_type: form.request_type,
      title: form.title,
      description: leaveDescription,
      amount:
        form.request_type === "leave"
          ? form.leave_duration === "half_day"
            ? 0.5
            : leaveDays
          : form.amount
          ? Number(form.amount)
          : null,
    };

    try {
      setLoading(true);
      await createApprovalRequest(payload);
      setForm(emptyForm);
      await loadItems();
    } catch (err) {
      console.error(err);
      setError("Unable to submit approval request");
    } finally {
      setLoading(false);
    }
  }

  async function handleAction(id, action) {
    const comment =
      window.prompt(`Comment for ${action}:`) || `${action} from UI`;

    try {
      await takeApprovalAction(id, { action, comment });
      await loadItems();
    } catch (err) {
      console.error(err);
      setError("Unable to update approval request");
    }
  }

  function canTakeAction(item) {
    const role = String(currentUser.role || "").toLowerCase();
    const status = String(item.status || "").toLowerCase().replaceAll(" ", "_");

    if (role === "employee") return false;
    if (role === "manager" && status === "pending_manager") return true;
    if (role === "admin" && status === "pending_admin") return true;

    return false;
  }

  function canTransferToAdmin(item) {
    const role = String(currentUser.role || "").toLowerCase();
    const status = String(item.status || "").toLowerCase().replaceAll(" ", "_");

    return role === "manager" && status === "pending_manager";
  }

  function displayStatusText(item) {
    if (item.status === "approved") return "Approved";
    if (item.status === "rejected") return "Rejected";
    if (item.status === "on_hold") return "On Hold";

    if (String(currentUser.role || "").toLowerCase() === "employee") {
      return "Waiting for approval";
    }

    return "No action available";
  }

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="rounded-4xl bg-linear-to-r from-violet-600 to-fuchsia-500 p-8 text-white shadow-2xl">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-white/75">
            Approval Workflow
          </p>
          <h2 className="mt-3 text-3xl font-black">
            Submit, review and track requests
          </h2>
        </div>

        {error && (
          <div className="rounded-2xl bg-rose-50 p-4 font-semibold text-rose-700">
            {error}
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          className="rounded-3xl bg-white p-6 shadow-xl"
        >
          <h3 className="mb-5 text-xl font-black text-slate-900">
            Submit Request
          </h3>

          <div className="grid gap-4 md:grid-cols-2">
            <select
              value={form.request_type}
              onChange={(e) =>
                setForm({ ...form, request_type: e.target.value })
              }
              className="rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-fuchsia-500 focus:ring-2"
            >
              <option value="leave">Leave</option>
              <option value="expense">Expense</option>
              <option value="purchase">Purchase</option>
              <option value="other">Other</option>
            </select>

            {form.request_type === "leave" ? (
              <div className="grid grid-cols-1 gap-3 md:grid-cols-4">
                <input
                  type="date"
                  required
                  title="Leave From Date"
                  value={form.leave_from_date}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      leave_from_date: e.target.value,
                      leave_to_date: form.leave_to_date || e.target.value,
                    })
                  }
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-fuchsia-500 focus:ring-2"
                />

                <input
                  type="date"
                  required
                  title="Leave To Date"
                  value={form.leave_to_date}
                  onChange={(e) =>
                    setForm({ ...form, leave_to_date: e.target.value })
                  }
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-fuchsia-500 focus:ring-2"
                />

                <select
                  value={form.leave_duration}
                  onChange={(e) =>
                    setForm({ ...form, leave_duration: e.target.value })
                  }
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-fuchsia-500 focus:ring-2"
                >
                  <option value="full_day">Full Day</option>

                  {form.leave_from_date === form.leave_to_date && (
                    <option value="half_day">Half Day</option>
                  )}
                </select>

                {form.leave_duration === "half_day" && (
                  <select
                    value={form.leave_session}
                    onChange={(e) =>
                      setForm({ ...form, leave_session: e.target.value })
                    }
                    className="rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-fuchsia-500 focus:ring-2"
                  >
                    <option value="forenoon">Forenoon</option>
                    <option value="afternoon">Afternoon</option>
                  </select>
                )}
              </div>
            ) : (
              <input
                className="rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-fuchsia-500 focus:ring-2"
                placeholder="Amount / value"
                value={form.amount}
                onChange={(e) => setForm({ ...form, amount: e.target.value })}
              />
            )}

            <input
              placeholder="Request title"
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              className="rounded-2xl border border-slate-200 bg-slate-50 p-3 md:col-span-2 outline-none ring-fuchsia-500 focus:ring-2"
              required
            />

            <textarea
              placeholder="Description"
              value={form.description}
              onChange={(e) =>
                setForm({ ...form, description: e.target.value })
              }
              className="rounded-2xl border border-slate-200 bg-slate-50 p-3 md:col-span-2 outline-none ring-fuchsia-500 focus:ring-2"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="mt-5 rounded-2xl bg-violet-600 px-6 py-3 font-black text-white shadow-lg shadow-violet-600/25 hover:bg-violet-700 disabled:opacity-60"
          >
            {loading ? "Submitting..." : "Submit Request"}
          </button>
        </form>

        <div className="space-y-4">
          {items.map((item) => {
            const leaveFromDate = getLeaveDetail(
              item.description,
              "Leave From Date"
            );
            const leaveToDate = getLeaveDetail(
              item.description,
              "Leave To Date"
            );
            const leaveDuration = getLeaveDetail(
              item.description,
              "Leave Duration"
            );
            const leaveSession = getLeaveDetail(item.description, "Session");
            const reason = item.description?.split("\n")[0]?.trim();

            return (
              <div key={item.id} className="rounded-3xl bg-white p-5 shadow-xl">
                <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="text-lg font-black text-slate-900">
                        {item.title}
                      </h3>
                      <span
                        className={`rounded-full px-3 py-1 text-xs font-black uppercase ${statusClass(
                          item.status
                        )}`}
                      >
                        {item.status}
                      </span>
                    </div>

                    {item.request_type === "leave" ? (
                      <div className="mt-2 space-y-1 text-sm text-slate-600">
                        <p>📅 From: {formatDate(leaveFromDate)}</p>
                        <p>📅 To: {formatDate(leaveToDate)}</p>
                        <p>
                          ⏱ Duration: {" "}
                          {leaveDuration === "half_day"
                            ? "Half Day"
                            : `${item.amount || 1} Day(s)`}
                        </p>

                        {leaveDuration === "half_day" && (
                          <p>🕒 Session: {leaveSession}</p>
                        )}

                        {reason && (
                          <p className="italic text-slate-500">"{reason}"</p>
                        )}
                      </div>
                    ) : (
                      <p className="mt-2 text-sm text-slate-500">
                        Amount: {item.amount}
                      </p>
                    )}
                  </div>

                  {canTakeAction(item) ? (
                    <div className="flex flex-wrap gap-2">
                      <button
                        type="button"
                        onClick={() => handleAction(item.id, "approve")}
                        className="rounded-2xl bg-emerald-500 px-4 py-2 text-sm font-black text-white hover:bg-emerald-600"
                      >
                        Approve
                      </button>

                      <button
                        type="button"
                        onClick={() => handleAction(item.id, "reject")}
                        className="rounded-2xl bg-rose-500 px-4 py-2 text-sm font-black text-white hover:bg-rose-600"
                      >
                        Reject
                      </button>

                      <button
                        type="button"
                        onClick={() => handleAction(item.id, "hold")}
                        className="rounded-2xl bg-amber-400 px-4 py-2 text-sm font-black text-slate-900 hover:bg-amber-500"
                      >
                        Hold
                      </button>

                      {canTransferToAdmin(item) && (
                        <button
                          type="button"
                          onClick={() => handleAction(item.id, "transfer_admin")}
                          className="rounded-2xl bg-violet-600 px-4 py-2 text-sm font-black text-white hover:bg-violet-700"
                        >
                          Transfer to Admin
                        </button>
                      )}
                    </div>
                  ) : (
                    <span className="rounded-2xl bg-slate-100 px-4 py-2 text-sm font-bold text-slate-600">
                      {displayStatusText(item)}
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AppLayout>
  );
}
