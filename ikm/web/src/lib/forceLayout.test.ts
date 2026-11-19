import { describe, it, expect } from 'vitest';
import { computeHeads, nodeRadius, initialPositions, areaCentroids } from './forceLayout';
import type { GraphNode } from './types';

const gn = (uid: string, title: string, area_uid: string, grado: number): GraphNode => ({
  uid, title, slug: uid, area_uid, grado, x: 0, y: 0,
});

const NODES = [
  gn('a1', 'Zebra', 'area-a', 3),
  gn('a2', 'Alpha', 'area-a', 8),   // cabeza de area-a (mayor grado)
  gn('a3', 'Mid', 'area-a', 5),
  gn('b1', 'Beta', 'area-b', 6),
  gn('b2', 'Gamma', 'area-b', 6),   // empate 6 → gana alfabético "Gamma"? no: Beta < Gamma → Beta
  gn('b3', 'Low', 'area-b', 1),
];

describe('computeHeads: jerarquía por área', () => {
  it('elige el mayor grado de cada área como cabeza', () => {
    const h = computeHeads(NODES);
    expect(h.heads.get('area-a')).toBe('a2');
    expect(h.headSet.has('a2')).toBe(true);
    expect(h.headSet.size).toBe(2);
  });

  it('desempata por título alfabético (determinista)', () => {
    const h = computeHeads(NODES);
    // area-b: Beta y Gamma empatan en 6 → "Beta" < "Gamma"
    expect(h.heads.get('area-b')).toBe('b1');
  });

  it('cabeza global = nodo más conectado del mapa', () => {
    const h = computeHeads(NODES);
    expect(h.globalHead).toBe('a2'); // grado 8
    expect(h.globalHeadArea).toBe('area-a');
  });

  it('área de un solo nodo: ese nodo es su cabeza', () => {
    const h = computeHeads([gn('x', 'Solo', 'area-x', 0)]);
    expect(h.heads.get('area-x')).toBe('x');
    expect(h.globalHead).toBe('x');
  });
});

describe('nodeRadius + initialPositions: realce de cabeza', () => {
  it('la cabeza tiene radio mayor que un miembro del mismo grado', () => {
    expect(nodeRadius(8, true)).toBeGreaterThan(nodeRadius(8, false));
  });

  it('las cabezas se siembran en el centroide de su área, los miembros alrededor', () => {
    const centroids = areaCentroids(['area-a', 'area-b']);
    const heads = computeHeads(NODES);
    const sim = initialPositions(NODES, centroids, 90, heads.headSet);
    const headA = sim.find((n) => n.uid === 'a2')!;
    const memberA = sim.find((n) => n.uid === 'a1')!;
    const cA = centroids.get('area-a')!;
    const dHead = Math.hypot(headA.x - cA.x, headA.y - cA.y, headA.z - cA.z);
    const dMember = Math.hypot(memberA.x - cA.x, memberA.y - cA.y, memberA.z - cA.z);
    expect(headA.isHead).toBe(true);
    expect(dHead).toBeLessThan(dMember);
    expect(headA.radius).toBeGreaterThan(memberA.radius);
  });
});