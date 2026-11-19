/** Puente chat↔grafo (spec §8.7): enlaza entidades del mensaje del visitante
 * contra el release (conceptos por título, áreas por nombre) y deriva una
 * acción de grafo. Funciona aunque el backend sea stub: la intención se
 * resuelve en el cliente contra datos documentados, nunca se inventa.
 */
import type { ConceptIndexEntry, AreaInfo } from './types';
import { normalizeText } from './search';

export interface LinkedEntities {
  concepts: ConceptIndexEntry[];
  areas: AreaInfo[];
}

export type GraphAction =
  | { kind: 'path'; from: string; to: string; label: string }
  | { kind: 'areas'; areas: string[]; label: string }
  | { kind: 'neighborhood'; uid: string; label: string }
  | { kind: 'area'; area: string; label: string };

function escapeRe(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/** Match de frase completa con límites de palabra (tolerante a tildes/espacios). */
function phraseInText(normText: string, phrase: string): boolean {
  const p = normalizeText(phrase);
  if (p.length < 2) return false;
  const re = new RegExp(`(^|[^a-z0-9])${escapeRe(p).replace(/\s+/g, '\\s+')}([^a-z0-9]|$)`, 'i');
  return re.test(normText);
}

export function linkEntities(text: string, concepts: ConceptIndexEntry[], areas: AreaInfo[]): LinkedEntities {
  const norm = normalizeText(text);
  const matchedAreas = areas.filter((a) => phraseInText(norm, a.name) || phraseInText(norm, a.uid.replace(/-/g, ' ')));
  const matchedConcepts = concepts
    .filter((c) => phraseInText(norm, c.title))
    .sort((a, b) => b.title.length - a.title.length);
  // dedupe por uid
  const seen = new Set<string>();
  const conceptsUnique = matchedConcepts.filter((c) => (seen.has(c.uid) ? false : (seen.add(c.uid), true)));
  return { concepts: conceptsUnique, areas: matchedAreas };
}

const RELATIONAL = /relaci|conexi|conecta|v[ií]ncul|entre|compara|diferencia|\by\b|\band\b|->|↔/i;

/** Deriva la acción de grafo desde las entidades enlazadas y la intención. */
export function deriveAction(_text: string, ent: LinkedEntities): GraphAction | null {
  const { concepts, areas } = ent;
  if (areas.length >= 2) {
    const [a, b] = areas;
    return { kind: 'areas', areas: [a.uid, b.uid], label: `${a.name} ↔ ${b.name}` };
  }
  if (concepts.length >= 2) {
    const [a, b] = concepts;
    return { kind: 'path', from: a.uid, to: b.uid, label: `${a.title} → ${b.title}` };
  }
  if (concepts.length === 1) {
    return { kind: 'neighborhood', uid: concepts[0].uid, label: `Vecindad de ${concepts[0].title}` };
  }
  if (areas.length === 1) {
    return { kind: 'area', area: areas[0].uid, label: areas[0].name };
  }
  return null;
}

export function actionToUrl(a: GraphAction): string {
  switch (a.kind) {
    case 'path': return `/graph?from=${a.from}&to=${a.to}`;
    case 'areas': return `/graph?areas=${a.areas.join(',')}`;
    case 'neighborhood': return `/graph/view/${a.uid}`;
    case 'area': return `/graph?area=${a.area}`;
  }
}

/** Frase de intención legible para la UI (qué se va a activar). */
export function actionVerb(a: GraphAction): string {
  switch (a.kind) {
    case 'path': return 'Ver el camino entre';
    case 'areas': return 'Resaltar las relaciones entre';
    case 'neighborhood': return 'Explorar la vecindad de';
    case 'area': return 'Resaltar el área';
  }
}

export { RELATIONAL };