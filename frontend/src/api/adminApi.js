import api from "./client";

export async function getAllUsers(params = {}) {
  const { data } = await api.get("/users/", { params });
  return data;
}

export async function createUser(payload) {
  const { data } = await api.post("/users/", payload);
  return data;
}

export async function updateUser(userId, payload) {
  const { data } = await api.put(`/users/${userId}`, payload);
  return data;
}

export async function deleteUser(userId) {
  const { data } = await api.delete(`/users/${userId}`);
  return data;
}

export async function getAuditLogs(params = {}) {
  const { data } = await api.get("/audit-logs", { params });
  return data;
}
