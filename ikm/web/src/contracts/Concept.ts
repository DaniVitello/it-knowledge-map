// Generado desde contracts. No editar a mano.
import type { ConceptSections } from './ConceptSections';
import type { VerificationMark } from './VerificationMark';
export interface Concept {
  aliases?: Array<string>;
  area_uid?: (string) | null;
  content_hash: string;
  sections?: ConceptSections;
  slug: string;
  sources?: Array<string>;
  title: string;
  uid: string;
  verification_marks?: Array<VerificationMark>;
}
