import api from "./client";

export async function getTaskInsights() {
  const { data } = await api.get("/ai/task-insights");
  return data;
}

export async function getRecommendedAssignee() {
  const { data } = await api.get("/ai/recommend-assignee");
  return data;
}
