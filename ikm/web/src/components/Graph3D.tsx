/** Grafo 3D (Three.js + d3-force-3d, layout client-side). Estética tech neón
 * con bloom. Misma interfaz que GraphCanvas para alternar 2D/3D.
 * - Nodos instanciados (255 esferas), aristas con glow aditivo.
 * - Layout por fuerza con clustering por área (centroides en esfera).
 * - Labels CSS2D solo en hover/selección/vecinos (criterio §15.3).
 * - Cámara orbital, raycasting de nodos y aristas, animaciones fluidas.
 * - prefers-reduced-motion: sin tween de cámara ni pulso.
 */
import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/examples/jsm/renderers/CSS2DRenderer.js';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import {
  forceSimulation, forceLink, forceManyBody, forceCollide, forceX, forceY, forceZ,
} from 'd3-force-3d';
import type { GraphNode, GraphEdge } from '../lib/types';
import { areaCentroids, initialPositions, computeHeads, type SimNode, type HeadInfo } from '../lib/forceLayout';
import { nodeKind, ROOT_UID } from '../lib/obsidianGraph';

/** Modo Obsidian 3D: la raíz (grado ~265) debe verse mucho mayor; tope alto. */
const obsR3D = (grado: number) => Math.min(4 + Math.sqrt(grado) * 2.2, 80);

export interface Graph3DProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  selectedUid?: string | null;
  highlightUids?: Set<string> | null;
  highlightEdgeUids?: Set<string> | null;
  highlightAreas?: Set<string> | null;
  focusUid?: string | null;
  areaFilter?: string | null;
  fitSignal?: number;
  onSelect?: (uid: string | null) => void;
  onEdgeSelect?: (edgeUid: string) => void;
  onHover?: (uid: string | null) => void;
  className?: string;
  obsidian?: boolean;
  monoColor?: string;
  areaColors?: Record<string, string>;
}

interface CamTween { fromPos: THREE.Vector3; toPos: THREE.Vector3; fromTarget: THREE.Vector3; toTarget: THREE.Vector3; start: number; dur: number }

interface State {
  renderer: THREE.WebGLRenderer;
  labelRenderer: CSS2DRenderer;
  scene: THREE.Scene;
  camera: THREE.PerspectiveCamera;
  composer: EffectComposer;
  controls: OrbitControls;
  nodesMesh: THREE.InstancedMesh;
  edgesLine: THREE.LineSegments;
  edgesGeom: THREE.BufferGeometry;
  simNodes: SimNode[];
  edgeUids: string[];
  nodeIndex: Map<string, number>;
  labels: Map<string, CSS2DObject>;
  sim: any;
  heads: HeadInfo;
  raycaster: THREE.Raycaster;
  pointer: THREE.Vector2;
  hoverUid: string | null;
  palette: Map<string, THREE.Color>;
  bg: THREE.Color;
  accent: THREE.Color;
  raf: number;
  disposed: boolean;
  camTween: CamTween | null;
  width: number;
  height: number;
  reduced: boolean;
  dummy: THREE.Object3D;
  downX: number;
  downY: number;
  lastPointer: number;
}

function cssColor(name: string, fallback: string): THREE.Color {
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  if (!v) return new THREE.Color(fallback);
  return new THREE.Color(`rgb(${v.split(/\s+/).join(',')})`);
}

function resolvePalette(nodes: GraphNode[]) {
  const areas = new Map<string, THREE.Color>();
  for (const n of nodes) {
    if (n.area_uid && !areas.has(n.area_uid)) {
      areas.set(n.area_uid, cssColor(`--area-${n.area_uid}`, '#94a3b8'));
    }
  }
  return { areas, bg: cssColor('--c-base', '#0a0f1e'), accent: cssColor('--c-accent', '#60a5fa') };
}

/** Color y visibilidad por nodo/arista/label según foco, filtro y camino. */
function applyHighlight(s: State, p: Graph3DProps) {
  const anchor = s.hoverUid ?? p.selectedUid ?? null;
  const neighborSet = new Set<string>();
  if (anchor) {
    neighborSet.add(anchor);
    for (const e of p.edges) {
      if (e.source === anchor) neighborSet.add(e.target);
      if (e.target === anchor) neighborSet.add(e.source);
    }
  }
  const pathSet = p.highlightUids ?? null;

  const nodeVisible = (n: SimNode): number => {
    if (p.highlightAreas && p.highlightAreas.size > 0) return p.highlightAreas.has(n.area_uid ?? '') ? 1 : 0.08;
    if (p.areaFilter && n.area_uid !== p.areaFilter) return 0.1;
    if (pathSet && !pathSet.has(n.uid)) return 0.12;
    if (anchor && !neighborSet.has(n.uid)) return 0.16;
    return 1;
  };

  const c = new THREE.Color();
  for (let i = 0; i < s.simNodes.length; i++) {
    const n = s.simNodes[i];
    const base = p.obsidian
      ? new THREE.Color(p.areaColors?.[n.area_uid ?? ''] ?? p.monoColor ?? '#94a3b8')
      : (s.palette.get(n.area_uid ?? '') ?? s.accent);
    const f = nodeVisible(n);
    c.copy(base).multiplyScalar(f);
    if (!p.obsidian && n.isHead && f >= 1) c.copy(base).multiplyScalar(1.3);
    if (!p.obsidian && n.uid === s.heads.globalHead && f >= 1) c.copy(s.accent).multiplyScalar(1.35);
    if (pathSet && pathSet.has(n.uid)) c.copy(base).multiplyScalar(1.4);
    if (n.uid === p.selectedUid) c.copy(s.accent).multiplyScalar(1.5);
    s.nodesMesh.setColorAt(i, c);
  }
  if (s.nodesMesh.instanceColor) s.nodesMesh.instanceColor.needsUpdate = true;

  // aristas
  const posAttr = s.edgesGeom.getAttribute('color') as THREE.BufferAttribute;
  const ec = new THREE.Color();
  for (let i = 0; i < s.edgeUids.length; i++) {
    const e = p.edges[i];
    const a = s.simNodes[s.nodeIndex.get(e.source)!];
    const b = s.simNodes[s.nodeIndex.get(e.target)!];
    if (p.highlightAreas && p.highlightAreas.size > 0) {
      const both = p.highlightAreas.has(a.area_uid ?? '') && p.highlightAreas.has(b.area_uid ?? '');
      const fa = both ? 1.25 : 0.03;
      const ca = both ? s.accent : (s.palette.get(a.area_uid ?? '') ?? s.accent);
      ec.copy(ca).multiplyScalar(fa);
      posAttr.setXYZ(i * 2, ec.r, ec.g, ec.b);
      posAttr.setXYZ(i * 2 + 1, ec.r, ec.g, ec.b);
      continue;
    }
    const isHl = (p.highlightEdgeUids?.has(e.uid)) || (anchor && (e.source === anchor || e.target === anchor));
    const dimArea = p.areaFilter && a.area_uid !== p.areaFilter && b.area_uid !== p.areaFilter;
    const dimPath = pathSet && !(pathSet.has(e.source) && pathSet.has(e.target));
    const spoke = a.isHead || b.isHead;
    let f = p.obsidian ? 0.12 : (spoke ? 0.5 : 0.18);
    if (isHl) f = 1.3;
    if (dimArea || dimPath) f = 0.04;
    else if (anchor && !isHl) f = 0.06;
    const col = isHl ? s.accent : (p.obsidian ? new THREE.Color(p.monoColor ?? '#94a3b8') : (s.palette.get(a.area_uid ?? '') ?? s.accent));
    ec.copy(col).multiplyScalar(f);
    posAttr.setXYZ(i * 2, ec.r, ec.g, ec.b);
    posAttr.setXYZ(i * 2 + 1, ec.r, ec.g, ec.b);
  }
  posAttr.needsUpdate = true;

  // labels: hover, selección, vecinos, camino + cabezas de área siempre visibles
  const show = new Set<string>(neighborSet);
  for (const h of s.heads.headSet) show.add(h);
  if (p.obsidian) for (const sn of s.simNodes) if (nodeKind(sn.uid) !== 'concept') show.add(sn.uid);
  if (p.selectedUid) show.add(p.selectedUid);
  if (pathSet) for (const u of pathSet) show.add(u);
  for (const [uid, label] of s.labels) {
    const vis = show.has(uid) && !(p.areaFilter && s.simNodes[s.nodeIndex.get(uid)!].area_uid !== p.areaFilter);
    (label.element as HTMLElement).style.opacity = vis ? '1' : '0';
  }
}

function syncPositions(s: State, p: Graph3DProps, now: number) {
  const pulse = s.reduced ? 1 : 1 + Math.sin(now * 0.004) * 0.12;
  for (let i = 0; i < s.simNodes.length; i++) {
    const n = s.simNodes[i];
    const scale = n.radius * (n.uid === p.selectedUid ? pulse : 1);
    s.dummy.position.set(n.x, n.y, n.z);
    s.dummy.scale.setScalar(scale);
    s.dummy.updateMatrix();
    s.nodesMesh.setMatrixAt(i, s.dummy.matrix);
    const label = s.labels.get(n.uid);
    if (label) label.position.set(n.x, n.y + n.radius + 4, n.z);
  }
  s.nodesMesh.instanceMatrix.needsUpdate = true;

  const posAttr = s.edgesGeom.getAttribute('position') as THREE.BufferAttribute;
  for (let i = 0; i < p.edges.length; i++) {
    const e = p.edges[i];
    const a = s.simNodes[s.nodeIndex.get(e.source)!];
    const b = s.simNodes[s.nodeIndex.get(e.target)!];
    posAttr.setXYZ(i * 2, a.x, a.y, a.z);
    posAttr.setXYZ(i * 2 + 1, b.x, b.y, b.z);
  }
  posAttr.needsUpdate = true;
  s.edgesGeom.computeBoundingSphere();
}

function fitCamera(s: State) {
  // encuadrar toda la nube: cámara alejada según extensión
  let maxR = 1;
  for (const n of s.simNodes) maxR = Math.max(maxR, Math.hypot(n.x, n.y, n.z));
  const dist = maxR * 2.4 + 200;
  const toPos = new THREE.Vector3(0, dist * 0.25, dist);
  const toTarget = new THREE.Vector3(0, 0, 0);
  if (s.reduced) {
    s.camera.position.copy(toPos);
    s.controls.target.copy(toTarget);
  } else {
    s.camTween = { fromPos: s.camera.position.clone(), toPos, fromTarget: s.controls.target.clone(), toTarget, start: performance.now(), dur: 700 };
  }
}

function focusNode(s: State, uid: string) {
  const i = s.nodeIndex.get(uid);
  if (i === undefined) return;
  const n = s.simNodes[i];
  const target = new THREE.Vector3(n.x, n.y, n.z);
  const dir = s.camera.position.clone().sub(s.controls.target).normalize();
  const toPos = target.clone().add(dir.multiplyScalar(320));
  if (s.reduced) {
    s.controls.target.copy(target);
    s.camera.position.copy(toPos);
  } else {
    s.camTween = { fromPos: s.camera.position.clone(), toPos, fromTarget: s.controls.target.clone(), toTarget: target, start: performance.now(), dur: 650 };
  }
}

function frameNodes(s: State, uids: string[]) {
  const pts = uids.map((u) => s.simNodes[s.nodeIndex.get(u)!]).filter(Boolean);
  if (!pts.length) return;
  let cx = 0, cy = 0, cz = 0;
  for (const n of pts) { cx += n.x; cy += n.y; cz += n.z; }
  cx /= pts.length; cy /= pts.length; cz /= pts.length;
  let maxR = 1;
  for (const n of pts) maxR = Math.max(maxR, Math.hypot(n.x - cx, n.y - cy, n.z - cz));
  const dist = maxR * 2.6 + 200;
  const target = new THREE.Vector3(cx, cy, cz);
  const dir = s.camera.position.clone().sub(s.controls.target).normalize();
  const toPos = target.clone().add(dir.multiplyScalar(dist));
  if (s.reduced) { s.controls.target.copy(target); s.camera.position.copy(toPos); }
  else s.camTween = { fromPos: s.camera.position.clone(), toPos, fromTarget: s.controls.target.clone(), toTarget: target, start: performance.now(), dur: 700 };
}

function stepCamTween(s: State, now: number) {
  const t = s.camTween;
  if (!t) return;
  const k = Math.min((now - t.start) / t.dur, 1);
  const e = 1 - Math.pow(1 - k, 3);
  s.camera.position.lerpVectors(t.fromPos, t.toPos, e);
  s.controls.target.lerpVectors(t.fromTarget, t.toTarget, e);
  if (k >= 1) s.camTween = null;
}

export default function Graph3D(props: Graph3DProps) {
  const mountRef = useRef<HTMLDivElement>(null);
  const propsRef = useRef(props);
  propsRef.current = props;
  const st = useRef<State | null>(null);

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount || props.nodes.length === 0) return;

    const width = mount.clientWidth || 800;
    const height = mount.clientHeight || 600;
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const { areas, bg, accent } = resolvePalette(props.nodes);

    const scene = new THREE.Scene();
    scene.background = bg;
    scene.fog = new THREE.FogExp2(bg.getHex(), 0.00085);

    const camera = new THREE.PerspectiveCamera(60, width / height, 1, 8000);
    camera.position.set(0, 260, 1250);

    // Sin antialias nativo: el compositor ya resuelve MSAA sobre su target (doble AA = desperdicio).
    const renderer = new THREE.WebGLRenderer({ antialias: false, powerPreference: 'high-performance' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
    renderer.setSize(width, height);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    mount.appendChild(renderer.domElement);

    const labelRenderer = new CSS2DRenderer();
    labelRenderer.setSize(width, height);
    labelRenderer.domElement.style.position = 'absolute';
    labelRenderer.domElement.style.top = '0';
    labelRenderer.domElement.style.left = '0';
    labelRenderer.domElement.style.pointerEvents = 'none';
    labelRenderer.domElement.style.zIndex = '5';
    mount.appendChild(labelRenderer.domElement);

    // Render target con MSAA + HDR: bordes limpios a través del bloom y glow de calidad.
    const rt = new THREE.WebGLRenderTarget(width, height, { samples: 2, type: THREE.HalfFloatType });
    const composer = new EffectComposer(renderer, rt);
    composer.addPass(new RenderPass(scene, camera));
    const bloom = new UnrealBloomPass(new THREE.Vector2(width / 2, height / 2), props.obsidian ? 0.35 : 0.9, 0.55, props.obsidian ? 0.5 : 0.18);
    composer.addPass(bloom);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.06;
    controls.rotateSpeed = 0.6;
    controls.minDistance = 120;
    controls.maxDistance = 3200;
    controls.autoRotateSpeed = 0.45;

    // nodos instanciados
    const sphere = new THREE.SphereGeometry(1, 14, 14);
    const nodeMat = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
    const nodesMesh = new THREE.InstancedMesh(sphere, nodeMat, props.nodes.length);
    nodesMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    scene.add(nodesMesh);

    // aristas
    const edgesGeom = new THREE.BufferGeometry();
    const ePos = new Float32Array(props.edges.length * 6);
    const eCol = new Float32Array(props.edges.length * 6);
    edgesGeom.setAttribute('position', new THREE.BufferAttribute(ePos, 3).setUsage(THREE.DynamicDrawUsage));
    edgesGeom.setAttribute('color', new THREE.BufferAttribute(eCol, 3).setUsage(THREE.DynamicDrawUsage));
    const edgeMat = new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.95, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false });
    const edgesLine = new THREE.LineSegments(edgesGeom, edgeMat);
    scene.add(edgesLine);

    // simulación: modo Obsidian (mind-map jerárquico, fuerza pura, raíz al
    // centro) o modo mapa (cabezas de área fijadas, miembros orbitando).
    const areaUids = [...new Set(props.nodes.map((n) => n.area_uid).filter(Boolean))] as string[];
    const heads = computeHeads(props.nodes);
    const simLinks = props.edges.map((e) => ({ source: e.source, target: e.target, uid: e.uid }));
    const edgeUids = props.edges.map((e) => e.uid);
    let simNodes: SimNode[];
    let sim: any;
    if (props.obsidian) {
      simNodes = props.nodes.map((n, i) => {
        const a = i * 2.399963;
        const rr = n.uid === ROOT_UID ? 0 : 40 + 16 * Math.sqrt((i % 60) + 1);
        const radius = nodeKind(n.uid) === 'area' ? obsR3D(n.grado) * 1.5 : obsR3D(n.grado);
        return { ...n, x: Math.cos(a) * rr, y: Math.sin(a * 1.3) * rr, z: Math.sin(a) * rr, radius };
      });
      for (const sn of simNodes) if (sn.uid === ROOT_UID) { (sn as any).fx = 0; (sn as any).fy = 0; (sn as any).fz = 0; }
      sim = forceSimulation(simNodes as any, 3)
        .force('link', forceLink(simLinks as any).id((d: any) => d.uid).distance(85).strength(0.18))
        .force('charge', forceManyBody().strength(-130))
        .force('collide', forceCollide().radius((d: any) => d.radius + 3).strength(0.85))
        .force('x', forceX(0).strength(0.02))
        .force('y', forceY(0).strength(0.02))
        .force('z', forceZ(0).strength(0.02))
        .alpha(1).alphaDecay(0.022).velocityDecay(0.35);
    } else {
      const centroids = areaCentroids(areaUids);
      simNodes = initialPositions(props.nodes, centroids, 90, heads.headSet);
      const idxTmp = new Map(simNodes.map((n, i) => [n.uid, i]));
      for (const sn of simNodes) {
        if (sn.isHead) {
          sn.anchor = centroids.get(sn.area_uid ?? '') ?? { x: 0, y: 0, z: 0 };
          sn.headRef = null;
          (sn as any).fx = sn.anchor.x; (sn as any).fy = sn.anchor.y; (sn as any).fz = sn.anchor.z;
        } else {
          const hu = heads.heads.get(sn.area_uid ?? '');
          sn.headRef = hu ? simNodes[idxTmp.get(hu)!] : null;
        }
      }
      const tx = (d: any) => d.isHead ? (d.anchor?.x ?? 0) : (d.headRef?.x ?? 0);
      const ty = (d: any) => d.isHead ? (d.anchor?.y ?? 0) : (d.headRef?.y ?? 0);
      const tz = (d: any) => d.isHead ? (d.anchor?.z ?? 0) : (d.headRef?.z ?? 0);
      sim = forceSimulation(simNodes as any, 3)
        .force('link', forceLink(simLinks as any).id((d: any) => d.uid).distance(50).strength(0.06))
        .force('charge', forceManyBody().strength(-25))
        .force('collide', forceCollide().radius((d: any) => d.radius + 3).strength(0.85))
        .force('x', forceX(tx).strength((d: any) => d.isHead ? 0.5 : 0.25))
        .force('y', forceY(ty).strength((d: any) => d.isHead ? 0.5 : 0.25))
        .force('z', forceZ(tz).strength((d: any) => d.isHead ? 0.5 : 0.25))
        .alpha(1).alphaDecay(0.022).velocityDecay(0.35);
    }
    const nodeIndex = new Map(simNodes.map((n, i) => [n.uid, i]));

    // labels
    const labels = new Map<string, CSS2DObject>();
    for (const n of simNodes) {
      const div = document.createElement('div');
      const isHeadLike = n.isHead || (props.obsidian && nodeKind(n.uid) !== 'concept');
      div.className = isHeadLike ? 'graph3d-label graph3d-label-head' : 'graph3d-label';
      div.textContent = n.title;
      div.style.opacity = '0';
      const obj = new CSS2DObject(div);
      obj.position.set(n.x, n.y, n.z);
      scene.add(obj);
      labels.set(n.uid, obj);
    }

    const s: State = {
      renderer, labelRenderer, scene, camera, composer, controls, nodesMesh, edgesLine, edgesGeom,
      simNodes, edgeUids, nodeIndex, labels, sim, heads,
      raycaster: new THREE.Raycaster(), pointer: new THREE.Vector2(),
      hoverUid: null, palette: areas, bg, accent, raf: 0, disposed: false, camTween: null,
      width, height, reduced, dummy: new THREE.Object3D(), downX: 0, downY: 0,
      lastPointer: performance.now(),
    };
    s.raycaster.params.Line = { threshold: 5 };
    st.current = s;

    applyHighlight(s, propsRef.current);
    syncPositions(s, propsRef.current, performance.now());
    fitCamera(s);

    // loop
    const animate = (now: number) => {
      if (s.disposed) return;
      if (s.sim.alpha() > 0.004) s.sim.tick();
      syncPositions(s, propsRef.current, now);
      stepCamTween(s, now);
      const p = propsRef.current;
      const busy = !!(p.selectedUid || p.highlightUids || p.highlightAreas || s.camTween || s.hoverUid);
      s.controls.autoRotate = !s.reduced && !busy && (now - s.lastPointer > 3500);
      s.controls.update();
      const __d = document.getElementById('ikm-dbg3d');
      if (__d) __d.textContent = JSON.stringify({ cam: s.camera.position.toArray().map((v: number) => Math.round(v)), tgt: s.controls.target.toArray().map((v: number) => Math.round(v)), ns: s.simNodes.map((n) => [n.title, Math.round(n.x), Math.round(n.y), Math.round(n.z)]) });
      s.composer.render();
      s.labelRenderer.render(s.scene, s.camera);
      s.raf = requestAnimationFrame(animate);
    };
    s.raf = requestAnimationFrame(animate);

    // interacción
    const setPointer = (e: PointerEvent) => {
      const rect = renderer.domElement.getBoundingClientRect();
      s.pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      s.pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    };
    const pickNode = (): string | null => {
      s.raycaster.setFromCamera(s.pointer, s.camera);
      const hits = s.raycaster.intersectObject(s.nodesMesh);
      if (hits.length && hits[0].instanceId !== undefined) return s.simNodes[hits[0].instanceId].uid;
      return null;
    };
    const pickEdge = (): string | null => {
      s.raycaster.setFromCamera(s.pointer, s.camera);
      const hits = s.raycaster.intersectObject(s.edgesLine);
      if (hits.length && hits[0].index !== undefined) return s.edgeUids[Math.floor(hits[0].index / 2)] ?? null;
      return null;
    };
    const onMove = (e: PointerEvent) => {
      setPointer(e);
      const uid = pickNode();
      if (uid !== s.hoverUid) {
        s.hoverUid = uid;
        applyHighlight(s, propsRef.current);
        propsRef.current.onHover?.(uid);
        renderer.domElement.style.cursor = uid ? 'pointer' : 'grab';
      }
    };
    const onDown = (e: PointerEvent) => { s.downX = e.clientX; s.downY = e.clientY; s.lastPointer = performance.now(); };
    const onUp = (e: PointerEvent) => {
      if (Math.hypot(e.clientX - s.downX, e.clientY - s.downY) > 6) return; // fue drag
      setPointer(e);
      const uid = pickNode();
      if (uid) { propsRef.current.onSelect?.(uid); return; }
      const edge = pickEdge();
      if (edge) { propsRef.current.onEdgeSelect?.(edge); return; }
      propsRef.current.onSelect?.(null);
    };
    renderer.domElement.addEventListener('pointermove', onMove);
    renderer.domElement.addEventListener('pointerdown', onDown);
    renderer.domElement.addEventListener('pointerup', onUp);
    const onWheel = () => { s.lastPointer = performance.now(); };
    renderer.domElement.addEventListener('wheel', onWheel, { passive: true });

    // resize
    const ro = new ResizeObserver(() => {
      const w = mount.clientWidth, h = mount.clientHeight;
      if (!w || !h) return;
      s.width = w; s.height = h;
      s.camera.aspect = w / h;
      s.camera.updateProjectionMatrix();
      s.renderer.setSize(w, h);
      s.composer.setSize(w, h);
      s.labelRenderer.setSize(w, h);
    });
    ro.observe(mount);

    // tema
    const refreshTheme = () => {
      const pal = resolvePalette(propsRef.current.nodes);
      s.palette = pal.areas; s.bg = pal.bg; s.accent = pal.accent;
      s.scene.background = pal.bg;
      if (s.scene.fog) (s.scene.fog as THREE.FogExp2).color.copy(pal.bg);
      applyHighlight(s, propsRef.current);
    };
    const mo = new MutationObserver(refreshTheme);
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });

    return () => {
      s.disposed = true;
      cancelAnimationFrame(s.raf);
      s.sim.stop();
      ro.disconnect();
      mo.disconnect();
      renderer.domElement.removeEventListener('pointermove', onMove);
      renderer.domElement.removeEventListener('pointerdown', onDown);
      renderer.domElement.removeEventListener('pointerup', onUp);
      renderer.domElement.removeEventListener('wheel', onWheel);
      controls.dispose();
      sphere.dispose(); nodeMat.dispose(); edgesGeom.dispose(); edgeMat.dispose();
      for (const [, label] of s.labels) { scene.remove(label); (label.element as HTMLElement).remove(); }
      composer.dispose();
      renderer.dispose();
      renderer.domElement.remove();
      labelRenderer.domElement.remove();
      st.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [props.nodes, props.edges, props.obsidian]);

  useEffect(() => {
    if (st.current) applyHighlight(st.current, propsRef.current);
  }, [props.selectedUid, props.highlightUids, props.highlightEdgeUids, props.highlightAreas, props.areaFilter, props.obsidian, props.monoColor, props.areaColors]);

  useEffect(() => {
    if (st.current && props.focusUid) focusNode(st.current, props.focusUid);
  }, [props.focusUid]);

  useEffect(() => {
    if (st.current && props.fitSignal) fitCamera(st.current);
  }, [props.fitSignal]);

  // Modo camino: encuadrar los nodos de la ruta para que la cadena se vea.
  useEffect(() => {
    if (st.current && props.highlightUids && props.highlightUids.size > 0) {
      const uids = [...props.highlightUids];
      const t = setTimeout(() => { if (st.current) frameNodes(st.current, uids); }, 700);
      return () => clearTimeout(t);
    }
  }, [props.highlightUids]);

  return (
    <div
      ref={mountRef}
      className={`relative overflow-hidden ${props.className ?? ''}`}
      role="application"
      aria-label="Grafo 3D de conceptos. Arrastrá para rotar, rueda para zoom, click para seleccionar. La lista de conceptos ofrece navegación por teclado."
    >
      <div id="ikm-dbg3d" style={{ position: 'absolute', left: 4, top: 4, zIndex: 60, fontSize: 9, fontFamily: 'monospace', background: 'rgba(0,0,0,.85)', color: '#0f0', padding: 4, maxWidth: 380, whiteSpace: 'pre', pointerEvents: 'none' }} />
    </div>
  );
}