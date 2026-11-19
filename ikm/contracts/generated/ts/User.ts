// Generado desde contracts. No editar a mano.
import type { UserStatus } from './UserStatus';
export interface User {
  created_at: string;
  deleted_at?: (string) | null;
  email: string;
  email_verified: boolean;
  google_sub: string;
  id: string;
  last_seen_at?: (string) | null;
  status?: UserStatus;
}
