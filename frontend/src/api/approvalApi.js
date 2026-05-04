import api from "./client";

export async function createApprovalRequest(payload) {
    const { data } = await api.post("/approvals", payload);
    return data;
}

export async function getApprovals(params = {}) {
    const { data } = await api.get("/approvals", { params });
    return data;
}

export async function getApprovalById(requestId) {
    const { data } = await api.get(`/approvals/${requestId}`);
    return data;
}

export async function takeApprovalAction(requestId, payload) {
    const { data } = await api.post(`/approvals/${requestId}/action`, payload);
    return data;
}

export async function getApprovalHistory(requestId) {
    const { data } = await api.get(`/approvals/${requestId}/history`);
    return data;
}
