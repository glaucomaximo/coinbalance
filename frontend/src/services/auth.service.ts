import { apiClient } from '@/lib/api/client';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: string;
    username: string;
    email: string;
    role: string;
    permissions: string[];
  };
}

export interface UserInfo {
  id: string;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: number;
  last_login: number | null;
  permissions: string[];
}

export class AuthService {
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>(
      '/api/v1/auth/login',
      credentials
    );
    
    apiClient.setToken(response.access_token);
    
    return response;
  }

  async logout(): Promise<void> {
    try {
      await apiClient.post('/api/v1/auth/logout');
    } finally {
      apiClient.clearToken();
    }
  }

  async getCurrentUser(): Promise<UserInfo> {
    return apiClient.get<UserInfo>('/api/v1/auth/me');
  }

  isAuthenticated(): boolean {
    if (typeof window === 'undefined') return false;
    return !!localStorage.getItem('authToken');
  }
}

export const authService = new AuthService();
