// Generado desde contracts. No editar a mano.
export interface Evidence {
  alt_text?: (string) | null;
  kind: EvidenceKind;
  mime: string;
  record_uid: string;
  review?: EvidenceReview;
  sha256: string;
  size: number;
  storage_key: string;
  uid: string;
  variants?: Array<EvidenceVariant>;
}
