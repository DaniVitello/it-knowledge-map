// Generado desde contracts. No editar a mano.
import type { MessageRole } from './MessageRole';
export interface Message {
  blocks?: Array<Record<string, unknown>>;
  cached?: boolean;
  conversation_id: string;
  created_at: string;
  degraded?: boolean;
  expires_at?: (string) | null;
  id: string;
  retrieval_trace?: Record<string, unknown>;
  role: MessageRole;
  scope_class?: (string) | null;
  text?: string;
  tokens_in?: number;
  tokens_out?: number;
  ui_actions?: Array<Record<string, unknown>>;
}
