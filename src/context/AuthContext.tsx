import React, { createContext, useContext, useState, useEffect, useRef, useCallback, type ReactNode } from 'react';

export type Role = 'admin' | 'teacher' | 'student';

export interface User {
  id: string;
  telegram_id: number;
  first_name: string;
  last_name: string;
  username: string;
  language_code: string;
  photo_url: string;
  role: Role;
}

export interface AdminProfile {
  id: string;
  user_id: string;
  avatar_url: string;
  bio: string;
  is_active: boolean;
}

export interface StudentProfile {
  id: string;
  user_id: string;
  coin_balance: number;
  total_coins_earned: number;
  total_coins_spent: number;
  avatar_url: string;
  bio: string;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  adminProfile: AdminProfile | null;
  studentProfile: StudentProfile | null;
  loading: boolean;
  error: string | null;
  logout: () => void;
  login: (
    token: string,
    user: User,
    adminProfile?: AdminProfile,
    studentProfile?: StudentProfile
  ) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [adminProfile, setAdminProfile] = useState<AdminProfile | null>(null);
  const [studentProfile, setStudentProfile] = useState<StudentProfile | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error] = useState<string | null>(null);
  const logoutTimer = useRef<number | null>(null);

  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    if (logoutTimer.current) {
      clearTimeout(logoutTimer.current);
      logoutTimer.current = null;
    }
  }, []);

  const parseJwt = (t: string) => {
    try {
      const parts = t.split('.');
      if (parts.length < 2) return null;
      const base64 = parts[1].replace(/-/g, '+').replace(/_/g, '/');
      const json = decodeURIComponent(atob(base64).split('').map((c) => {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));
      return JSON.parse(json);
    } catch {
      return null;
    }
  };

  const login = useCallback(
    (
      t: string,
      u: User,
      ap?: AdminProfile,
      sp?: StudentProfile
    ) => {
      setToken(t);
      setUser(u);
      setStudentProfile(sp || null);
      setAdminProfile(ap || null);
      try {
        localStorage.setItem('authToken', t);
        localStorage.setItem('user', JSON.stringify(u));
        if (sp) {
          localStorage.setItem('studentProfile', JSON.stringify(sp));
        }
        if (ap) {
          localStorage.setItem('adminProfile', JSON.stringify(ap));
        }
      } catch {
        // ignore
      }
    }, [setToken, setUser, setStudentProfile, setAdminProfile]);

  useEffect(() => {
    const onStorage = (e: StorageEvent) => {
      if (e.key === 'authToken') {
        const newToken = e.newValue;
        if (!newToken) {
          logout();
        } else {
          setToken(newToken);
        }
      }
      if (e.key === 'user') {
        try {
          const newUser = e.newValue ? JSON.parse(e.newValue) : null;
          setUser(newUser);
        } catch {
          // ignore
        }
      }
    };

    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, [logout]);

  useEffect(() => {
    if (!token) {
      if (logoutTimer.current) {
        clearTimeout(logoutTimer.current);
        logoutTimer.current = null;
      }
      return;
    }

    const payload = parseJwt(token);
    if (!payload || !payload.exp) {
      // invalid token — force logout
      logout();
      return;
    }

    const expMs = payload.exp * 1000;
    const now = Date.now();
    if (expMs <= now) {
      logout();
      return;
    }

    const msUntil = expMs - now;
    // clear existing timer
    if (logoutTimer.current) {
      clearTimeout(logoutTimer.current);
    }
    logoutTimer.current = window.setTimeout(() => {
      logout();
    }, msUntil) as unknown as number;

    return () => {
      if (logoutTimer.current) {
        clearTimeout(logoutTimer.current);
        logoutTimer.current = null;
      }
    };
  }, [token, logout]);

  return (
    <AuthContext.Provider value={{ user, token, loading, error, logout, login, studentProfile, adminProfile }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
