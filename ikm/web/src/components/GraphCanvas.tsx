/** Grafo 2D en canvas (DR-L10-02): 255 nodos / 913 aristas a ≥30 fps sin
 * dependencias de grafos. Posiciones precalculadas del release.
 * - Labels solo en hover, selección y vecinos (criterio §15.3).
 * - Pan con drag, zoom con rueda/pinch, click en nodo o arista.
 * - prefers-reduced-motion: sin animaciones de cámara.
 * - Colores resueltos desde los tokens CSS (canvas no lee variables).
 */
import { useCallback, useEffect, useLayoutEffect, useMemo, useRef } from 'react';
import type { GraphEdge, GraphNode } from '../lib/types';

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
}

interface Camera { tx: number; ty: number; k: number }

const MIN_K = 0.15;
const MAX_K = 8;

function easeOutCubic(t: number): number {
  return 1 - Math.pow(1 - t, 3);
}

export default function GraphCanvas({
  nodes, edges, selectedUid = null, highlightUids = null, highlightEdgeUids = null,
  highlightAreas = null, focusUid = null, areaFilter = null, fitSignal = 0, onSelect, onEdgeSelect, onHover, className = '',
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
    if (!w || !h || nodes.length === 0) return;
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const n of nodes) {
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
  }, [nodes]);

  const centerOn = useCallback((uid: string, animate = true) => {
    const n = nodeByUid.get(uid);
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
  }, [nodeByUid]);

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
    // El tick aplica el fit en cuanto conoce el tamaño real del contenedor.
    didFit.current = false;
    dirty.current = true;
  }, [nodes]);

  useEffect(() => {
    if (fitSignal > 0) fitView(true);
  }, [fitSignal, fitView]);

  useEffect(() => {
    if (!focusUid) return;
    // Si el tamaño aún no se conoce, el tick encuadra primero (didFit) y
    // reintentamos el centrado en el próximo frame con tamaño ya disponible.
    let tries = 0;
    const attempt = () => {
      if (size.current.w > 0) {
        centerOn(focusUid);
      } else if (tries++ < 30) {
        timer = window.setTimeout(attempt, 50);
      }
    };
    let timer = window.setTimeout(attempt, 40);
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

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);

    const sx = (x: number) => x * k + tx;
    const sy = (y: number) => y * k + ty;

    const activeSet = highlightUids;
    const focusSet = new Set<string>();
    const labelUids = new Set<string>();
    const anchor = hover.current ?? selectedUid;
    if (anchor) {
      focusSet.add(anchor);
      labelUids.add(anchor);
      for (const nb of neighbors.get(anchor) ?? []) {
        focusSet.add(nb);
        labelUids.add(nb);
      }
    }
    if (selectedUid) labelUids.add(selectedUid);
    if (activeSet) for (const u of activeSet) labelUids.add(u);

    const nodeAlpha = (n: GraphNode): number => {
      if (highlightAreas && highlightAreas.size > 0) return highlightAreas.has(n.area_uid ?? '') ? 1 : 0.08;
      if (areaFilter && n.area_uid !== areaFilter) return 0.1;
      if (activeSet && !activeSet.has(n.uid)) return 0.14;
      if (anchor && !focusSet.has(n.uid)) return 0.22;
      return 1;
    };

    // Halos suaves por área (agrupación visual)
    const areaBounds = new Map<string, { cx: number; cy: number; r: number; count: number }>();
    for (const n of nodes) {
      if (!n.area_uid) continue;
      const b = areaBounds.get(n.area_uid) ?? { cx: 0, cy: 0, r: 0, count: 0 };
      b.cx += n.x; b.cy += n.y; b.count += 1;
      areaBounds.set(n.area_uid, b);
    }
    for (const [areaUid, b] of areaBounds) {
      const cx = b.cx / b.count;
      const cy = b.cy / b.count;
      let r = 0;
      for (const n of nodes) {
        if (n.area_uid === areaUid) r = Math.max(r, Math.hypot(n.x - cx, n.y - cy));
      }
      const color = pal.areas.get(areaUid) ?? pal.line;
      const dim = areaFilter && areaUid !== areaFilter;
      ctx.beginPath();
      ctx.arc(sx(cx), sy(cy), (r + 34) * k, 0, Math.PI * 2);
      ctx.fillStyle = color.replace('rgb(', 'rgba(').replace(')', ` / ${dim ? 0.02 : 0.05})`);
      ctx.fill();
    }

    // Aristas
    for (const e of edges) {
      const a = nodeByUid.get(e.source);
      const b = nodeByUid.get(e.target);
      if (!a || !b) continue;
      if (highlightAreas && highlightAreas.size > 0) {
        const both = highlightAreas.has(a.area_uid ?? '') && highlightAreas.has(b.area_uid ?? '');
        const al = both ? 0.85 : 0.03;
        const col = both ? pal.accent : (pal.areas.get(a.area_uid ?? '') ?? pal.line);
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
      const dimByArea = areaFilter && a.area_uid !== areaFilter && b.area_uid !== areaFilter;
      const dimBySet = activeSet && !(activeSet.has(e.source) && activeSet.has(e.target));
      let alpha = 0.16;
      let width = 1;
      let color = pal.line;
      if (isHl) { alpha = 0.85; width = 1.6; color = pal.accent; }
      if (dimByArea || dimBySet) alpha = Math.min(alpha, 0.05);
      else if (anchor && !isHl) alpha = 0.07;
      ctx.beginPath();
      ctx.moveTo(sx(a.x), sy(a.y));
      ctx.lineTo(sx(b.x), sy(b.y));
      ctx.strokeStyle = color.startsWith('rgb(')
        ? color.replace('rgb(', 'rgba(').replace(')', ` / ${alpha})`)
        : color;
      ctx.lineWidth = width;
      ctx.stroke();
    }

    // Nodos
    for (const n of nodes) {
      const alpha = nodeAlpha(n);
      const r = Math.min(4 + Math.sqrt(n.grado) * 1.4, 12) * Math.max(k, 0.55);
      const color = pal.areas.get(n.area_uid ?? '') ?? pal.line;
      const x = sx(n.x);
      const y = sy(n.y);
      if (x < -40 || x > w + 40 || y < -40 || y > h + 40) continue;

      if (n.uid === selectedUid) {
        ctx.beginPath();
        ctx.arc(x, y, r + 6, 0, Math.PI * 2);
        ctx.fillStyle = pal.accent.replace('rgb(', 'rgba(').replace(')', ' / 0.22)');
        ctx.fill();
      }
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fillStyle = color.startsWith('rgb(')
        ? color.replace('rgb(', 'rgba(').replace(')', ` / ${alpha})`)
        : color;
      ctx.fill();
      if (n.uid === selectedUid || n.uid === hover.current) {
        ctx.lineWidth = 1.5;
        ctx.strokeStyle = pal.ink;
        ctx.stroke();
      }
    }

    // Labels (solo hover/selección/vecinos/foco)
    ctx.font = '11px system-ui, sans-serif';
    ctx.textBaseline = 'middle';
    for (const uid of labelUids) {
      const n = nodeByUid.get(uid);
      if (!n) continue;
      if (areaFilter && n.area_uid !== areaFilter) continue;
      const x = sx(n.x);
      const y = sy(n.y);
      if (x < -100 || x > w + 100 || y < -20 || y > h + 20) continue;
      const r = Math.min(4 + Math.sqrt(n.grado) * 1.4, 12) * Math.max(k, 0.55);
      const text = n.title;
      const tw = ctx.measureText(text).width;
      const lx = x + r + 6;
      const ly = y;
      ctx.fillStyle = pal.bg.replace('rgb(', 'rgba(').replace(')', ' / 0.82)');
      ctx.beginPath();
      ctx.roundRect(lx - 4, ly - 9, tw + 8, 18, 4);
      ctx.fill();
      ctx.fillStyle = uid === selectedUid || uid === hover.current ? pal.accent : pal.ink;
      ctx.fillText(text, lx, ly);
    }
  }, [nodes, edges, nodeByUid, neighbors, selectedUid, highlightUids, highlightEdgeUids, highlightAreas, areaFilter]);

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

  // Loop rAF: dibuja solo cuando hay cambios o animación de cámara.
  // Además verifica el tamaño del contenedor en cada frame (self-healing):
  // ResizeObserver puede llegar tarde en dev; sin tamaño, fit/center se abortan.
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
  }, [draw, fitView]);

  useEffect(() => { dirty.current = true; }, [selectedUid, highlightUids, highlightEdgeUids, highlightAreas, areaFilter, draw]);

  // Hit testing
  const hitNode = useCallback((px: number, py: number): GraphNode | null => {
    const { tx, ty, k } = cam.current;
    const wx = (px - tx) / k;
    const wy = (py - ty) / k;
    let best: GraphNode | null = null;
    let bestD = 14 / k;
    for (const n of nodes) {
      const d = Math.hypot(n.x - wx, n.y - wy);
      const r = Math.min(4 + Math.sqrt(n.grado) * 1.4, 12) / k + 6 / k;
      if (d < Math.max(r, 8 / k) && d < bestD + 14 / k) {
        if (!best || d < bestD) { best = n; bestD = d; }
      }
    }
    return best;
  }, [nodes]);

  const hitEdge = useCallback((px: number, py: number): GraphEdge | null => {
    const { tx, ty, k } = cam.current;
    const wx = (px - tx) / k;
    const wy = (py - ty) / k;
    let best: GraphEdge | null = null;
    let bestD = 6 / k;
    for (const e of edges) {
      const a = nodeByUid.get(e.source);
      const b = nodeByUid.get(e.target);
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
  }, [edges, nodeByUid]);

  const localPoint = (e: { clientX: number; clientY: number }) => {
    const rect = canvasRef.current!.getBoundingClientRect();
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
  };

  const onPointerDown = (e: React.PointerEvent<HTMLCanvasElement>) => {
    canvasRef.current?.setPointerCapture(e.pointerId);
    const p = localPoint(e);
    pointers.current.set(e.pointerId, p);
    if (pointers.current.size === 1) {
      drag.current = { x: p.x, y: p.y, tx: cam.current.tx, ty: cam.current.ty, moved: false };
    } else if (pointers.current.size === 2) {
      const [a, b] = [...pointers.current.values()];
      pinch.current = { dist: Math.hypot(a.x - b.x, a.y - b.y), k: cam.current.k };
      drag.current = null;
    }
  };

  const onPointerMove = (e: React.PointerEvent<HTMLCanvasElement>) => {
    const p = localPoint(e);
    if (pointers.current.has(e.pointerId)) pointers.current.set(e.pointerId, p);

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
    pointers.current.delete(e.pointerId);
    if (pointers.current.size < 2) pinch.current = null;
    if (pointers.current.size === 0) {
      if (!wasDrag) {
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
    }
  };

  const onWheel = (e: React.WheelEvent<HTMLCanvasElement>) => {
    // El preventDefault real lo hace el listener nativo no-pasivo (abajo).
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
        aria-label="Grafo de conceptos. Usá las flechas para moverte, más y menos para zoom, 0 para encuadrar. La lista de conceptos debajo ofrece navegación por teclado completa."
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