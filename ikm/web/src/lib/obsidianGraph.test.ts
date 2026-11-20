import { describe, it, expect } from 'vitest';
import { buildObsidianGraph, nodeKind, ROOT_UID, areaNodeUid } from './obsidianGraph';
import type { GraphNode, GraphEdge } from './types';

const gn = (uid: string, title: string, area_uid: string): GraphNode => ({ uid, title, slug: uid, area_uid, grado: 0, x: 0, y: 0 });
const ge = (uid: string, source: string, target: string): GraphEdge => ({ uid, source, target, type: 'relacion', cross_area: false, has_explanation: true });

const graph = {
  nodes: [gn('c1', 'HTTP', 'backend'), gn('c2', 'DNS', 'networking'), gn('c3', 'IP', 'networking')],
  edges: [ge('r1', 'c1', 'c2')],
};
const areas = [{ uid: 'backend', name: 'Backend' }, { uid: 'networking', name: 'Networking & Internet' }];

describe('buildObsidianGraph: mind-map del vault', () => {
  const og = buildObsidianGraph(graph, areas);

  it('agrega raíz + cabezas de área + conceptos', () => {
    expect(og.nodes.length).toBe(1 + 2 + 3);
    expect(og.nodes.some((n) => n.uid === ROOT_UID)).toBe(true);
    expect(og.nodes.some((n) => n.uid === areaNodeUid('backend'))).toBe(true);
  });

  it('la raíz enlaza a áreas y a todos los conceptos (grado alto)', () => {
    const root = og.nodes.find((n) => n.uid === ROOT_UID)!;
    expect(root.grado).toBe(2 + 3);
    expect(root.title).toBe('Mercado IT');
  });

  it('jerarquía raíz→área, raíz→concepto, área→concepto', () => {
    expect(og.edges.some((e) => e.source === ROOT_UID && e.target === areaNodeUid('backend'))).toBe(true);
    expect(og.edges.some((e) => e.source === ROOT_UID && e.target === 'c1')).toBe(true);
    expect(og.edges.some((e) => e.source === areaNodeUid('backend') && e.target === 'c1')).toBe(true);
  });

  it('conserva las relaciones reales entre conceptos', () => {
    expect(og.edges.some((e) => e.uid === 'r1')).toBe(true);
  });

  it('el área cabeza tiene grado raíz + sus conceptos', () => {
    const net = og.nodes.find((n) => n.uid === areaNodeUid('networking'))!;
    expect(net.grado).toBe(1 + 2); // raíz + DNS + IP
  });

  it('nodeKind distingue raíz / área / concepto', () => {
    expect(nodeKind(ROOT_UID)).toBe('root');
    expect(nodeKind(areaNodeUid('backend'))).toBe('area');
    expect(nodeKind('c1')).toBe('concept');
  });
});