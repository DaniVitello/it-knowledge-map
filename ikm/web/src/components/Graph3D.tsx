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
import { areaCentroids, initialPositions, type SimNode } from '../lib/forceLayout';

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
    const base = s.palette.get(n.area_uid ?? '') ?? s.accent;
    const f = nodeVisible(n);
    c.copy(base).multiplyScalar(f);
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
    let f = 0.28;
    if (isHl) f = 1.3;
    if (dimArea || dimPath) f = 0.04;
    else if (anchor && !isHl) f = 0.06;
    const col = isHl ? s.accent : (s.palette.get(a.area_uid ?? '') ?? s.accent);
    ec.copy(col).multiplyScalar(f);
    posAttr.setXYZ(i * 2, ec.r, ec.g, ec.b);
    posAttr.setXYZ(i * 2 + 1, ec.r, ec.g, ec.b);
  }
  posAttr.needsUpdate = true;

  // labels: hover, selección, vecinos, camino
  const show = new Set<string>(neighborSet);
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

    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    mount.appendChild(renderer.domElement);

    const labelRenderer = new CSS2DRenderer();
    labelRenderer.setSize(width, height);
    labelRenderer.domElement.style.position = 'absolute';
    labelRenderer.domElement.style.top = '0';
    labelRenderer.domElement.style.left = '0';
    labelRenderer.domElement.style.pointerEvents = 'none';
    mount.appendChild(labelRenderer.domElement);

    const composer = new EffectComposer(renderer);
    composer.addPass(new RenderPass(scene, camera));
    const bloom = new UnrealBloomPass(new THREE.Vector2(width, height), 0.9, 0.55, 0.18);
    composer.addPass(bloom);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.rotateSpeed = 0.6;
    controls.minDistance = 120;
    controls.maxDistance = 3200;
    controls.autoRotateSpeed = 0.45;

    // nodos instanciados
    const sphere = new THREE.SphereGeometry(1, 18, 18);
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

    // simulación
    const areaUids = [...new Set(props.nodes.map((n) => n.area_uid).filter(Boolean))] as string[];
    const centroids = areaCentroids(areaUids);
    const simNodes = initialPositions(props.nodes, centroids);
    const nodeIndex = new Map(simNodes.map((n, i) => [n.uid, i]));
    const simLinks = props.edges.map((e) => ({ source: e.source, target: e.target, uid: e.uid }));
    const edgeUids = props.edges.map((e) => e.uid);
    const sim = forceSimulation(simNodes as any, 3)
      .force('link', forceLink(simLinks as any).id((d: any) => d.uid).distance(75).strength(0.22))
      .force('charge', forceManyBody().strength(-45))
      .force('collide', forceCollide().radius((d: any) => d.radius + 3).strength(0.7))
      .force('x', forceX((d: any) => centroids.get(d.area_uid ?? '')?.x ?? 0).strength(0.055))
      .force('y', forceY((d: any) => centroids.get(d.area_uid ?? '')?.y ?? 0).strength(0.055))
      .force('z', forceZ((d: any) => centroids.get(d.area_uid ?? '')?.z ?? 0).strength(0.055))
      .alpha(1).alphaDecay(0.022).velocityDecay(0.35);

    // labels
    const labels = new Map<string, CSS2DObject>();
    for (const n of simNodes) {
      const div = document.createElement('div');
      div.className = 'graph3d-label';
      div.textContent = n.title;
      div.style.opacity = '0';
      const obj = new CSS2DObject(div);
      obj.position.set(n.x, n.y, n.z);
      scene.add(obj);
      labels.set(n.uid, obj);
    }

    const s: State = {
      renderer, labelRenderer, scene, camera, composer, controls, nodesMesh, edgesLine, edgesGeom,
      simNodes, edgeUids, nodeIndex, labels, sim,
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
  }, [props.nodes, props.edges]);

  useEffect(() => {
    if (st.current) applyHighlight(st.current, propsRef.current);
  }, [props.selectedUid, props.highlightUids, props.highlightEdgeUids, props.highlightAreas, props.areaFilter]);

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
    />
  );
}