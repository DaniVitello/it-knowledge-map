import { describe, expect, it } from 'vitest';
import { buildAdjacency, edgesAlongPath, neighborsOf, shortestPath, subgraphAround } from './graph';
import type { GraphData } from './types';

const graph: GraphData = {
  nodes: [
    { uid: 'c_A', title: 'A', slug: 'a', area_uid: 'x', grado: 2, x: 0, y: 0 },
    { uid: 'c_B', title: 'B', slug: 'b', area_uid: 'x', grado: 2, x: 10, y: 0 },
    { uid: 'c_C', title: 'C', slug: 'c', area_uid: 'y', grado: 2, x: 20, y: 0 },
    { uid: 'c_D', title: 'D', slug: 'd', area_uid: 'y', grado: 0, x: 90, y: 90 },
  ],
  edges: [
    { uid: 'r_AB', source: 'c_A', target: 'c_B', type: 'untyped', cross_area: false, has_explanation: true },
    { uid: 'r_BC', source: 'c_B', target: 'c_C', type: 'uses', cross_area: true, has_explanation: true },
  ],
};

describe('buildAdjacency', () => {
  it('registra ambas direcciones', () => {
    const adj = buildAdjacency(graph);
    const a = neighborsOf(adj, 'c_A');
    expect(a).toHaveLength(1);
    expect(a[0].uid).toBe('c_B');
    expect(a[0].direction).toBe('out');
    const b = neighborsOf(adj, 'c_B');
    expect(b.map((n) => n.uid).sort()).toEqual(['c_A', 'c_C']);
    expect(b.find((n) => n.uid === 'c_A')!.direction).toBe('in');
  });
  it('nodo aislado devuelve lista vacía', () => {
    const adj = buildAdjacency(graph);
    expect(neighborsOf(adj, 'c_D')).toEqual([]);
    expect(neighborsOf(adj, 'c_INEXISTENTE')).toEqual([]);
  });
});

describe('shortestPath', () => {
  const adj = buildAdjacency(graph);
  it('encuentra el camino más corto', () => {
    expect(shortestPath(adj, 'c_A', 'c_C')).toEqual(['c_A', 'c_B', 'c_C']);
  });
  it('mismo nodo -> camino trivial', () => {
    expect(shortestPath(adj, 'c_A', 'c_A')).toEqual(['c_A']);
  });
  it('sin camino -> null', () => {
    expect(shortestPath(adj, 'c_A', 'c_D')).toBeNull();
  });
  it('uid desconocido -> null', () => {
    expect(shortestPath(adj, 'c_A', 'c_ZZZ')).toBeNull();
  });
});

describe('subgraphAround', () => {
  const adj = buildAdjacency(graph);
  it('profundidad 1 incluye vecinos y sus aristas', () => {
    const sub = subgraphAround(graph, adj, 'c_B', 1);
    expect(sub.nodes.map((n) => n.uid).sort()).toEqual(['c_A', 'c_B', 'c_C']);
    expect(sub.edges).toHaveLength(2);
  });
  it('profundidad 0 es solo el nodo', () => {
    const sub = subgraphAround(graph, adj, 'c_B', 0);
    expect(sub.nodes.map((n) => n.uid)).toEqual(['c_B']);
    expect(sub.edges).toHaveLength(0);
  });
});

describe('edgesAlongPath', () => {
  it('devuelve las aristas del camino en cualquier dirección', () => {
    const edges = edgesAlongPath(graph, ['c_C', 'c_B', 'c_A']);
    expect(edges.map((e) => e.uid).sort()).toEqual(['r_AB', 'r_BC']);
  });
});