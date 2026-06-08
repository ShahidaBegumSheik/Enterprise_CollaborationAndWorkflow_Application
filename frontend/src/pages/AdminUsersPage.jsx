import { useEffect, useState, useCallback } from "react";
import {
  getAllUsers,
  createUser,
  updateUser,
  deleteUser,
} from "../api/adminApi";

export default function AdminUsersPage() {
  const currentUser = JSON.parse(localStorage.getItem("enterprise_user") || "{}");
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [showEdit, setShowEdit] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [toast, setToast] = useState(null);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [size] = useState(10);

  const [newUser, setNewUser] = useState({
    full_name: "",
    email: "",
    password: "",
    role: "employee",
  });

  const loadUsers = useCallback(async () => {
    try {
      const data = await getAllUsers({page, size});
      setUsers(Array.isArray(data.items) ? data.items : []);
    } catch (error) {
      console.error(error);
      showToast("Unable to load users", "error");
    }
  }, []);

  useEffect(() => {
    async function fetchUsers() {
          try {
            const data = await getAllUsers({page, size});
            setUsers(Array.isArray(data.items) ? data.items : []);
          } catch (err) {
            console.error(err);
            showToast("Unable to laod users", "error");
          }
        }
        fetchUsers();
  }, []);

  function showToast(message, type = "success") {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  }

  function getErrorMessage(error) {
    const detail = error?.response?.data?.detail;

    if (Array.isArray(detail)) {
      return detail.map((d) => d.msg).join(", ");
    }

    if (typeof detail === "string") {
      return detail;
    }

    if (error?.response?.status === 401) {
      return "Session expired. Please login again.";
    }

    if (error?.response?.status === 403) {
      return "Only admin can manage users.";
    }

    return "Something went wrong";
  }

  function validateCreateForm() {
    if (!newUser.full_name.trim()) return "Full name is required";
    if (!newUser.email.trim()) return "Email is required";
    if (!newUser.password.trim()) return "Password is required";
    return null;
  }

  async function handleCreate() {
    const validationError = validateCreateForm();
    if (validationError) {
      showToast(validationError, "error");
      return;
    }

    try {
      setLoading(true);
      await createUser(newUser);
      setShowCreate(false);
      setNewUser({ full_name: "", email: "", password: "", role: "employee" });
      showToast("User created successfully");
      await loadUsers();
    } catch (error) {
      console.error(error);
      showToast(getErrorMessage(error), "error");
    } finally {
      setLoading(false);
    }
  }

  async function handleUpdate() {
    try {
      setLoading(true);
      await updateUser(selectedUser.id, {
        full_name: selectedUser.full_name,
        email: selectedUser.email,
        role: selectedUser.role,
        department_id: selectedUser.department_id ?? null,
      });
      setShowEdit(false);
      showToast("User updated successfully");
      await loadUsers();
    } catch (error) {
      console.error(error);
      showToast(getErrorMessage(error), "error");
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(id) {
    if (!confirm("Delete this user?")) return;

    try {
      setLoading(true);
      await deleteUser(id);
      showToast("User deleted successfully");
      await loadUsers();
    } catch (error) {
      console.error(error);
      showToast(getErrorMessage(error), "error");
    } finally {
      setLoading(false);
    }
  }

  const roleColor = {
    admin: "bg-rose-100 text-rose-700 border-rose-200",
    manager: "bg-blue-100 text-blue-700 border-blue-200",
    employee: "bg-emerald-100 text-emerald-700 border-emerald-200",
  };

  return (
    <div className="w-full max-w-full">
      {toast && (
        <div
          className={`fixed right-6 top-6 z-50 rounded-2xl px-5 py-3 font-semibold text-white shadow-xl ${
            toast.type === "error" ? "bg-rose-600" : "bg-emerald-600"
          }`}
        >
          {toast.message}
        </div>
      )}

      <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm font-bold uppercase tracking-[0.25em] text-indigo-500">
            Admin Panel
          </p>
          <h1 className="mt-1 text-3xl font-black text-slate-900">
            User Management
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Create, edit, and manage Admins, Managers, and Employees.
          </p>
        </div>

        <button
          type="button"
          onClick={() => setShowCreate(true)}
          className="rounded-2xl bg-indigo-600 px-5 py-3 font-black text-white shadow-lg shadow-indigo-600/25 hover:bg-indigo-700 disabled:opacity-60"
          disabled={loading}
        >
          + Create User
        </button>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <StatCard title="Total Users" value={users.length} color="from-indigo-500 to-purple-600" />
        <StatCard title="Admins" value={users.filter((u) => u.role === "admin").length} color="from-rose-500 to-pink-600" />
        <StatCard title="Employees" value={users.filter((u) => u.role === "employee").length} color="from-emerald-500 to-teal-600" />
      </div>

      <div className="mt-6 overflow-x-auto rounded-2xl bg-white shadow ring-1 ring-slate-200">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-900 text-white">
            <tr>
              <th className="px-5 py-4">Name</th>
              <th className="px-5 py-4">Email</th>
              <th className="px-5 py-4">Role</th>
              <th className="px-5 py-4 text-center">Actions</th>
            </tr>
          </thead>

          <tbody>
            {users.map((user) => (
              <tr key={user.id} className="border-b border-slate-100 hover:bg-indigo-50">
                <td className="px-5 py-4 font-bold text-slate-800">
                  {user.full_name}
                </td>
                <td className="px-5 py-4 text-slate-600">{user.email}</td>
                <td className="px-5 py-4">
                  <span
                    className={`rounded-full border px-3 py-1 text-xs font-black ${
                      roleColor[user.role] || roleColor.employee
                    }`}
                  >
                    {user.role}
                  </span>
                </td>
                <td className="px-5 py-4 text-center">
                  <button
                    type="button"
                    onClick={() => {
                      setSelectedUser(user);
                      setShowEdit(true);
                    }}
                    className="mr-2 rounded-xl bg-blue-500 px-3 py-2 font-semibold text-white hover:bg-blue-600"
                  >
                    Edit
                  </button>

                  {Number(currentUser.id) !== Number(user.id) ? (
                    <button
                      type="button"
                      onClick={() => handleDelete(user.id)}
                      className="rounded-xl bg-rose-500 px-3 py-2 font-semibold text-white hover:bg-rose-600"
                    >
                      Delete
                    </button>
                  ) : (
                    <button
                      type="button"
                      disabled
                      className="rounded-xl bg-slate-300 px-3 py-2 font-semibold text-slate-500 cursor-not-allowed"
                    >
                      Current User
                    </button>
                  )}
                </td>
              </tr>
            ))}

            {users.length === 0 && (
              <tr>
                <td colSpan="4" className="px-5 py-10 text-center font-semibold text-slate-500">
                  No users found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {showCreate && (
        <Modal title="Create New User" onClose={() => setShowCreate(false)}>
          <Input label="Full Name" value={newUser.full_name} onChange={(value) => setNewUser({ ...newUser, full_name: value })} />
          <Input label="Email" value={newUser.email} onChange={(value) => setNewUser({ ...newUser, email: value })} />
          <Input label="Password" type="password" value={newUser.password} onChange={(value) => setNewUser({ ...newUser, password: value })} />
          <SelectRole value={newUser.role} onChange={(value) => setNewUser({ ...newUser, role: value })} />
          <button type="button" onClick={handleCreate} disabled={loading} className="mt-2 w-full rounded-2xl bg-indigo-600 py-3 font-black text-white hover:bg-indigo-700 disabled:opacity-60">
            {loading ? "Creating..." : "Create User"}
          </button>
        </Modal>
      )}

      {showEdit && selectedUser && (
        <Modal title="Edit User" onClose={() => setShowEdit(false)}>
          <Input label="Full Name" value={selectedUser.full_name || ""} onChange={(value) => setSelectedUser({ ...selectedUser, full_name: value })} />
          <Input label="Email" value={selectedUser.email || ""} onChange={(value) => setSelectedUser({ ...selectedUser, email: value })} />
          <SelectRole value={selectedUser.role} onChange={(value) => setSelectedUser({ ...selectedUser, role: value })} />
          <button type="button" onClick={handleUpdate} disabled={loading} className="mt-2 w-full rounded-2xl bg-blue-600 py-3 font-black text-white hover:bg-blue-700 disabled:opacity-60">
            {loading ? "Saving..." : "Save Changes"}
          </button>
        </Modal>
      )}
    </div>
  );
}

function StatCard({ title, value, color }) {
  return (
    <div className={`rounded-3xl bg-gradient-to-r ${color} p-5 text-white shadow-xl`}>
      <p className="text-sm font-semibold opacity-80">{title}</p>
      <h2 className="mt-2 text-4xl font-black">{value}</h2>
    </div>
  );
}

function Modal({ title, children, onClose }) {
  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/60 px-4 backdrop-blur-sm">
      <div className="w-full max-w-md rounded-4xl bg-white p-6 shadow-2xl">
        <div className="mb-5 flex items-center justify-between">
          <h2 className="text-xl font-black text-slate-900">{title}</h2>
          <button type="button" onClick={onClose} className="rounded-full bg-slate-100 px-3 py-1 font-bold text-slate-600 hover:bg-slate-200">
            ✕
          </button>
        </div>
        <div className="space-y-4">{children}</div>
      </div>
    </div>
  );
}

function Input({ label, value, onChange, type = "text" }) {
  return (
    <div>
      <label className="mb-1 block text-sm font-bold text-slate-600">{label}</label>
      <input type={type} value={value} onChange={(e) => onChange(e.target.value)} className="w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 outline-none ring-indigo-500 focus:ring-2" />
    </div>
  );
}

function SelectRole({ value, onChange }) {
  return (
    <div>
      <label className="mb-1 block text-sm font-bold text-slate-600">Role</label>
      <select value={value} onChange={(e) => onChange(e.target.value)} className="w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 outline-none ring-indigo-500 focus:ring-2">
        <option value="admin">Admin</option>
        <option value="manager">Manager</option>
        <option value="employee">Employee</option>
      </select>
    </div>
  );
}
