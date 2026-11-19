/** Búsqueda cliente sobre el release: índice invertido liviano con scoring
 * título > cuerpo, tolerante a tildes. Determinista y testeable sin DOM.
 */
import type { ClientIndex, ConceptIndexEntry, ReleaseBootstrap } from './types';

export interface SearchDoc {
  uid: string;
  title: string;
  slug: string;
  areaUid: string | null;
  numero: number | null;
  marksCount: number;
  titleNorm: string;
  bodyNorm: string;
  /** section -> texto normalizado (para snippet contextual). */
  sections: Map<string, string>;
}

export interface SearchIndex {
  docs: SearchDoc[];
  byUid: Map<string, SearchDoc>;
}

export interface SearchResult {
  uid: string;
  title: string;
  slug: string;
  areaUid: string | null;
  score: number;
  snippet: string;
  section: string | null;
}

export function normalizeText(s: string): string {
  return (s || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

export function tokenize(q: string): string[] {
  return normalizeText(q).split(/[^a-z0-9]+/).filter((t) => t.length > 1);
}

const HEADER_RE = /^Concepto:.*?\|.*?Seccion:.*?\n/;

export function buildSearchIndex(bootstrap: ReleaseBootstrap, clientIndex: ClientIndex | null): SearchIndex {
  const sectionsByUid = new Map<string, Map<string, string>>();
  if (clientIndex) {
    for (const ch of clientIndex.chunks) {
      let map = sectionsByUid.get(ch.entity_uid);
      if (!map) {
        map = new Map();
        sectionsByUid.set(ch.entity_uid, map);
      }
      const body = ch.text.replace(HEADER_RE, '');
      map.set(ch.section, (map.get(ch.section) ?? '') + ' ' + normalizeText(body));
    }
  }
  const docs: SearchDoc[] = bootstrap.concepts.map((c: ConceptIndexEntry) => {
    const sections = sectionsByUid.get(c.uid) ?? new Map<string, string>();
    let bodyNorm = '';
    for (const text of sections.values()) bodyNorm += ' ' + text;
    return {
      uid: c.uid,
      title: c.title,
      slug: c.slug,
      areaUid: c.area_uid,
      numero: c.numero,
      marksCount: c.marks_count,
      titleNorm: normalizeText(c.title),
      bodyNorm: bodyNorm.trim(),
      sections,
    };
  });
  return { docs, byUid: new Map(docs.map((d) => [d.uid, d])) };
}

function snippetAround(text: string, term: string, radius = 70): string {
  const i = text.indexOf(term);
  if (i < 0) return text.slice(0, radius * 2).trim();
  const start = Math.max(0, i - radius);
  const end = Math.min(text.length, i + term.length + radius);
  return (start > 0 ? '…' : '') + text.slice(start, end).trim() + (end < text.length ? '…' : '');
}

export interface SearchOptions {
  area?: string | null;
  limit?: number;
}

export function search(index: SearchIndex, query: string, opts: SearchOptions = {}): SearchResult[] {
  const terms = tokenize(query);
  if (terms.length === 0) return [];
  const limit = opts.limit ?? 20;
  const results: SearchResult[] = [];

  for (const doc of index.docs) {
    if (opts.area && doc.areaUid !== opts.area) continue;
    let score = 0;
    let matchedAll = true;
    let bestSection: string | null = null;
    let bestTerm = terms[0];

    for (const term of terms) {
      let termScore = 0;
      if (doc.titleNorm === term) termScore += 40;
      else if (doc.titleNorm.startsWith(term)) termScore += 22;
      else if (doc.titleNorm.includes(term)) termScore += 14;

      if (doc.bodyNorm.includes(term)) {
        termScore += 4;
        for (const [section, text] of doc.sections) {
          if (text.includes(term)) {
            termScore += 1;
            if (!bestSection) {
              bestSection = section;
              bestTerm = term;
            }
          }
        }
      }
      if (termScore === 0) matchedAll = false;
      score += termScore;
    }

    // Todas las palabras deben aparecer en algún lado (AND suave).
    if (!matchedAll || score === 0) continue;
    if (terms.length > 1 && doc.titleNorm.includes(normalizeText(query))) score += 12;

    const snippet = bestSection
      ? snippetAround(doc.sections.get(bestSection) ?? '', bestTerm)
      : doc.title;
    results.push({
      uid: doc.uid, title: doc.title, slug: doc.slug, areaUid: doc.areaUid,
      score, snippet, section: bestSection,
    });
  }

  results.sort((a, b) => b.score - a.score || a.title.localeCompare(b.title));
  return results.slice(0, limit);
}