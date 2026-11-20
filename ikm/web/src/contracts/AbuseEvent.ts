// Generado desde contracts. No editar a mano.
import type { AbuseKind } from './AbuseKind';
export interface AbuseEvent {
  created_at: string;
  id: string;
  ip_hash: string;
  kind: AbuseKind;
  user_id?: (string) | null;
}
