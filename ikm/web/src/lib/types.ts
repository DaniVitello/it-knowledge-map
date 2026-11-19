/** Tipos del release estático. Los contratos base vienen de ikm/contracts (L0). */
import type { Concept, Relation } from '@contracts/index';

export interface Manifest {
  schema_version: number;
  release_id: string;
  pipeline_version: string;
  vault_hash: string;
  counts: {
    concepts: number;
    areas: number;
    relations: number;
    journey_records: number;
    evidence: number;
    chunks: number;
  };
  files: { path: string; sha256: string }[];
}

export interface AreaInfo {
  uid: string;
  name: string;
  order: number;
  color_token: string;
  count: number;
  context_framing?: string | null;
  professional_roles: string[];
}

export interface ConceptIndexEntry {
  uid: string;
  title: string;
  slug: string;
  area_uid: string | null;
  numero: number | null;
  marks_count: number;
  sections_missing: string[];
}

export interface ReleaseBootstrap {
  schema_version: number;
  counts: Record<string, number>;
  areas: { uid: string; name: string; order: number; count: number }[];
  concepts: ConceptIndexEntry[];
}

export interface GraphNode {
  uid: string;
  title: string;
  slug: string;
  area_uid: string | null;
  grado: number;
  x: number;
  y: number;
}

export interface GraphEdge {
  uid: string;
  source: string;
  target: string;
  type: string;
  cross_area: boolean;
  has_explanation: boolean;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

/** Ficha completa: contrato Concept + meta de navegación del release. */
export interface Ficha extends Concept {
  numero?: number | null;
  tags?: string[];
  sections_missing?: string[];
  related_uids?: string[];
  sources_detail?: { url: string; title?: string | null }[];
}

export type RelationRecord = Relation;

export interface ClientIndexChunk {
  chunk_id: string;
  entity_uid: string;
  area_uid: string | null;
  section: string;
  text: string;
}

export interface ClientIndex {
  chunks: ClientIndexChunk[];
  total: number;
}