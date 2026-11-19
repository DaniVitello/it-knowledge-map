// Generado desde contracts. No editar a mano.
import type { Camera } from './Camera';
import type { Origin } from './Origin';
import type { ViewType } from './ViewType';
export interface ExplorationState {
  camera?: (Camera) | null;
  created_at?: (string) | null;
  filters?: Record<string, unknown>;
  focus_uids?: Array<string>;
  label?: (string) | null;
  origin?: Origin;
  relation_uids?: Array<string>;
  release_id: string;
  version: number;
  view_type: ViewType;
}
