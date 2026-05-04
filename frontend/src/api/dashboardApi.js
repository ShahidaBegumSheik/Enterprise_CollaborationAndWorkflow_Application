import api from "./client";

export async function getDashboardSummary() {
    const { data } = await api.get("/dashboard/summary");
    return data;
}

export async function getTaskAnalytics() {
    const { data } = await api.get("/dashboard/task-analytics");
    return data;
}

export async function getApprovalAnalytics() {
    const { data } = await api.get("/dashboard/approval-analytics");
    return data;
}