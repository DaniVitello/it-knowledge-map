/** Layout por fuerza (client-side, d3-force-3d) con jerarquía por área.
 * Funciones puras testeables: cabeza de cada área (mayor grado), centroides en
 * esfera Fibonacci / círculo, y radio de nodo por grado + realce de cabeza.
 * La simulación vive en Graph3D / GraphCanvas.
 */
import type { GraphNode } from './types';

export interface Vec3 { x: number; y: number; z: number }

export interface HeadInfo {
  /** area_uid -> uid de su cabeza (concepto más conectado del área). */
  heads: Map<string, string>;
  /** uids de todas las cabezas de área. */
  headSet: Set<string>;
  /** uid del nodo más conectado de todo el mapa (cabeza de cabezas). */
  globalHead: string | null;
  globalHeadArea: string | null;
}

/** Cabeza de cada área = mayor grado (desempate alfabético por título, determinista). */
export function computeHeads(nodes: GraphNode[]): HeadInfo {
  const byArea = new Map<string, GraphNode[]>();
  for (const n of nodes) {
    const a = n.area_uid ?? '';
    if (!byArea.has(a)) byArea.set(a, []);
    byArea.get(a)!.push(n);
  }
  const heads = new Map<string, string>();
  const headSet = new Set<string>();
  for (const [area, ns] of byArea) {
    const sorted = [...ns].sort((a, b) => (b.grado - a.grado) || a.title.localeCompare(b.title));
    if (sorted[0]) {
      heads.set(area, sorted[0].uid);
      headSet.add(sorted[0].uid);
    }
  }
  const sortedAll = [...nodes].sort((a, b) => (b.grado - a.grado) || a.title.localeCompare(b.title));
  const globalHead = sortedAll[0]?.uid ?? null;
  const globalHeadArea = sortedAll[0]?.area_uid ?? null;
  return { heads, headSet, globalHead, globalHeadArea };
}

/** Centroides de área distribuidos en una esfera (espiral Fibonacci). */
export function areaCentroids(areaUids: string[], radius = 460): Map<string, Vec3> {
  const uids = [...areaUids].sort();
  const n = Math.max(uids.length, 1);
  const golden = Math.PI * (3 - Math.sqrt(5));
  const out = new Map<string, Vec3>();
  uids.forEach((uid, i) => {
    const y = 1 - (i / Math.max(n - 1, 1)) * 2; // 1 .. -1
    const r = Math.sqrt(Math.max(0, 1 - y * y));
    const theta = golden * i;
    out.set(uid, {
      x: Math.cos(theta) * r * radius,
      y: y * radius,
      z: Math.sin(theta) * r * radius,
    });
  });
  return out;
}

/** Radio de nodo en unidades de mundo, según grado; las cabezas van realzadas. */
export function nodeRadius(grado: number, isHead = false): number {
  const base = 5 + Math.sqrt(Math.max(grado, 0)) * 1.6;
  return isHead ? base * 2.1 + 10 : base;
}

export interface SimNode extends GraphNode {
  x: number; y: number; z: number;
  vx?: number; vy?: number; vz?: number;
  index?: number;
  radius: number;
  isHead?: boolean;
  /** Ancla fija de la cabeza (centroide de su área). */
  anchor?: Vec3;
  /** Referencia viva a la cabeza del área (para que los miembros la orbiten). */
  headRef?: SimNode | null;
}

export interface SimLink { source: string | SimNode; target: string | SimNode; uid: string }

/** Posiciones iniciales: las cabezas en el centroide de su área, los miembros
 * dispersos alrededor (semilla determinista, sin Math.random). */
export function initialPositions(nodes: GraphNode[], centroids: Map<string, Vec3>, jitter = 90, headSet?: Set<string>): SimNode[] {
  return nodes.map((n, i) => {
    const c = centroids.get(n.area_uid ?? '') ?? { x: 0, y: 0, z: 0 };
    const isHead = headSet?.has(n.uid) ?? false;
    const a = i * 2.399963; // ángulo áureo
    const rr = isHead ? 4 : jitter * Math.sqrt((i % 30) / 30 + 0.1);
    return {
      ...n,
      x: c.x + Math.cos(a) * rr,
      y: c.y + Math.sin(a * 1.3) * rr,
      z: c.z + Math.sin(a) * rr,
      radius: nodeRadius(n.grado, isHead),
      isHead,
    };
  });
}