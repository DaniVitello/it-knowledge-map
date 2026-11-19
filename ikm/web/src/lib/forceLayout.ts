/** Layout 3D por fuerza (client-side, d3-force-3d) con clustering por área.
 * Funciones puras testeables: centroides de área en esfera Fibonacci y radio
 * de nodo por grado. La simulación vive en Graph3D.
 */
import type { GraphNode } from './types';

export interface Vec3 { x: number; y: number; z: number }

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

/** Radio de nodo en unidades de mundo, según grado. */
export function nodeRadius(grado: number): number {
  return 5 + Math.sqrt(Math.max(grado, 0)) * 1.6;
}

export interface SimNode extends GraphNode {
  x: number; y: number; z: number;
  vx?: number; vy?: number; vz?: number;
  index?: number;
  radius: number;
}

export interface SimLink { source: string | SimNode; target: string | SimNode; uid: string }

/** Posiciones iniciales dispersas alrededor del centroide de su área. */
export function initialPositions(nodes: GraphNode[], centroids: Map<string, Vec3>, jitter = 90): SimNode[] {
  return nodes.map((n, i) => {
    const c = centroids.get(n.area_uid ?? '') ?? { x: 0, y: 0, z: 0 };
    // dispersión determinista por índice (sin Math.random para reproducibilidad visual)
    const a = i * 2.399963; // ángulo áureo
    const rr = jitter * Math.sqrt((i % 30) / 30 + 0.1);
    return {
      ...n,
      x: c.x + Math.cos(a) * rr,
      y: c.y + Math.sin(a * 1.3) * rr,
      z: c.z + Math.sin(a) * rr,
      radius: nodeRadius(n.grado),
    };
  });
}