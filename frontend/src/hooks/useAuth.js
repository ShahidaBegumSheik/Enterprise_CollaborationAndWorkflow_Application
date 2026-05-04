import { useContext } from "react";
import { AuthContext } from "../api/context/AuthContext";

export default function useAuth() {
    return useContext(AuthContext);
}