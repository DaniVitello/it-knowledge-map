import { describe, it, expect } from 'vitest';
import { linkEntities, deriveAction, actionToUrl } from './chatBridge';
import type { ConceptIndexEntry, AreaInfo } from './types';

const area = (uid: string, name: string): AreaInfo => ({
  uid, name, order: 1, color_token: 'cyan', count: 10, professional_roles: [],
});
const concept = (uid: string, title: string, area_uid: string): ConceptIndexEntry => ({
  uid, title, slug: uid, area_uid, numero: 1, marks_count: 0, sections_missing: [],
});

const AREAS = [area('frontend', 'Frontend'), area('backend', 'Backend'), area('networking', 'Internet & Web')];
const CONCEPTS = [
  concept('c_http', 'HTTP', 'backend'),
  concept('c_dns', 'DNS', 'networking'),
  concept('c_aiml', 'AI / ML Fundamentals', 'ai-ml'),
  concept('c_ip', 'IP', 'networking'),
];

describe('chatBridge: entity linking', () => {
  it('dos áreas nombradas → áreas, sin conceptos parciales', () => {
    const ent = linkEntities('¿Cómo se relacionan Frontend y Backend?', CONCEPTS, AREAS);
    expect(ent.areas.map((a) => a.uid).sort()).toEqual(['backend', 'frontend']);
    expect(ent.concepts).toHaveLength(0);
  });

  it('dos conceptos → path', () => {
    const ent = linkEntities('Camino entre HTTP y DNS', CONCEPTS, AREAS);
    expect(ent.concepts.map((c) => c.uid).sort()).toEqual(['c_dns', 'c_http']);
    const act = deriveAction('Camino entre HTTP y DNS', ent);
    expect(act?.kind).toBe('path');
  });

  it('un concepto → vecindad', () => {
    const ent = linkEntities('Explorá AI / ML Fundamentals', CONCEPTS, AREAS);
    const act = deriveAction('Explorá AI / ML Fundamentals', ent);
    expect(act?.kind).toBe('neighborhood');
    if (act?.kind === 'neighborhood') expect(act.uid).toBe('c_aiml');
  });

  it('límite de palabra: IP no matchea dentro de equipment', () => {
    const ent = linkEntities('hablamos de equipment', CONCEPTS, AREAS);
    expect(ent.concepts).toHaveLength(0);
  });

  it('sin entidades → acción nula', () => {
    const ent = linkEntities('hola qué tal', CONCEPTS, AREAS);
    expect(deriveAction('hola qué tal', ent)).toBeNull();
  });
});

describe('chatBridge: deriveAction + URLs', () => {
  it('áreas → resaltar relaciones entre áreas', () => {
    const ent = linkEntities('relación entre frontend y backend', CONCEPTS, AREAS);
    const act = deriveAction('relación entre frontend y backend', ent);
    expect(act?.kind).toBe('areas');
    if (act?.kind === 'areas') expect([...act.areas].sort()).toEqual(['backend', 'frontend']);
    expect(actionToUrl(act!)).toBe('/graph?areas=frontend,backend');
  });

  it('path → URL from/to', () => {
    const act = deriveAction('HTTP y DNS', linkEntities('HTTP y DNS', CONCEPTS, AREAS));
    expect(actionToUrl(act!)).toMatch(/^\/graph\?from=c_(http|dns)&to=c_(http|dns)$/);
  });

  it('vecindad → URL /graph/view/:uid', () => {
    const act = deriveAction('DNS', linkEntities('DNS', CONCEPTS, AREAS));
    expect(actionToUrl(act!)).toBe('/graph/view/c_dns');
  });

  it('un área → URL ?area=', () => {
    const act = deriveAction('mostrame backend', linkEntities('mostrame backend', CONCEPTS, AREAS));
    expect(act?.kind).toBe('area');
    expect(actionToUrl(act!)).toBe('/graph?area=backend');
  });
});