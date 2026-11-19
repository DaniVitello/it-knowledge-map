/** Wikilinks de Obsidian: parseo, resolución contra el release y limpieza
 * de explicaciones quoted. Los links de navegación NO son relaciones.
 */
import type { ConceptIndexEntry } from './types';
import { normalizeText } from './search';

export interface WikiToken {
  kind: 'text' | 'link';
  text: string;
  target?: string;
  alias?: string;
}

const WIKI_RE = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g;

export function parseWikilinks(text: string): WikiToken[] {
  const tokens: WikiToken[] = [];
  let last = 0;
  for (const m of text.matchAll(WIKI_RE)) {
    const idx = m.index ?? 0;
    if (idx > last) tokens.push({ kind: 'text', text: text.slice(last, idx) });
    const target = m[1].trim();
    const alias = m[2]?.trim();
    tokens.push({ kind: 'link', text: alias || target, target, alias });
    last = idx + m[0].length;
  }
  if (last < text.length) tokens.push({ kind: 'text', text: text.slice(last) });
  return tokens;
}

/** Normaliza un destino textual: '05 - Networking & Internet/02 - IP' -> 'ip'. */
export function normalizeWikiTarget(target: string): string {
  let t = (target || '').split('#')[0].split('|')[0].trim();
  t = t.replace(/\\/g, '/');
  if (t.includes('/')) t = t.split('/').pop() ?? t;
  t = t.replace(/\.md$/i, '');
  t = t.replace(/^\d+\s*-\s*/, '');
  return normalizeText(t);
}

export type TitleIndex = Map<string, ConceptIndexEntry>;

export function buildTitleIndex(concepts: ConceptIndexEntry[]): TitleIndex {
  const map: TitleIndex = new Map();
  for (const c of concepts) {
    const key = normalizeText(c.title);
    if (!map.has(key)) map.set(key, c);
  }
  return map;
}

export function resolveWikiTarget(target: string, index: TitleIndex): ConceptIndexEntry | undefined {
  return index.get(normalizeWikiTarget(target));
}

/** Convierte [[dest|alias]] en links markdown con esquema ikm:// para el renderer. */
export function wikilinksToMarkdown(text: string): string {
  return (text || '').replace(WIKI_RE, (_all, target: string, alias?: string) => {
    const label = (alias || target).trim();
    const dest = encodeURIComponent(target.trim());
    return `[${label}](ikm://${dest})`;
  });
}

/** Limpia una explicación quoted para mostrarla como texto legible:
 * '[Relacionados] - [[03 - Backend/04 - Lenguaje Backend|Lenguaje Backend]] · *Backend*'
 * -> 'Lenguaje Backend · Backend' (los links se resuelven en el componente).
 */
export function cleanExplanationText(text: string): string {
  let t = (text || '').trim();
  t = t.replace(/^\[Relacionados\]\s*-?\s*/i, '');
  t = t.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (_all, target: string, alias?: string) =>
    (alias || target.split('/').pop() || target).replace(/^\d+\s*-\s*/, '').trim());
  t = t.replace(/\*([^*]+)\*/g, '$1');
  return t.replace(/\s+/g, ' ').trim();
}