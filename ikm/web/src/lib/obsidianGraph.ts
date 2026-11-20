/** Grafo "modo Obsidian": replica el mind-map del vault IT-Mind-Map.
 * El vault tiene una raíz (00 - Indice Maestro IT, el "mercado IT") que enlaza
 * a las 10 áreas Y a los 255 conceptos directamente; cada índice de área enlaza
 * a su raíz y a sus conceptos; los conceptos tienen sus relaciones reales.
 * Acá se agrega esa jerarquía (raíz + cabezas de área) al grafo de conceptos,
 * para que la raíz quede como nodo central gigante, las áreas como cabezas
 * medianas y los conceptos como hojas chicas (tamaño por grado, como Obsidian).
 */
import type { GraphNode, GraphEdge } from './types';

export const ROOT_UID = 'root';
export const areaNodeUid = (areaUid: string) => `area:${areaUid}`;

export type NodeKind = 'root' | 'area' | 'concept';
export function nodeKind(uid: string): NodeKind {
  if (uid === ROOT_UID) return 'root';
  if (uid.startsWith('area:')) return 'area';
  return 'concept';
}

export interface ObsidianGraph { nodes: GraphNode[]; edges: GraphEdge[] }

const hEdge = (uid: string, source: string, target: string): GraphEdge => ({
  uid, source, target, type: 'jerarquia', cross_area: false, has_explanation: false,
});

/** Construye el grafo aumentado: raíz + cabezas de área + conceptos + jerarquía + relaciones. */
export function buildObsidianGraph(
  graph: { nodes: GraphNode[]; edges: GraphEdge[] },
  areas: { uid: string; name: string }[],
  rootTitle = 'Mercado IT',
): ObsidianGraph {
  const nodes: GraphNode[] = [];
  const edges: GraphEdge[] = [];

  nodes.push({ uid: ROOT_UID, title: rootTitle, slug: 'mercado-it', area_uid: null, grado: 0, x: 0, y: 0 });
  for (const a of areas) {
    nodes.push({ uid: areaNodeUid(a.uid), title: a.name, slug: a.uid, area_uid: a.uid, grado: 0, x: 0, y: 0 });
  }
  for (const n of graph.nodes) nodes.push({ ...n });

  // Jerarquía del vault: raíz → área, raíz → concepto, área → concepto.
  for (const a of areas) edges.push(hEdge(`h-root-${a.uid}`, ROOT_UID, areaNodeUid(a.uid)));
  for (const n of graph.nodes) {
    edges.push(hEdge(`h-root-${n.uid}`, ROOT_UID, n.uid));
    if (n.area_uid) edges.push(hEdge(`h-area-${n.uid}`, areaNodeUid(n.area_uid), n.uid));
  }
  // Relaciones reales entre conceptos (se conservan tal cual).
  for (const e of graph.edges) edges.push(e);

  // Grado real contando todos los enlaces (la raíz queda ~265, áreas ~26, hojas pocas).
  const degree = new Map<string, number>();
  for (const e of edges) {
    degree.set(e.source, (degree.get(e.source) ?? 0) + 1);
    degree.set(e.target, (degree.get(e.target) ?? 0) + 1);
  }
  for (const n of nodes) n.grado = degree.get(n.uid) ?? 0;

  return { nodes, edges };
}