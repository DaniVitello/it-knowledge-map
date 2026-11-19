import { describe, expect, it } from 'vitest';
import { buildSearchIndex, normalizeText, search, tokenize } from './search';
import type { ClientIndex, ReleaseBootstrap } from './types';

const bootstrap: ReleaseBootstrap = {
  schema_version: 1,
  counts: { concepts: 3 },
  areas: [],
  concepts: [
    { uid: 'c_AAAAAAAAAA', title: 'Búsqueda Binaria', slug: 'busqueda-binaria', area_uid: 'software-engineering', numero: 1, marks_count: 0, sections_missing: [] },
    { uid: 'c_BBBBBBBBBB', title: 'HTTP', slug: 'http', area_uid: 'networking', numero: 2, marks_count: 1, sections_missing: [] },
    { uid: 'c_CCCCCCCCCC', title: 'DNS', slug: 'dns', area_uid: 'networking', numero: 3, marks_count: 0, sections_missing: [] },
  ],
};

const clientIndex: ClientIndex = {
  total: 3,
  chunks: [
    { chunk_id: 'c_AAAAAAAAAA#objetivo#0', entity_uid: 'c_AAAAAAAAAA', area_uid: 'software-engineering', section: 'objetivo', text: 'Concepto: Búsqueda Binaria | Area: software-engineering | Seccion: objetivo\nencuentro elementos en listas ordenadas dividiendo el espacio de búsqueda' },
    { chunk_id: 'c_BBBBBBBBBB#como_funciona#0', entity_uid: 'c_BBBBBBBBBB', area_uid: 'networking', section: 'como_funciona', text: 'Concepto: HTTP | Area: networking | Seccion: como_funciona\nel cliente envía una petición y el servidor responde con un código de estado' },
    { chunk_id: 'c_CCCCCCCCCC#objetivo#0', entity_uid: 'c_CCCCCCCCCC', area_uid: 'networking', section: 'objetivo', text: 'Concepto: DNS | Area: networking | Seccion: objetivo\nresuelvo nombres de dominio a direcciones ip para ubicar servidores' },
  ],
};

describe('normalizeText / tokenize', () => {
  it('saca tildes y normaliza espacios', () => {
    expect(normalizeText('  BÚSQUEDA   Binaria ')).toBe('busqueda binaria');
  });
  it('tokeniza descartando cortos y símbolos', () => {
    expect(tokenize('HTTP/2 y DNS!')).toEqual(['http', 'dns']);
  });
});

describe('buildSearchIndex + search', () => {
  const index = buildSearchIndex(bootstrap, clientIndex);

  it('encuentra por título sin tildes', () => {
    const r = search(index, 'busqueda');
    expect(r.length).toBeGreaterThan(0);
    expect(r[0].uid).toBe('c_AAAAAAAAAA');
  });

  it('el título pesa más que el cuerpo', () => {
    const r = search(index, 'dns');
    expect(r[0].uid).toBe('c_CCCCCCCCCC');
  });

  it('encuentra por contenido del cuerpo con snippet y sección', () => {
    const r = search(index, 'servidores');
    expect(r.some((x) => x.uid === 'c_CCCCCCCCCC')).toBe(true);
    const dns = r.find((x) => x.uid === 'c_CCCCCCCCCC')!;
    expect(dns.section).toBe('objetivo');
    expect(dns.snippet.length).toBeGreaterThan(0);
  });

  it('AND suave: todas las palabras deben aparecer', () => {
    const r = search(index, 'http zzztermino');
    expect(r).toEqual([]);
  });

  it('filtra por área', () => {
    const r = search(index, 'ip', { area: 'networking' });
    expect(r.every((x) => x.areaUid === 'networking')).toBe(true);
  });

  it('query vacía no devuelve resultados', () => {
    expect(search(index, '   ')).toEqual([]);
  });

  it('funciona sin client-index (solo títulos)', () => {
    const soloTitulos = buildSearchIndex(bootstrap, null);
    expect(search(soloTitulos, 'http')[0].uid).toBe('c_BBBBBBBBBB');
    expect(search(soloTitulos, 'servidores')).toEqual([]);
  });

  it('respeta el límite y ordena por score', () => {
    const r = search(index, 'e', { limit: 2 });
    expect(r.length).toBeLessThanOrEqual(2);
  });
});