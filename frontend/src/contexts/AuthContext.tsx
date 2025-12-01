import React, { createContext, useContext, useState, useEffect } from 'react';

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
  login: (email: string, password: string, role: UserRole) => boolean;
  signup: (email: string, password: string, name: string, role: UserRole) => boolean;
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

  const login = (email: string, password: string, role: UserRole): boolean => {
    // Mock authentication - in real app, this would call an API
    if (email && password) {
      const newUser: User = {
        // Use fixed ID that exists in DB for testing
        id: "2caf16d3-740d-47d9-b8ce-a96d07ec3387",
        email,
        name: email.split('@')[0],
        role,
        reportsSubmitted: Math.floor(Math.random() * 10),
        cleanUpsJoined: Math.floor(Math.random() * 5),
        nftsAdopted: Math.floor(Math.random() * 3),
      };
      setUser(newUser);
      localStorage.setItem('aqua-guardian-user', JSON.stringify(newUser));
      return true;
    }
    return false;
  };

  const signup = (email: string, password: string, name: string, role: UserRole): boolean => {
    // Mock signup - in real app, this would call an API
    if (email && password && name) {
      const newUser: User = {
        // Use fixed ID that exists in DB for testing
        id: "2caf16d3-740d-47d9-b8ce-a96d07ec3387",
        email,
        name,
        role,
        reportsSubmitted: 0,
        cleanUpsJoined: 0,
        nftsAdopted: 0,
      };
      setUser(newUser);
      localStorage.setItem('aqua-guardian-user', JSON.stringify(newUser));
      return true;
    }
    return false;
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