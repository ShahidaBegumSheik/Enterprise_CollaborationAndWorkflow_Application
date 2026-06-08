import api from "./client";

export async function getDepartments(params = {}) {
    const { data } = await api.get("/departments", { params });
    return data;
}

export async function createDepartment(payload) {
    const { data } = await api.post("/departments", payload);
    return data;
}

export async function updateDepartment(departmentId, payload) {
    const { data } = await api.put(`/departments/${departmentId}`, payload);
    return data;
}

export async function deleteDepartment(departmentId) {
    const { data } = await api.delete(`/departments/${departmentId}`);
    return data;
}

export async function getWorkspaces(params = {}) {
    const { data } = await api.get("/workspaces", { params });
    return data;
}

export async function createWorkspace(payload) {
    const { data } = await api.post("/workspaces", payload);
    return data;
}

export async function updateWorkspace(workspaceId, payload) {
    const { data } = await api.put(`/workspaces/${workspaceId}`, payload);
    return data;
}

export async function deleteWorkspace(workspaceId) {
    const { data } = await api.delete(`/workspaces/${workspaceId}`);
    return data;
}

