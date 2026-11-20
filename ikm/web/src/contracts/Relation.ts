// Generado desde contracts. No editar a mano.
import type { Explanation } from './Explanation';
import type { RelationType } from './RelationType';
import type { TypeBasis } from './TypeBasis';
export interface Relation {
  cross_area?: boolean;
  explanation?: (Explanation) | null;
  source_uid: string;
  target_uid: string;
  type?: RelationType;
  type_basis?: TypeBasis;
  uid: string;
}
