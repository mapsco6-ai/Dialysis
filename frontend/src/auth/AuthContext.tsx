import { createContext, useCallback, useEffect, useMemo, useState, type ReactNode } from "react";
import { jwtDecode } from "jwt-decode";
import { apiClient, tokenStorage } from "../api/client";
import type { Role } from "./roles";

interface TokenPayload {
  user_id: number;
  roles: Role[];
  full_name: string;
}

interface CurrentUser {
  id: number;
  fullName: string;
  roles: Role[];
}

interface AuthContextValue {
  user: CurrentUser | null;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  hasRole: (...roles: Role[]) => boolean;
}

export const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function decodeUser(accessToken: string): CurrentUser {
  const payload = jwtDecode<TokenPayload>(accessToken);
  return { id: payload.user_id, fullName: payload.full_name, roles: payload.roles };
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const access = tokenStorage.getAccess();
    if (access) {
      try {
        setUser(decodeUser(access));
      } catch {
        tokenStorage.clear();
      }
    }
    setIsLoading(false);
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    const response = await apiClient.post("/auth/login/", { username, password });
    const { access, refresh } = response.data;
    tokenStorage.set(access, refresh);
    setUser(decodeUser(access));
  }, []);

  const logout = useCallback(() => {
    tokenStorage.clear();
    setUser(null);
  }, []);

  const hasRole = useCallback(
    (...roles: Role[]) => !!user && (user.roles.includes("Admin") || roles.some((r) => user.roles.includes(r))),
    [user],
  );

  const value = useMemo(
    () => ({ user, isLoading, login, logout, hasRole }),
    [user, isLoading, login, logout, hasRole],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
