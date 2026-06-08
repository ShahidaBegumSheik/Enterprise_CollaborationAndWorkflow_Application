import api from "./client";

export async function getSubscription() {
  const { data } = await api.get("/billing/me");
  return data;
}

export async function checkoutPlan(plan) {
  const { data } = await api.post(`/billing/checkout/${plan}`);
  return data;
}

export async function verifyPayment(payload) {
  const { data } = await api.post("/billing/verify-payment", payload);
  return data;
}

