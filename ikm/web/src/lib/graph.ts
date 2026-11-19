/** Operaciones de grafo puras: adyacencia, vecindad, camino más corto (BFS).
 * Deterministas: vecinos ordenados por uid; sin estado global.
 */
import type { GraphData, GraphEdge, GraphNode } from './types';

export interface Neighbor {
  uid: string;
  edgeUid: string;
  type: string;
  crossArea: boolean;
  hasExplanation: boolean;
  /** 'out' = este concepto -> vecino; 'in' = vecino -> este concepto. */
  direction: 'out' | 'in';
}

export type Adjacency = Map<string, Neighbor[]>;

export function buildAdjacency(graph: GraphData): Adjacency {
  const adj: Adjacency = new Map();
  for (const n of graph.nodes) adj.set(n.uid, []);
  for (const e of graph.edges) {
    adj.get(e.source)?.push({
      uid: e.target, edgeUid: e.uid, type: e.type,
      crossArea: e.cross_area, hasExplanation: e.has_explanation, direction: 'out',
    });
    adj.get(e.target)?.push({
      uid: e.source, edgeUid: e.uid, type: e.type,
      crossArea: e.cross_area, hasExplanation: e.has_explanation, direction: 'in',
    });
  }
  for (const list of adj.values()) {
    list.sort((a, b) => a.uid.localeCompare(b.uid) || a.direction.localeCompare(b.direction));
  }
  return adj;
}

export function neighborsOf(adj: Adjacency, uid: string): Neighbor[] {
  return adj.get(uid) ?? [];
}

/** Camino más corto no dirigido entre dos uids (BFS). null si no hay camino. */
export function shortestPath(adj: Adjacency, from: string, to: string): string[] | null {
  if (from === to) return [from];
  if (!adj.has(from) || !adj.has(to)) return null;
  const prev = new Map<string, string>();
  const visited = new Set<string>([from]);
  const queue: string[] = [from];
  while (queue.length > 0) {
    const current = queue.shift()!;
    for (const nb of neighborsOf(adj, current)) {
      if (visited.has(nb.uid)) continue;
      visited.add(nb.uid);
      prev.set(nb.uid, current);
      if (nb.uid === to) {
        const path: string[] = [to];
        let cursor = to;
        while (prev.has(cursor)) {
          cursor = prev.get(cursor)!;
          path.push(cursor);
        }
        return path.reverse();
      }
      queue.push(nb.uid);
    }
  }
  return null;
}

export interface Subgraph {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

/** Vecindad de profundidad N alrededor de un uid (para vista contextual). */
export function subgraphAround(graph: GraphData, adj: Adjacency, uid: string, depth = 1): Subgraph {
  const keep = new Set<string>([uid]);
  let frontier = [uid];
  for (let d = 0; d < depth; d++) {
    const next: string[] = [];
    for (const u of frontier) {
      for (const nb of neighborsOf(adj, u)) {
        if (!keep.has(nb.uid)) {
          keep.add(nb.uid);
          next.push(nb.uid);
        }
      }
    }
    frontier = next;
  }
  return {
    nodes: graph.nodes.filter((n) => keep.has(n.uid)),
    edges: graph.edges.filter((e) => keep.has(e.source) && keep.has(e.target)),
  };
}

/** Nodos alcanzables desde un conjunto (para resaltar camino en el grafo). */
export function edgesAlongPath(graph: GraphData, path: string[]): GraphEdge[] {
  const pairs = new Set<string>();
  for (let i = 0; i + 1 < path.length; i++) {
    pairs.add(`${path[i]}|${path[i + 1]}`);
    pairs.add(`${path[i + 1]}|${path[i]}`);
  }
  return graph.edges.filter((e) => pairs.has(`${e.source}|${e.target}`));
}