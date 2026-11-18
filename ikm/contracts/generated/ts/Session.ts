// Generado desde contracts. No editar a mano.
export interface Session {
  created_at: string;
  expires_at: string;
  id_hash: string;
  ip_hash?: (string) | null;
  last_seen_at?: (string) | null;
  revoked_at?: (string) | null;
  ua_hash?: (string) | null;
  user_id: string;
}
