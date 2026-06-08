import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { getCurrentUser } from "../api/authApi";

export default function OAuthSuccessPage() {
  const [params] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    async function completeLogin() {
      try {
        const token = params.get("access_token") || params.get("token");
        const refreshToken = params.get("refresh_token");

        if (!token) {
          navigate("/login", { replace: true });
          return;
        }

        localStorage.setItem("enterprise_access_token", token);

        if (refreshToken) {
          localStorage.setItem("enterprise_refresh_token", refreshToken);
        }

        const user = await getCurrentUser();
        localStorage.setItem("enterprise_user", JSON.stringify(user));

        window.location.replace("/dashboard");
      } catch (error) {
        console.error("Google login failed:", error);

        localStorage.removeItem("enterprise_access_token");
        localStorage.removeItem("enterprise_refresh_token");
        localStorage.removeItem("enterprise_user");

        navigate("/login", { replace: true });
      }
    }

    completeLogin();
  }, [params, navigate]);

  return <div className="p-6 font-bold">Signing in with Google...</div>;
}