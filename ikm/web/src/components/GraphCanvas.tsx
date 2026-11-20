/** Grafo 2D en canvas, layout de fuerzas en vivo estilo Obsidian (DR-L10c).
 * - Simulación d3-force 2D en el cliente: los nodos se asientan animados y la
 *   proximidad refleja las conexiones (no posiciones decorativas fijas).
 * - Jerarquía por grado: el radio crece con la cantidad de conexiones (los hubs
 *   se ven claramente mayores), además de la agrupación por área.
 * - Nodos arrastrables (fijá un nodo y la simulación se recalienta), foco al
 *   hover (vecinos iluminados, resto atenuado), labels que aparecen con el zoom.
 * - Pan con drag en vacío, zoom con rueda/pinch, click en nodo o arista.
 * - prefers-reduced-motion: layout resuelto sin animación continua.
 * - Colores resueltos desde los tokens CSS (canvas no lee variables).
 */
import { useCallback, useEffect, useLayoutEffect, useMemo, useRef } from 'react';
import { forceSimulation, forceLink, forceManyBody, forceCollide, forceX, forceY } from 'd3-force-3d';
import type { GraphEdge, GraphNode } from '../lib/types';
import { computeHeads } from '../lib/forceLayout';
import { nodeKind, ROOT_UID } from '../lib/obsidianGraph';

export interface GraphCanvasProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  selectedUid?: string | null;
  highlightUids?: Set<string> | null;
  highlightEdgeUids?: Set<string> | null;
  highlightAreas?: Set<string> | null;
  focusUid?: string | null;
  areaFilter?: string | null;
  /** Incrementar para pedir un re-encuadre animado desde afuera. */
  fitSignal?: number;
  onSelect?: (uid: string | null) => void;
  onEdgeSelect?: (edgeUid: string) => void;
  onHover?: (uid: string | null) => void;
  className?: string;
  /** Modo Obsidian: mind-map jerárquico (raíz+áreas+conceptos), color uniforme editable. */
  obsidian?: boolean;
  monoColor?: string;
  areaColors?: Record<string, string>;
}

interface Camera { tx: number; ty: number; k: number }
interface SimNode2 {
  uid: string; area_uid: string | null; grado: number;
  x: number; y: number; vx: number; vy: number;
  fx?: number | null; fy?: number | null;
  isHead?: boolean;
  isRoot?: boolean;
  anchor?: { x: number; y: number };
  headRef?: SimNode2 | null;
}

const MIN_K = 0.12;
const MAX_K = 9;
const GOLDEN = 2.399963229728653;

/** Jerarquía visual: radio por grado (hubs notablemente mayores); cabezas realzadas. */
const nodeR = (grado: number, isHead = false) => Math.min(3 + Math.sqrt(grado) * 2.8 + (isHead ? 8 : 0), 34);
/** Modo Obsidian: la raíz (grado ~265) debe verse mucho mayor; tope más alto. */
const obsR = (grado: number) => Math.min(3 + Math.sqrt(grado) * 2.8, 60);
function toRgb(c: string): string {
  if (c.startsWith('#') && c.length === 7) {
    const r = parseInt(c.slice(1, 3), 16), g = parseInt(c.slice(3, 5), 16), b = parseInt(c.slice(5, 7), 16);
    return `rgb(${r} ${g} ${b})`;
  }
  return c;
}

function easeOutCubic(t: number): number {
  return 1 - Math.pow(1 - t, 3);
}

/** Centroides de área en un círculo (semilla para que agrupen orgánico). */
function areaSeeds(areaUids: string[], radius = 340): Map<string, { x: number; y: number }> {
  const m = new Map<string, { x: number; y: number }>();
  const n = Math.max(areaUids.length, 1);
  areaUids.forEach((uid, i) => {
    const a = (i / n) * Math.PI * 2 - Math.PI / 2;
    m.set(uid, { x: Math.cos(a) * radius, y: Math.sin(a) * radius });
  });
  return m;
}

export default function GraphCanvas({
  nodes, edges, selectedUid = null, highlightUids = null, highlightEdgeUids = null,
  highlightAreas = null, focusUid = null, areaFilter = null, fitSignal = 0, onSelect, onEdgeSelect, onHover, className = '',
  obsidian = false, monoColor = '#94a3b8', areaColors = {},
}: GraphCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wrapRef = useRef<HTMLDivElement>(null);
  const cam = useRef<Camera>({ tx: 0, ty: 0, k: 1 });
  const camAnim = useRef<{ from: Camera; to: Camera; start: number; dur: number } | null>(null);
  const size = useRef({ w: 0, h: 0, dpr: 1 });
  const hover = useRef<string | null>(null);
  const dirty = useRef(true);
  const pointers = useRef(new Map<number, { x: number; y: number }>());
  const drag = useRef<{ x: number; y: number; tx: number; ty: number; moved: boolean } | null>(null);
  const dragNode = useRef<SimNode2 | null>(null);
  const downAt = useRef<{ x: number; y: number; moved: boolean } | null>(null);
  const pinch = useRef<{ dist: number; k: number } | null>(null);
  const reduced = useRef(false);
  const didFit = useRef(false);

  const nodeByUid = useMemo(() => new Map(nodes.map((n) => [n.uid, n])), [nodes]);
  const neighbors = useMemo(() => {
    const map = new Map<string, Set<string>>();
    for (const n of nodes) map.set(n.uid, new Set());
    for (const e of edges) {
      map.get(e.source)?.add(e.target);
      map.get(e.target)?.add(e.source);
    }
    return map;
  }, [nodes, edges]);

  // Simulación de fuerzas 2D (Obsidian): link + repulsión + colisión + gravedad
  // suave por área. Se detiene el timer interno de d3 y se tick-ea en el rAF.
  const simData = useMemo(() => {
    const isReduced = typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (obsidian) {
      // Mind-map jerárquico: fuerza pura, raíz fija al centro. El grado alto de
      // la raíz la lleva al centro; las áreas quedan alrededor y las hojas en la
      // periferia (como Obsidian). Sin cabezas fijadas por área.
      const simNodes: SimNode2[] = nodes.map((n, i) => {
        const a = i * GOLDEN;
        const rr = n.uid === ROOT_UID ? 0 : 30 + 14 * Math.sqrt((i % 60) + 1);
        return { uid: n.uid, area_uid: n.area_uid, grado: n.grado, isRoot: n.uid === ROOT_UID, x: Math.cos(a) * rr, y: Math.sin(a) * rr, vx: 0, vy: 0 };
      });
      const byUid = new Map(simNodes.map((sn) => [sn.uid, sn]));
      for (const sn of simNodes) if (sn.isRoot) { sn.fx = 0; sn.fy = 0; }
      const links = edges.map((e) => ({ source: e.source, target: e.target }));
      const sim = forceSimulation(simNodes as any, 2)
        .force('link', forceLink(links as any).id((d: any) => d.uid).distance(55).strength(0.2))
        .force('charge', forceManyBody().strength(-55))
        .force('collide', forceCollide().radius((d: any) => obsR(d.grado) + 2).strength(0.85).iterations(2))
        .force('x', forceX(0).strength(0.03))
        .force('y', forceY(0).strength(0.03))
        .alpha(1).alphaDecay(0.028).velocityDecay(0.4).alphaMin(0.003)
        .stop();
      const pre = isReduced ? 300 : 14;
      for (let i = 0; i < pre; i++) sim.tick();
      return { sim, simNodes, byUid, heads: computeHeads(nodes) };
    }
    const areaUids = [...new Set(nodes.map((n) => n.area_uid).filter(Boolean))] as string[];
    // Radio proporcional al tamaño: el mapa completo usa 340, una vecindad (recorte) queda compacta.
    const seedR = Math.max(70, Math.min(340, 40 * Math.sqrt(nodes.length)));
    const seeds = areaSeeds(areaUids, seedR);
    const heads = computeHeads(nodes);
    const simNodes: SimNode2[] = nodes.map((n, i) => {
      const s = seeds.get(n.area_uid ?? '') ?? { x: 0, y: 0 };
      const isHead = heads.headSet.has(n.uid);
      const a = i * GOLDEN;
      const rr = isHead ? 3 : 16 * Math.sqrt((i % 50) + 1);
      return { uid: n.uid, area_uid: n.area_uid, grado: n.grado, isHead, x: s.x + Math.cos(a) * rr, y: s.y + Math.sin(a) * rr, vx: 0, vy: 0 };
    });
    const byUid = new Map(simNodes.map((sn) => [sn.uid, sn]));
    for (const sn of simNodes) {
      if (sn.isHead) { sn.anchor = seeds.get(sn.area_uid ?? '') ?? { x: 0, y: 0 }; sn.headRef = null; sn.fx = sn.anchor.x; sn.fy = sn.anchor.y; }
      else { const hu = heads.heads.get(sn.area_uid ?? ''); sn.headRef = hu ? byUid.get(hu) ?? null : null; }
    }
    const links = edges.map((e) => ({ source: e.source, target: e.target }));
    const sim = forceSimulation(simNodes as any, 2)
      .force('link', forceLink(links as any).id((d: any) => d.uid).distance(40).strength(0.06))
      .force('charge', forceManyBody().strength(-25))
      .force('collide', forceCollide().radius((d: any) => nodeR(d.grado, d.isHead) + 2.5).strength(0.9).iterations(2))
      .force('x', forceX((d: any) => d.isHead ? (d.anchor?.x ?? 0) : (d.headRef?.x ?? 0)).strength((d: any) => d.isHead ? 0.5 : 0.25))
      .force('y', forceY((d: any) => d.isHead ? (d.anchor?.y ?? 0) : (d.headRef?.y ?? 0)).strength((d: any) => d.isHead ? 0.5 : 0.25))
      .alpha(1).alphaDecay(0.028).velocityDecay(0.4).alphaMin(0.003)
      .stop();
    // Pre-tick: con reduced-motion se resuelve ya; si no, parcial y sigue animando.
    const pre = isReduced ? 300 : 14;
    for (let i = 0; i < pre; i++) sim.tick();
    return { sim, simNodes, byUid, heads };
  }, [nodes, edges, obsidian]);

  // Paleta resuelta desde tokens CSS (se recalcula si cambia el tema).
  const palette = useRef({ areas: new Map<string, string>(), ink: '#e5e7eb', line: '#334155', accent: '#60a5fa', bg: '#0a0f1e' });
  const refreshPalette = useCallback(() => {
    const cs = getComputedStyle(document.documentElement);
    const rgb = (name: string, fallback: string) => {
      const v = cs.getPropertyValue(name).trim();
      return v ? `rgb(${v})` : fallback;
    };
    const areas = new Map<string, string>();
    for (const n of nodes) {
      if (n.area_uid && !areas.has(n.area_uid)) {
        areas.set(n.area_uid, rgb(`--area-${n.area_uid}`, 'rgb(148 163 184)'));
      }
    }
    palette.current = {
      areas,
      ink: rgb('--c-ink', '#e5e7eb'),
      line: rgb('--c-line', '#334155'),
      accent: rgb('--c-accent', '#60a5fa'),
      bg: rgb('--c-base', '#0a0f1e'),
    };
    dirty.current = true;
  }, [nodes]);

  useEffect(() => {
    refreshPalette();
    const obs = new MutationObserver(refreshPalette);
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    reduced.current = mq.matches;
    const onMq = () => { reduced.current = mq.matches; };
    mq.addEventListener?.('change', onMq);
    return () => { obs.disconnect(); mq.removeEventListener?.('change', onMq); };
  }, [refreshPalette]);

  const fitView = useCallback((animate = true) => {
    const { w, h } = size.current;
    if (!w || !h || simData.simNodes.length === 0) return;
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const n of simData.simNodes) {
      minX = Math.min(minX, n.x); maxX = Math.max(maxX, n.x);
      minY = Math.min(minY, n.y); maxY = Math.max(maxY, n.y);
    }
    const bw = Math.max(maxX - minX, 1);
    const bh = Math.max(maxY - minY, 1);
    const k = Math.min(Math.min(w / bw, h / bh) * 0.88, MAX_K);
    const cx = (minX + maxX) / 2;
    const cy = (minY + maxY) / 2;
    const to = { k, tx: w / 2 - cx * k, ty: h / 2 - cy * k };
    if (animate && !reduced.current && !document.hidden) {
      camAnim.current = { from: { ...cam.current }, to, start: performance.now(), dur: 380 };
    } else {
      cam.current = to;
      camAnim.current = null;
    }
    dirty.current = true;
  }, [simData]);

  const centerOn = useCallback((uid: string, animate = true) => {
    const n = simData.byUid.get(uid);
    const { w, h } = size.current;
    if (!n || !w) return;
    // Solo panea: mantener el zoom actual conserva visible la vecindad.
    const k = cam.current.k;
    const to = { k, tx: w / 2 - n.x * k, ty: h / 2 - n.y * k };
    if (animate && !reduced.current && !document.hidden) {
      camAnim.current = { from: { ...cam.current }, to, start: performance.now(), dur: 340 };
    } else {
      cam.current = to;
      camAnim.current = null;
    }
    dirty.current = true;
  }, [simData]);

  // Resize + fit inicial
  useEffect(() => {
    const wrap = wrapRef.current;
    const canvas = canvasRef.current;
    if (!wrap || !canvas) return;
    const ro = new ResizeObserver(() => {
      const rect = wrap.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      size.current = { w: rect.width, h: rect.height, dpr };
      canvas.width = Math.round(rect.width * dpr);
      canvas.height = Math.round(rect.height * dpr);
      canvas.style.width = `${rect.width}px`;
      canvas.style.height = `${rect.height}px`;
      dirty.current = true;
      if (!didFit.current && rect.width > 0 && nodes.length > 0) {
        didFit.current = true;
        fitView(false);
      }
    });
    ro.observe(wrap);
    return () => ro.disconnect();
  }, [nodes, fitView]);

  useEffect(() => {
    // Cuando cambian los nodos (vista completa <-> contextual), re-encuadrar.
    // Antes solo marcaba didFit=false, pero el layout-effect corria antes y no lo aplicaba.
    didFit.current = false;
    dirty.current = true;
    fitView(false);
  }, [nodes, simData, fitView]);

  useEffect(() => {
    if (fitSignal > 0) fitView(true);
  }, [fitSignal, fitView]);

  useEffect(() => {
    if (!focusUid) return;
    let tries = 0;
    let timer = 0;
    const attempt = () => {
      if (size.current.w > 0) {
        centerOn(focusUid);
      } else if (tries++ < 30) {
        timer = window.setTimeout(attempt, 50);
      }
    };
    timer = window.setTimeout(attempt, 40);
    return () => clearTimeout(timer);
  }, [focusUid, centerOn]);

  // Dibujo
  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const { w, h, dpr } = size.current;
    const { tx, ty, k } = cam.current;
    const pal = palette.current;
    const P = simData.byUid;
    const __dbg = document.getElementById('ikm-dbg');
    if (__dbg) __dbg.textContent = JSON.stringify({ sel: selectedUid, cam: { k: +cam.current.k.toFixed(2), tx: Math.round(cam.current.tx), ty: Math.round(cam.current.ty) }, w: w, h: h,
      ns: nodes.map((n) => { const q = P.get(n.uid); return [n.title, q ? Math.round(q.x) : null, q ? Math.round(q.y) : null, q && q.isHead ? 1 : 0]; }) });

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);

    const sx = (x: number) => x * k + tx;
    const sy = (y: number) => y * k + ty;

    const activeSet = highlightUids;
    const focusSet = new Set<string>();
    const anchor = hover.current ?? selectedUid;
    if (anchor) {
      focusSet.add(anchor);
      for (const nb of neighbors.get(anchor) ?? []) focusSet.add(nb);
    }

    const nodeAlpha = (n: GraphNode): number => {
      if (highlightAreas && highlightAreas.size > 0) return highlightAreas.has(n.area_uid ?? '') ? 1 : 0.08;
      if (areaFilter && n.area_uid !== areaFilter) return 0.1;
      if (activeSet && !activeSet.has(n.uid)) return 0.14;
      if (anchor && !focusSet.has(n.uid)) return 0.2;
      return 1;
    };

    // Aristas (tenues por defecto, como Obsidian; brillantes al resaltar)
    for (const e of edges) {
      const a = P.get(e.source);
      const b = P.get(e.target);
      if (!a || !b) continue;
      const na = nodeByUid.get(e.source);
      const nb = nodeByUid.get(e.target);
      if (obsidian) {
        const isHl = highlightEdgeUids?.has(e.uid) || (anchor && (e.source === anchor || e.target === anchor));
        const al = isHl ? 0.85 : 0.1;
        const col = isHl ? pal.accent : pal.line;
        ctx.beginPath();
        ctx.moveTo(sx(a.x), sy(a.y));
        ctx.lineTo(sx(b.x), sy(b.y));
        ctx.strokeStyle = col.replace('rgb(', 'rgba(').replace(')', ` / ${al})`);
        ctx.lineWidth = isHl ? 1.6 : 1;
        ctx.stroke();
        continue;
      }
      if (highlightAreas && highlightAreas.size > 0) {
        const both = highlightAreas.has(na?.area_uid ?? '') && highlightAreas.has(nb?.area_uid ?? '');
        const al = both ? 0.85 : 0.03;
        const col = both ? pal.accent : pal.line;
        ctx.beginPath();
        ctx.moveTo(sx(a.x), sy(a.y));
        ctx.lineTo(sx(b.x), sy(b.y));
        ctx.strokeStyle = col.replace('rgb(', 'rgba(').replace(')', ` / ${al})`);
        ctx.lineWidth = both ? 1.6 : 1;
        ctx.stroke();
        continue;
      }
      const isHl = highlightEdgeUids?.has(e.uid)
        || (anchor && (e.source === anchor || e.target === anchor));
      const dimByArea = areaFilter && na?.area_uid !== areaFilter && nb?.area_uid !== areaFilter;
      const dimBySet = activeSet && !(activeSet.has(e.source) && activeSet.has(e.target));
      const spoke = a.isHead || b.isHead;
      let alpha = spoke ? 0.3 : 0.08;
      let width = spoke ? 1.3 : 1;
      let color = pal.line;
      if (isHl) { alpha = 0.9; width = 1.7; color = pal.accent; }
      if (dimByArea || dimBySet) alpha = Math.min(alpha, 0.04);
      else if (anchor && !isHl) alpha = 0.06;
      ctx.beginPath();
      ctx.moveTo(sx(a.x), sy(a.y));
      ctx.lineTo(sx(b.x), sy(b.y));
      ctx.strokeStyle = color.replace('rgb(', 'rgba(').replace(')', ` / ${alpha})`);
      ctx.lineWidth = width;
      ctx.stroke();
    }

    // Nodos (radio por grado = jerarquía; color por área; cabezas con anillo)
    for (const n of nodes) {
      const p = P.get(n.uid);
      if (!p) continue;
      const alpha = nodeAlpha(n);
      const r = Math.max((obsidian ? obsR(n.grado) : nodeR(n.grado, p.isHead)) * k, 1.6);
      const color = obsidian ? toRgb(areaColors[n.area_uid ?? ''] ?? monoColor) : (pal.areas.get(n.area_uid ?? '') ?? pal.line);
      const x = sx(p.x);
      const y = sy(p.y);
      if (x < -40 || x > w + 40 || y < -40 || y > h + 40) continue;

      if (n.uid === selectedUid) {
        ctx.beginPath();
        ctx.arc(x, y, r + 5, 0, Math.PI * 2);
        ctx.fillStyle = pal.accent.replace('rgb(', 'rgba(').replace(')', ' / 0.22)');
        ctx.fill();
      }
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fillStyle = color.replace('rgb(', 'rgba(').replace(')', ` / ${alpha})`);
      ctx.fill();
      if (!obsidian && p.isHead) {
        // Anillo de cabeza: la cabeza global va en accent, las demás en su área.
        ctx.beginPath();
        ctx.arc(x, y, r + 3, 0, Math.PI * 2);
        ctx.lineWidth = 2;
        const ringCol = n.uid === simData.heads.globalHead ? pal.accent : color;
        ctx.strokeStyle = ringCol.replace('rgb(', 'rgba(').replace(')', ` / ${0.75 * alpha})`);
        ctx.stroke();
      }
      if (n.uid === selectedUid || n.uid === hover.current) {
        ctx.lineWidth = 1.5;
        ctx.strokeStyle = pal.ink;
        ctx.stroke();
      }
    }

    // Labels: por defecto solo los títulos estructurales (cabezas de área en
    // mapa; áreas + raíz en Obsidian). El resto aparece al hover/selección/camino.
    ctx.textBaseline = 'middle';
    for (const n of nodes) {
      const p = P.get(n.uid);
      if (!p) continue;
      const isStructural = (p.isHead ?? false) || (obsidian && nodeKind(n.uid) !== 'concept');
      const isRevealed = focusSet.has(n.uid) || (activeSet?.has(n.uid) ?? false);
      if (!isStructural && !isRevealed) continue;
      const na = nodeAlpha(n);
      if (na < 0.3 && !isStructural) continue;
      if (areaFilter && n.area_uid !== areaFilter && !isRevealed) continue;
      const x = sx(p.x);
      const y = sy(p.y);
      if (x < -120 || x > w + 120 || y < -20 || y > h + 20) continue;
      const r = Math.max((obsidian ? obsR(n.grado) : nodeR(n.grado)) * k, 1.6);
      ctx.font = isStructural ? '600 10px system-ui, sans-serif' : '9px system-ui, sans-serif';
      const text = n.title;
      const tw = ctx.measureText(text).width;
      const lx = x + r + 5;
      const ly = y;
      const a = isRevealed ? 1 : 0.95;
      ctx.fillStyle = pal.bg.replace('rgb(', 'rgba(').replace(')', ` / ${0.82 * a})`);
      ctx.beginPath();
      ctx.roundRect(lx - 3, ly - 7, tw + 6, 14, 3);
      ctx.fill();
      ctx.fillStyle = (n.uid === selectedUid || n.uid === hover.current ? pal.accent : pal.ink)
        .replace('rgb(', 'rgba(').replace(')', ` / ${a})`);
      ctx.fillText(text, lx, ly);
    }
  }, [nodes, edges, nodeByUid, neighbors, simData, selectedUid, highlightUids, highlightEdgeUids, highlightAreas, areaFilter, obsidian, monoColor, areaColors]);

  // Primer paint síncrono: no depender de rAF (pestañas en background lo
  // throttlean; el grafo debe verse igual al montar). Mide, encuadra y dibuja.
  useLayoutEffect(() => {
    const canvas = canvasRef.current;
    const wrap = wrapRef.current;
    if (!canvas || !wrap) return;
    const rect = wrap.getBoundingClientRect();
    if (rect.width <= 0 || nodes.length === 0) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    size.current = { w: rect.width, h: rect.height, dpr };
    canvas.width = Math.round(rect.width * dpr);
    canvas.height = Math.round(rect.height * dpr);
    canvas.style.width = `${rect.width}px`;
    canvas.style.height = `${rect.height}px`;
    refreshPalette();
    if (!didFit.current) {
      didFit.current = true;
      fitView(false);
    }
    dirty.current = false;
    draw();
  }, [nodes, draw, fitView, refreshPalette]);

  // Loop rAF: tick-ea la simulación mientras se asienta y dibuja con cambios.
  useEffect(() => {
    let raf = 0;
    const tick = (now: number) => {
      const canvas = canvasRef.current;
      const wrap = wrapRef.current;
      if (canvas && wrap) {
        const rect = wrap.getBoundingClientRect();
        if (rect.width > 0 && (rect.width !== size.current.w || rect.height !== size.current.h)) {
          const dpr = Math.min(window.devicePixelRatio || 1, 2);
          size.current = { w: rect.width, h: rect.height, dpr };
          canvas.width = Math.round(rect.width * dpr);
          canvas.height = Math.round(rect.height * dpr);
          canvas.style.width = `${rect.width}px`;
          canvas.style.height = `${rect.height}px`;
          dirty.current = true;
          if (!didFit.current) {
            didFit.current = true;
            fitView(false);
          }
        }
      }
      // Simulación en vivo (salvo reduced-motion): los nodos se asientan animados.
      if (!reduced.current && simData.sim.alpha() > simData.sim.alphaMin()) {
        simData.sim.tick();
        dirty.current = true;
      }
      const anim = camAnim.current;
      if (anim) {
        const t = Math.min((now - anim.start) / anim.dur, 1);
        const e = easeOutCubic(t);
        cam.current = {
          tx: anim.from.tx + (anim.to.tx - anim.from.tx) * e,
          ty: anim.from.ty + (anim.to.ty - anim.from.ty) * e,
          k: anim.from.k + (anim.to.k - anim.from.k) * e,
        };
        if (t >= 1) camAnim.current = null;
        dirty.current = true;
      }
      if (dirty.current) {
        dirty.current = false;
        draw();
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [draw, fitView, simData]);

  useEffect(() => { dirty.current = true; }, [selectedUid, highlightUids, highlightEdgeUids, highlightAreas, areaFilter, draw]);

  // Hit testing (sobre posiciones vivas de la simulación)
  const hitNode = useCallback((px: number, py: number): SimNode2 | null => {
    const { tx, ty, k } = cam.current;
    const wx = (px - tx) / k;
    const wy = (py - ty) / k;
    let best: SimNode2 | null = null;
    let bestD = Infinity;
    for (const n of simData.simNodes) {
      const d = Math.hypot(n.x - wx, n.y - wy);
      const r = nodeR(n.grado, n.isHead) + 6 / k;
      if (d < Math.max(r, 8 / k) && d < bestD) { best = n; bestD = d; }
    }
    return best;
  }, [simData]);

  const hitEdge = useCallback((px: number, py: number): GraphEdge | null => {
    const { tx, ty, k } = cam.current;
    const wx = (px - tx) / k;
    const wy = (py - ty) / k;
    let best: GraphEdge | null = null;
    let bestD = 6 / k;
    for (const e of edges) {
      const a = simData.byUid.get(e.source);
      const b = simData.byUid.get(e.target);
      if (!a || !b) continue;
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const len2 = dx * dx + dy * dy;
      if (len2 === 0) continue;
      let t = ((wx - a.x) * dx + (wy - a.y) * dy) / len2;
      t = Math.max(0, Math.min(1, t));
      const d = Math.hypot(wx - (a.x + t * dx), wy - (a.y + t * dy));
      if (d < bestD) { bestD = d; best = e; }
    }
    return best;
  }, [edges, simData]);

  const localPoint = (e: { clientX: number; clientY: number }) => {
    const rect = canvasRef.current!.getBoundingClientRect();
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
  };
  const toWorld = (p: { x: number; y: number }) => ({
    x: (p.x - cam.current.tx) / cam.current.k,
    y: (p.y - cam.current.ty) / cam.current.k,
  });

  const onPointerDown = (e: React.PointerEvent<HTMLCanvasElement>) => {
    canvasRef.current?.setPointerCapture(e.pointerId);
    const p = localPoint(e);
    pointers.current.set(e.pointerId, p);
    downAt.current = { x: p.x, y: p.y, moved: false };
    if (pointers.current.size === 1) {
      const n = hitNode(p.x, p.y);
      if (n) {
        // Arrastrar nodo: fijarlo y recalentar la simulación (como Obsidian).
        dragNode.current = n;
        n.fx = n.x; n.fy = n.y;
        simData.sim.alphaTarget(0.3);
        simData.sim.alpha(Math.max(simData.sim.alpha(), 0.3));
        drag.current = null;
        canvasRef.current!.style.cursor = 'grabbing';
      } else {
        drag.current = { x: p.x, y: p.y, tx: cam.current.tx, ty: cam.current.ty, moved: false };
      }
    } else if (pointers.current.size === 2) {
      const [a, b] = [...pointers.current.values()];
      pinch.current = { dist: Math.hypot(a.x - b.x, a.y - b.y), k: cam.current.k };
      drag.current = null;
      if (dragNode.current) { const dn = dragNode.current; if (dn.isHead && dn.anchor) { dn.fx = dn.anchor.x; dn.fy = dn.anchor.y; } else { dn.fx = null; dn.fy = null; } dragNode.current = null; simData.sim.alphaTarget(0); }
    }
  };

  const onPointerMove = (e: React.PointerEvent<HTMLCanvasElement>) => {
    const p = localPoint(e);
    if (pointers.current.has(e.pointerId)) pointers.current.set(e.pointerId, p);
    if (downAt.current && Math.hypot(p.x - downAt.current.x, p.y - downAt.current.y) > 4) downAt.current.moved = true;

    if (pinch.current && pointers.current.size === 2) {
      const [a, b] = [...pointers.current.values()];
      const dist = Math.hypot(a.x - b.x, a.y - b.y);
      const mid = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
      const k = Math.max(MIN_K, Math.min(MAX_K, pinch.current.k * (dist / pinch.current.dist)));
      const wx = (mid.x - cam.current.tx) / cam.current.k;
      const wy = (mid.y - cam.current.ty) / cam.current.k;
      cam.current = { k, tx: mid.x - wx * k, ty: mid.y - wy * k };
      dirty.current = true;
      return;
    }

    if (dragNode.current && pointers.current.size === 1) {
      const w = toWorld(p);
      dragNode.current.fx = w.x;
      dragNode.current.fy = w.y;
      dirty.current = true;
      return;
    }

    if (drag.current && pointers.current.size === 1) {
      const dx = p.x - drag.current.x;
      const dy = p.y - drag.current.y;
      if (Math.abs(dx) + Math.abs(dy) > 4) drag.current.moved = true;
      if (drag.current.moved) {
        camAnim.current = null;
        cam.current = { ...cam.current, tx: drag.current.tx + dx, ty: drag.current.ty + dy };
        dirty.current = true;
      }
      return;
    }

    // Hover
    const n = hitNode(p.x, p.y);
    const uid = n?.uid ?? null;
    if (uid !== hover.current) {
      hover.current = uid;
      dirty.current = true;
      onHover?.(uid);
      canvasRef.current!.style.cursor = uid ? 'pointer' : 'grab';
    }
  };

  const onPointerUp = (e: React.PointerEvent<HTMLCanvasElement>) => {
    const p = localPoint(e);
    const wasDrag = drag.current?.moved;
    const wasNodeDrag = dragNode.current && downAt.current?.moved;
    const clickedNode = dragNode.current && !downAt.current?.moved ? dragNode.current : null;
    pointers.current.delete(e.pointerId);
    if (pointers.current.size < 2) pinch.current = null;
    if (dragNode.current) {
      const dn = dragNode.current;
      if (dn.isHead && dn.anchor) { dn.fx = dn.anchor.x; dn.fy = dn.anchor.y; }
      else { dn.fx = null; dn.fy = null; }
      dragNode.current = null;
      simData.sim.alphaTarget(0);
    }
    if (pointers.current.size === 0) {
      if (clickedNode) {
        onSelect?.(clickedNode.uid);
      } else if (!wasDrag && !wasNodeDrag) {
        const n = hitNode(p.x, p.y);
        if (n) {
          onSelect?.(n.uid);
        } else {
          const edge = hitEdge(p.x, p.y);
          if (edge) onEdgeSelect?.(edge.uid);
          else onSelect?.(null);
        }
      }
      drag.current = null;
      downAt.current = null;
      canvasRef.current!.style.cursor = 'grab';
    }
  };

  const onWheel = (e: React.WheelEvent<HTMLCanvasElement>) => {
    const p = localPoint(e);
    const factor = Math.exp(-e.deltaY * 0.0012);
    const k = Math.max(MIN_K, Math.min(MAX_K, cam.current.k * factor));
    const wx = (p.x - cam.current.tx) / cam.current.k;
    const wy = (p.y - cam.current.ty) / cam.current.k;
    camAnim.current = null;
    cam.current = { k, tx: p.x - wx * k, ty: p.y - wy * k };
    dirty.current = true;
  };

  // Teclado sobre el canvas: pan, zoom, fit. La navegación por conceptos
  // tiene lista paralela en GraphPage (criterio de accesibilidad §15.5).
  const onKeyDown = (e: React.KeyboardEvent<HTMLCanvasElement>) => {
    const step = 48;
    const c = cam.current;
    let handled = true;
    switch (e.key) {
      case 'ArrowLeft': cam.current = { ...c, tx: c.tx + step }; break;
      case 'ArrowRight': cam.current = { ...c, tx: c.tx - step }; break;
      case 'ArrowUp': cam.current = { ...c, ty: c.ty + step }; break;
      case 'ArrowDown': cam.current = { ...c, ty: c.ty - step }; break;
      case '+': case '=': cam.current = { ...c, k: Math.min(MAX_K, c.k * 1.25) }; break;
      case '-': case '_': cam.current = { ...c, k: Math.max(MIN_K, c.k / 1.25) }; break;
      case '0': fitView(); break;
      case 'Escape': onSelect?.(null); break;
      default: handled = false;
    }
    if (handled) {
      e.preventDefault();
      camAnim.current = null;
      dirty.current = true;
    }
  };

  // Wheel nativo no-pasivo (React marca wheel como passive en algunos casos).
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const prevent = (e: WheelEvent) => e.preventDefault();
    canvas.addEventListener('wheel', prevent, { passive: false });
    return () => canvas.removeEventListener('wheel', prevent);
  }, []);

  return (
    <div ref={wrapRef} className={`relative overflow-hidden ${className}`}>
      <canvas
        ref={canvasRef}
        tabIndex={0}
        role="application"
        aria-label="Grafo de conceptos con layout de fuerzas. Arrastrá un nodo para moverlo, arrastrá el fondo para paneo, rueda para zoom, click para seleccionar. Usá las flechas para moverte, más y menos para zoom, 0 para encuadrar. La lista de conceptos debajo ofrece navegación por teclado completa."
        className="block outline-none cursor-grab focus-visible:ring-2 focus-visible:ring-accent/70"
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerCancel={onPointerUp}
        onWheel={onWheel}
        onKeyDown={onKeyDown}
      />
    </div>
  );
}