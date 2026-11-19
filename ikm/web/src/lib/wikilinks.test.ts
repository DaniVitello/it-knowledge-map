import { describe, expect, it } from 'vitest';
import {
  buildTitleIndex, cleanExplanationText, normalizeWikiTarget,
  parseWikilinks, resolveWikiTarget, wikilinksToMarkdown,
} from './wikilinks';
import type { ConceptIndexEntry } from './types';

const concepts: ConceptIndexEntry[] = [
  { uid: 'c_IP', title: 'IP', slug: 'ip', area_uid: 'networking', numero: 2, marks_count: 0, sections_missing: [] },
  { uid: 'c_LB', title: 'Lenguaje Backend', slug: 'lenguaje-backend', area_uid: 'backend', numero: 4, marks_count: 0, sections_missing: [] },
];

describe('parseWikilinks', () => {
  it('separa texto y links con alias', () => {
    const tokens = parseWikilinks('Uso [[05 - Networking/02 - IP|IP]] a diario');
    expect(tokens).toHaveLength(3);
    expect(tokens[1]).toMatchObject({ kind: 'link', target: '05 - Networking/02 - IP', alias: 'IP', text: 'IP' });
  });
  it('link sin alias usa el destino como texto', () => {
    const tokens = parseWikilinks('[[DNS]]');
    expect(tokens[0]).toMatchObject({ kind: 'link', text: 'DNS', target: 'DNS' });
  });
  it('texto sin links queda intacto', () => {
    expect(parseWikilinks('hola mundo')).toEqual([{ kind: 'text', text: 'hola mundo' }]);
  });
});

describe('normalizeWikiTarget + resolución', () => {
  it('saca prefijo de área, numeración y extensión', () => {
    expect(normalizeWikiTarget('05 - Networking & Internet/02 - IP.md')).toBe('ip');
    expect(normalizeWikiTarget('03 - Backend/04 - Lenguaje Backend#seccion')).toBe('lenguaje backend');
  });
  it('resuelve contra el índice de títulos', () => {
    const idx = buildTitleIndex(concepts);
    expect(resolveWikiTarget('05 - Networking & Internet/02 - IP', idx)?.uid).toBe('c_IP');
    expect(resolveWikiTarget('Lenguaje Backend', idx)?.uid).toBe('c_LB');
    expect(resolveWikiTarget('No Existe', idx)).toBeUndefined();
  });
});

describe('wikilinksToMarkdown', () => {
  it('convierte a links ikm:// con el destino codificado', () => {
    const md = wikilinksToMarkdown('Mirá [[03 - Backend/04 - Lenguaje Backend|el lenguaje]]');
    expect(md).toContain('[el lenguaje](ikm://');
    expect(md).toContain(encodeURIComponent('03 - Backend/04 - Lenguaje Backend'));
  });
});

describe('cleanExplanationText', () => {
  it('limpia el prefijo Relacionados y muestra el alias', () => {
    const raw = '[Relacionados] - [[03 - Backend/04 - Lenguaje Backend|Lenguaje Backend]] · *Backend*';
    expect(cleanExplanationText(raw)).toBe('Lenguaje Backend · Backend');
  });
  it('sin alias usa el nombre de la nota sin numeración', () => {
    expect(cleanExplanationText('[[05 - Networking & Internet/02 - IP]]')).toBe('IP');
  });
});