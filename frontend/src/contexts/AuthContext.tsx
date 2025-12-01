import React, { createContext, useContext, useState, useEffect } from 'react';
import { login as apiLogin, register as apiRegister } from '@/services/api';

export type UserRole = 'Student' | 'Citizen' | 'NGO' | 'Government' | 'Other';

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  reportsSubmitted: number;
  cleanUpsJoined: number;
  nftsAdopted: number;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string, role: UserRole) => Promise<boolean>;
  signup: (email: string, password: string, name: string, role: UserRole) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Check for saved user in localStorage
    const savedUser = localStorage.getItem('aqua-guardian-user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const login = async (email: string, password: string, role: UserRole): Promise<boolean> => {
    try {
      const data = await apiLogin({ email, password });

      // Map Supabase session/user to our User interface
      // Note: Adjust this mapping based on your actual backend response structure
      if (data?.user || data?.session) {
        const sbUser = data.user || data.session.user;
        const newUser: User = {
          id: sbUser.id,
          email: sbUser.email || email,
          name: sbUser.user_metadata?.name || email.split('@')[0],
          role: role, // Role might need to be fetched from DB if not in metadata
          reportsSubmitted: 0, // You might want to fetch these stats separately
          cleanUpsJoined: 0,
          nftsAdopted: 0,
        };

        setUser(newUser);
        localStorage.setItem('aqua-guardian-user', JSON.stringify(newUser));
        return true;
      }
      return false;
    } catch (error) {
      console.error("Login failed:", error);
      return false;
    }
  };

  const signup = async (email: string, password: string, name: string, role: UserRole): Promise<boolean> => {
    try {
      const data = await apiRegister({ email, password, name });

      if (data?.user || data?.session) {
        const sbUser = data.user || data.session.user;
        const newUser: User = {
          id: sbUser.id,
          email: sbUser.email || email,
          name: name,
          role: role,
          reportsSubmitted: 0,
          cleanUpsJoined: 0,
          nftsAdopted: 0,
        };
        setUser(newUser);
        localStorage.setItem('aqua-guardian-user', JSON.stringify(newUser));
        return true;
      }
      return false;
    } catch (error) {
      console.error("Signup failed:", error);
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('aqua-guardian-user');
  };

  const value = {
    user,
    login,
    signup,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};