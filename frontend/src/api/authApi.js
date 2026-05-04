import api from "./client";

export async function registerUser(payload) {
    const { data } = await api.post("/auth/register", payload);
    return data;
}

export async function loginUser(payload) {
    const formData = new URLSearchParams();
    formData.append("username", payload.email);
    formData.append("password", payload.password);

    const { data } = await api.post("/auth/login", formData, {
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
    });
    return data;
}

export async function getCurrentUser() {
    const { data } = await api.get("/auth/me");
    return data;
}

export async function updateProfile(payload) {
    const { data } = await api.patch("/auth/me", payload);
    return data;
}