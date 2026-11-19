// Generado desde contracts. No editar a mano.
import type { PeriodBasis } from './PeriodBasis';
export interface Period {
  basis: PeriodBasis;
  end?: (string) | null;
  precision: string;
  start: string;
}
