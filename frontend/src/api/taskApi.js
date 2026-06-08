import api from "./client";

export async function createTask(payload) {
    const { data } = await api.post("/tasks", payload);
    return data;
}

export async function getTasks(params = {}) {
    const { data } = await api.get("/tasks", { params });
    return data;
}

export async function getTaskById(taskId) {
    const { data } = await api.get(`/tasks/${taskId}`);
    return data;
}

export async function updateTask(taskId, payload) {
    const { data } = await api.put(`/tasks/${taskId}`, payload);
    return data;
}

export async function updateTaskStatus(taskId, status) {
    const { data } = await api.put(`/tasks/${taskId}/status`, { status });
    return data;
}

export async function deleteTask(taskId) {
    const { data } = await api.delete(`/tasks/${taskId}`);
    return data;
}

export async function assignTask(taskId, assigneeId) {
    const { data } = await api.put(`/tasks/${taskId}`, { assignee_id: assigneeId });
    return data;
}
