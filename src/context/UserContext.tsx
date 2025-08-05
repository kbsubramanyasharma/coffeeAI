import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface User {
  id: number;
  name: string;
}

interface UserContextProps {
  user: User | null;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
}

const UserContext = createContext<UserContextProps | undefined>(undefined);

export const UserProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  // Check for existing user data when component mounts
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const userName = localStorage.getItem('user_name');
    const userId = localStorage.getItem('user_id');
    
    if (token && userName && userId) {
      setUser({ id: parseInt(userId), name: userName });
    } else if (token && userId) {
      // Temporary fallback: if we have a token and user_id but no stored name
      // This could happen with existing users before this update
      setUser({ id: parseInt(userId), name: 'Coffee Lover' }); // Placeholder name
    }
  }, []);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};
