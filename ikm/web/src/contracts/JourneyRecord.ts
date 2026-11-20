// Generado desde contracts. No editar a mano.
import type { JourneyKind } from './JourneyKind';
import type { Period } from './Period';
import type { Publication } from './Publication';
export interface JourneyRecord {
  concept_uids?: Array<string>;
  content_hash: string;
  context?: (string) | null;
  decisions?: Array<string>;
  description?: (string) | null;
  evidence_uids?: Array<string>;
  kind?: Array<JourneyKind>;
  objective?: (string) | null;
  period?: (Period) | null;
  problems?: Array<string>;
  publication?: Publication;
  results?: Array<string>;
  slug: string;
  solutions?: Array<string>;
  stage?: (string) | null;
  technologies?: Array<string>;
  title: string;
  tools?: Array<string>;
  topics?: Array<string>;
  uid: string;
}
