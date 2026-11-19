/** /graph y /graph/view/:uid — grafo completo y vista contextual.
 * Filtros por área, modo camino (BFS), panel de relaciones quoted,
 * lista de conceptos para navegación por teclado (§15.5).
 * Vistas simples codificadas en la URL: ?focus= &area= &from= &to= (§15.2).
 */
import { lazy, Suspense, useEffect, useMemo, useState } from 'react';
import { Link, useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { ArrowLeft, Box, GitBranch, Maximize, Network, Square, X } from 'lucide-react';
import { useRelease, useRelations } from '../lib/release';
import { buildAdjacency, edgesAlongPath, neighborsOf, shortestPath, subgraphAround } from '../lib/graph';
import GraphCanvas from '../components/GraphCanvas';
const Graph3D = lazy(() => import('../components/Graph3D'));
import RelationCard from '../components/RelationCard';
import { AreaBadge } from '../components/ui';
import { areaColor } from '../lib/format';
import { normalizeText } from '../lib/search';
import { useRecordView } from '../lib/useExploration';
import type { ConceptIndexEntry } from '../lib/types';

function ConceptSelect({ value, onChange, concepts, areas, label }: {
  value: string;
  onChange: (uid: string) => void;
  concepts: ConceptIndexEntry[];
  areas: { uid: string; name: string }[];
  label: string;
}) {
  return (
    <select
      className="input !py-1.5 !text-xs max-w-[180px]"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      aria-label={label}
    >
      <option value="">Elegí un concepto…</option>
      {areas.map((a) => (
        <optgroup key={a.uid} label={a.name}>
          {concepts.filter((c) => c.area_uid === a.uid).map((c) => (
            <option key={c.uid} value={c.uid}>{c.title}</option>
          ))}
        </optgroup>
      ))}
    </select>
  );
}

export default function GraphPage() {
  const { uid: contextUid } = useParams();
  const [params, setParams] = useSearchParams();
  const navigate = useNavigate();
  const { graph, byUid, areas, bootstrap } = useRelease();
  const { data: relations } = useRelations(true);

  const adj = useMemo(() => buildAdjacency(graph), [graph]);
  const contextual = Boolean(contextUid && byUid.has(contextUid));
  const areaFilter = params.get('area');
  const from = params.get('from') ?? '';
  const to = params.get('to') ?? '';
  const focusParam = params.get('focus');
  const viewMode = params.get('view') === '2d' ? '2d' : '3d';
  const areasParam = params.get('areas');
  const highlightAreas = useMemo(() => areasParam ? new Set(areasParam.split(',').filter(Boolean)) : null, [areasParam]);

  const [selected, setSelected] = useState<string | null>(contextUid ?? focusParam);
  const [selectedEdge, setSelectedEdge] = useState<string | null>(null);
  const [pathMode, setPathMode] = useState(Boolean(from && to));
  const [centerRequest, setCenterRequest] = useState<string | null>(null);
  const [fitSignal, setFitSignal] = useState(0);
  const [listFilter, setListFilter] = useState('');

  const view = useMemo(
    () => (contextual ? subgraphAround(graph, adj, contextUid!, 1) : graph),
    [contextual, contextUid, graph, adj],
  );

  const path = useMemo(
    () => (from && to ? shortestPath(adj, from, to) : null),
    [adj, from, to],
  );
  const pathEdgeUids = useMemo(
    () => (path ? new Set(edgesAlongPath(graph, path).map((e) => e.uid)) : null),
    [path, graph],
  );
  const pathUids = useMemo(() => (path ? new Set(path) : null), [path]);

  const selectedRelations = useMemo(() => {
    if (!relations || !selected) return [];
    return relations.filter((r) => r.source_uid === selected || r.target_uid === selected);
  }, [relations, selected]);

  const selectedEdgeRecord = useMemo(
    () => (relations && selectedEdge ? relations.find((r) => r.uid === selectedEdge) ?? null : null),
    [relations, selectedEdge],
  );

  const listConcepts = useMemo(() => {
    const q = normalizeText(listFilter);
    const all = view.nodes
      .map((n) => byUid.get(n.uid))
      .filter((c): c is ConceptIndexEntry => Boolean(c))
      .sort((a, b) => a.title.localeCompare(b.title));
    return q ? all.filter((c) => normalizeText(c.title).includes(q)) : all;
  }, [view, byUid, listFilter]);

  const label = contextual
    ? byUid.get(contextUid!)?.title ?? 'Grafo'
    : path
      ? `Camino: ${byUid.get(from)?.title ?? from} → ${byUid.get(to)?.title ?? to}`
      : 'Grafo completo';

  useRecordView(
    contextual
      ? { type: 'graph', uid: contextUid!, origin: 'manual' }
      : path
        ? { type: 'path', uid: from, target: to, origin: 'manual' }
        : { type: 'graph', origin: 'manual' },
    label,
  );

  // Sincronizar selección con la URL en modo completo.
  const selectNode = (uid: string | null, center = false) => {
    setSelected(uid);
    setSelectedEdge(null);
    if (center && uid) setCenterRequest(uid);
    if (!contextual) {
      const p = new URLSearchParams(params);
      if (uid) p.set('focus', uid);
      else p.delete('focus');
      setParams(p, { replace: true });
    }
  };

  const setParam = (key: string, value: string | null) => {
    const p = new URLSearchParams(params);
    if (value) p.set(key, value);
    else p.delete(key);
    setParams(p, { replace: true });
  };

  useEffect(() => {
    if (contextUid) setSelected(contextUid);
  }, [contextUid]);

  const panelOpen = Boolean(selected || selectedEdgeRecord || path);
  const selectedEntry = selected ? byUid.get(selected) : undefined;
  const selectedNode = view.nodes.find((n) => n.uid === selected) ?? graph.nodes.find((n) => n.uid === selected);

  return (
    <div className="h-[calc(100vh-3.5rem)] flex flex-col">
      {/* Toolbar */}
      <div className="flex items-center gap-2 px-3 h-12 border-b border-line/50 bg-surface/60 flex-wrap shrink-0">
        {contextual ? (
          <>
            <button className="btn-ghost !p-1.5" onClick={() => navigate('/graph')} aria-label="Volver al grafo completo">
              <ArrowLeft className="h-4 w-4" />
            </button>
            <h1 className="text-sm font-semibold truncate">
              Vecindad de <span className="text-accent">{byUid.get(contextUid!)?.title}</span>
            </h1>
          </>
        ) : (
          <h1 className="text-sm font-semibold inline-flex items-center gap-1.5">
            <Network className="h-4 w-4 text-accent" aria-hidden />
            {path ? 'Camino entre conceptos' : 'Grafo completo'}
            <span className="text-faint font-normal hidden sm:inline">· {view.nodes.length} nodos · {view.edges.length} relaciones</span>
          </h1>
        )}

        <div className="ml-auto flex items-center gap-2 flex-wrap">
          {!contextual && (
            <select
              className="input !py-1.5 !text-xs !w-auto"
              value={areaFilter ?? ''}
              onChange={(e) => setParam('area', e.target.value || null)}
              aria-label="Filtrar por área"
            >
              <option value="">Todas las áreas</option>
              {areas.map((a) => <option key={a.uid} value={a.uid}>{a.name}</option>)}
            </select>
          )}
          <button
            className={`btn-ghost !py-1.5 !text-xs ${pathMode ? '!border-accent/50 !text-accent' : ''}`}
            onClick={() => {
              setPathMode((m) => !m);
              if (pathMode) { setParam('from', null); setParam('to', null); }
            }}
            aria-pressed={pathMode}
          >
            <GitBranch className="h-3.5 w-3.5" aria-hidden /> Camino
          </button>
          <button
            className="btn-ghost !py-1.5 !text-xs"
            onClick={() => setParam('view', viewMode === '3d' ? '2d' : null)}
            aria-pressed={viewMode === '3d'}
            title={viewMode === '3d' ? 'Cambiar a vista 2D' : 'Cambiar a vista 3D'}
          >
            {viewMode === '3d' ? <Square className="h-3.5 w-3.5" aria-hidden /> : <Box className="h-3.5 w-3.5" aria-hidden />}
            {viewMode === '3d' ? '2D' : '3D'}
          </button>
          <button className="btn-ghost !py-1.5 !text-xs" onClick={() => setFitSignal((s) => s + 1)}>
            <Maximize className="h-3.5 w-3.5" aria-hidden /> Encuadrar
          </button>
        </div>
      </div>

      {/* Selector de camino */}
      {pathMode && !contextual && (
        <div className="flex items-center gap-2 px-3 py-2 border-b border-line/50 bg-raised/30 flex-wrap shrink-0">
          <ConceptSelect value={from} onChange={(v) => setParam('from', v || null)} concepts={bootstrap.concepts} areas={areas} label="Concepto origen" />
          <span className="text-faint text-xs" aria-hidden>→</span>
          <ConceptSelect value={to} onChange={(v) => setParam('to', v || null)} concepts={bootstrap.concepts} areas={areas} label="Concepto destino" />
          {from && to && (
            <span className="text-xs text-muted" role="status">
              {path ? `${path.length - 1} saltos` : 'No hay camino entre estos conceptos'}
            </span>
          )}
        </div>
      )}

      <div className="flex-1 flex min-h-0 relative">
        {/* Grafo 3D (default) o 2D (toggle) */}
        {viewMode === '3d' ? (
          <Suspense fallback={
            <div className="flex-1 bg-base flex items-center justify-center text-sm text-muted">
              <span className="inline-block h-5 w-5 rounded-full border-2 border-line border-t-accent animate-spin mr-2.5" />
              Cargando grafo 3D…
            </div>
          }>
            <Graph3D
              className="flex-1 bg-base"
              nodes={view.nodes}
              edges={view.edges}
              selectedUid={selected}
              highlightUids={pathUids}
              highlightEdgeUids={pathEdgeUids}
              highlightAreas={highlightAreas}
              focusUid={contextual ? null : centerRequest}
              areaFilter={contextual ? null : areaFilter}
              fitSignal={fitSignal}
              onSelect={(uid) => selectNode(uid)}
              onEdgeSelect={(edgeUid) => { setSelectedEdge(edgeUid); setSelected(null); }}
            />
          </Suspense>
        ) : (
          <GraphCanvas
            className="flex-1 bg-base"
            nodes={view.nodes}
            edges={view.edges}
            selectedUid={selected}
            highlightUids={pathUids}
            highlightEdgeUids={pathEdgeUids}
            highlightAreas={highlightAreas}
            focusUid={contextual ? null : centerRequest}
            areaFilter={contextual ? null : areaFilter}
            fitSignal={fitSignal}
            onSelect={(uid) => selectNode(uid)}
            onEdgeSelect={(edgeUid) => { setSelectedEdge(edgeUid); setSelected(null); }}
          />
        )}

        {/* Leyenda de áreas */}
        {!contextual && (
          <div className="absolute left-3 bottom-3 panel px-3 py-2 flex flex-wrap gap-x-3 gap-y-1 max-w-[70%] text-[11px]">
            {areas.map((a) => (
              <button
                key={a.uid}
                className={`inline-flex items-center gap-1.5 hover:text-ink transition-colors ${areaFilter === a.uid ? 'text-ink font-semibold' : 'text-muted'}`}
                onClick={() => setParam('area', areaFilter === a.uid ? null : a.uid)}
                aria-pressed={areaFilter === a.uid}
              >
                <span aria-hidden className="h-2 w-2 rounded-full" style={{ backgroundColor: areaColor(a.uid) }} />
                {a.name}
              </button>
            ))}
          </div>
        )}

        {/* Panel lateral */}
        {panelOpen && (
          <aside
            className="w-80 shrink-0 border-l border-line/50 bg-surface/95 backdrop-blur overflow-y-auto max-lg:absolute max-lg:inset-y-0 max-lg:right-0 max-lg:z-20 max-lg:shadow-panel"
            aria-label="Detalle de la selección"
          >
            <div className="p-4 space-y-4">
              <div className="flex items-start justify-between gap-2">
                <h2 className="text-sm font-semibold text-faint uppercase tracking-wide">
                  {selectedEdgeRecord ? 'Relación' : path ? 'Camino' : 'Concepto'}
                </h2>
                <button
                  className="btn-ghost !p-1"
                  onClick={() => { setSelected(null); setSelectedEdge(null); if (path) { setParam('from', null); setParam('to', null); } }}
                  aria-label="Cerrar panel"
                >
                  <X className="h-3.5 w-3.5" />
                </button>
              </div>

              {selectedEdgeRecord && (
                <RelationCard relation={selectedEdgeRecord} />
              )}

              {selectedEntry && !selectedEdgeRecord && (
                <>
                  <div>
                    <Link
                      to={`/kb/c/${selectedEntry.uid}/${selectedEntry.slug}`}
                      className="text-lg font-bold hover:text-accent leading-tight block"
                    >
                      {selectedEntry.title}
                    </Link>
                    <div className="flex items-center gap-2 mt-1.5 flex-wrap">
                      <AreaBadge areaUid={selectedEntry.area_uid} />
                      <span className="text-xs text-faint">{selectedNode?.grado ?? 0} relaciones</span>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Link to={`/kb/c/${selectedEntry.uid}/${selectedEntry.slug}`} className="btn-primary !py-1.5 !text-xs flex-1">
                      Abrir ficha
                    </Link>
                    {!contextual && (
                      <Link to={`/graph/view/${selectedEntry.uid}`} className="btn-ghost !py-1.5 !text-xs flex-1">
                        Vecindad
                      </Link>
                    )}
                  </div>

                  <div>
                    <h3 className="text-xs font-semibold text-faint uppercase tracking-wide mb-2">
                      Relaciones ({selectedRelations.length})
                    </h3>
                    <div className="space-y-2.5">
                      {selectedRelations.map((r) => (
                        <RelationCard key={r.uid} relation={r} perspectiveUid={selectedEntry.uid} compact />
                      ))}
                    </div>
                  </div>

                  <div>
                    <h3 className="text-xs font-semibold text-faint uppercase tracking-wide mb-2">Vecinos (teclado)</h3>
                    <div className="flex flex-wrap gap-1.5">
                      {neighborsOf(adj, selectedEntry.uid).map((nb) => {
                        const e = byUid.get(nb.uid);
                        if (!e) return null;
                        return (
                          <button
                            key={nb.uid + nb.direction}
                            className="chip bg-raised/70 border border-line/50 text-muted hover:text-accent hover:border-accent/40"
                            onClick={() => selectNode(nb.uid, true)}
                          >
                            {e.title}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                </>
              )}

              {path && !selectedEntry && !selectedEdgeRecord && (
                <ol className="space-y-1.5" aria-label="Pasos del camino">
                  {path.map((uid, i) => {
                    const e = byUid.get(uid);
                    return (
                      <li key={uid} className="flex items-center gap-2">
                        <span className="text-[10px] text-faint tabular-nums w-4">{i + 1}</span>
                        <button
                          className="text-sm text-left hover:text-accent flex-1 truncate"
                          onClick={() => selectNode(uid, true)}
                        >
                          {e?.title ?? uid}
                        </button>
                        {e && <span aria-hidden className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: areaColor(e.area_uid) }} />}
                      </li>
                    );
                  })}
                </ol>
              )}
            </div>
          </aside>
        )}
      </div>

      {/* Lista accesible de conceptos (alternativa por teclado al canvas) */}
      <details className="border-t border-line/50 bg-surface/60 shrink-0">
        <summary className="px-4 py-2 text-xs text-muted cursor-pointer select-none hover:text-ink">
          Lista de conceptos ({listConcepts.length}) — navegación por teclado sin canvas
        </summary>
        <div className="px-4 pb-3">
          <input
            className="input !py-1.5 !text-xs max-w-xs mb-2"
            placeholder="Filtrar conceptos…"
            value={listFilter}
            onChange={(e) => setListFilter(e.target.value)}
            aria-label="Filtrar lista de conceptos"
          />
          <ul className="max-h-44 overflow-y-auto grid sm:grid-cols-2 lg:grid-cols-3 gap-x-4" aria-label="Conceptos del grafo">
            {listConcepts.map((c) => (
              <li key={c.uid}>
                <button
                  className={`w-full text-left text-xs py-1 px-1.5 rounded hover:bg-raised/70 truncate ${selected === c.uid ? 'text-accent font-semibold' : 'text-muted'}`}
                  onClick={() => selectNode(c.uid, true)}
                >
                  {c.title}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </details>
    </div>
  );
}