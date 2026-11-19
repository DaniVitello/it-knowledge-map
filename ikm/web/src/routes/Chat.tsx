/** /chat — cliente de chat (Capa 20b) + puente chat↔grafo (spec §8.7).
 * Estados explícitos: disponible / degradado / no-disponible. Procedencia visible.
 * Cada consulta enlaza entidades del release y activa el grafo en vivo:
 * "relación entre Frontend y Backend" resalta esas conexiones; "HTTP y DNS"
 * traza el camino; un concepto abre su vecindad. La intención se resuelve en el
 * cliente contra datos documentados (funciona aunque el backend sea stub).
 */
import { lazy, Suspense, useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { AlertTriangle, MessageSquare, Network, Send, WifiOff, X } from 'lucide-react';
import {
  probeChatAvailability, sendChat, ChatApiError,
  type ChatAvailability, type ChatTurn,
} from '../lib/api';
import { ProvenanceBadge, Spinner } from '../components/ui';
import { useRecordView } from '../lib/useExploration';
import { useRelease } from '../lib/release';
import { buildAdjacency, edgesAlongPath, neighborsOf, shortestPath } from '../lib/graph';
import { linkEntities, deriveAction, actionToUrl, actionVerb, type GraphAction } from '../lib/chatBridge';

const Graph3D = lazy(() => import('../components/Graph3D'));

const SUGGESTIONS = [
  '¿Cómo se relacionan Frontend y Backend?',
  'Camino entre HTTP y DNS',
  'Explorá AI / ML Fundamentals',
];

function AvailabilityChip({ state, onRetry }: { state: ChatAvailability; onRetry: () => void }) {
  if (state === 'comprobando') {
    return <span className="chip bg-raised/80 text-muted border border-line/50"><Spinner className="h-3 w-3" /> Comprobando backend…</span>;
  }
  if (state === 'disponible') {
    return <span className="chip bg-emerald-400/15 text-emerald-600 dark:text-emerald-300 border border-emerald-400/30">● Chat disponible</span>;
  }
  if (state === 'degradado') {
    return (
      <span className="chip bg-amber-400/15 text-amber-600 dark:text-amber-300 border border-amber-400/30">
        <AlertTriangle className="h-3 w-3" aria-hidden /> Chat degradado (backend en desarrollo)
      </span>
    );
  }
  return (
    <button className="chip bg-raised/80 text-muted border border-line/50 hover:text-ink" onClick={onRetry}>
      <WifiOff className="h-3 w-3" aria-hidden /> Chat no disponible · reintentar
    </button>
  );
}

export default function Chat() {
  const { graph, bootstrap, areas } = useRelease();
  const navigate = useNavigate();
  const [availability, setAvailability] = useState<ChatAvailability>('comprobando');
  const [turns, setTurns] = useState<ChatTurn[]>([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [action, setAction] = useState<GraphAction | null>(null);
  const [showGraph, setShowGraph] = useState(true);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useRecordView(null, '');

  const adj = useMemo(() => buildAdjacency(graph), [graph]);

  // Acción de grafo derivada de la última consulta (entidades documentadas).
  const graphView = useMemo(() => {
    if (!action) return { highlightUids: null as Set<string> | null, highlightEdgeUids: null as Set<string> | null, highlightAreas: null as Set<string> | null, focusUid: null as string | null };
    switch (action.kind) {
      case 'path': {
        const path = shortestPath(adj, action.from, action.to);
        if (!path) return { highlightUids: new Set([action.from, action.to]), highlightEdgeUids: null, highlightAreas: null, focusUid: action.from };
        return { highlightUids: new Set(path), highlightEdgeUids: new Set(edgesAlongPath(graph, path).map((e) => e.uid)), highlightAreas: null, focusUid: null };
      }
      case 'areas':
        return { highlightUids: null, highlightEdgeUids: null, highlightAreas: new Set(action.areas), focusUid: null };
      case 'neighborhood': {
        const nbs = neighborsOf(adj, action.uid).map((n) => n.uid);
        return { highlightUids: new Set([action.uid, ...nbs]), highlightEdgeUids: null, highlightAreas: null, focusUid: action.uid };
      }
      case 'area':
        return { highlightUids: null, highlightEdgeUids: null, highlightAreas: new Set([action.area]), focusUid: null };
    }
  }, [action, adj, graph]);

  const probe = () => {
    setAvailability('comprobando');
    probeChatAvailability().then(setAvailability);
  };

  useEffect(() => {
    probe();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, [turns, sending]);

  const submit = async (text: string) => {
    const message = text.trim();
    if (!message || sending) return;
    // Puente chat↔grafo: enlazar entidades y activar el grafo (incluso si el
    // backend no está, la exploración visual funciona con datos del release).
    const ent = linkEntities(message, bootstrap.concepts, areas);
    const act = deriveAction(message, ent);
    if (act) { setAction(act); setShowGraph(true); }

    if (availability === 'no-disponible') {
      setError('El backend de chat no está corriendo. Igual podés explorar el grafo activado abajo.');
      return;
    }
    setError(null);
    setInput('');
    const nextTurns: ChatTurn[] = [...turns, { role: 'user', text: message }];
    setTurns(nextTurns);
    setSending(true);
    try {
      const reply = await sendChat(message, turns);
      setTurns([...nextTurns, {
        role: 'assistant', text: reply.text || '(respuesta vacía)',
        provenance: reply.provenance, degraded: reply.degraded, note: reply.note,
      }]);
    } catch (e) {
      const msg = e instanceof ChatApiError ? e.message : 'No se pudo contactar al backend de chat.';
      setError(msg);
      if (e instanceof ChatApiError && e.code === 'red') setAvailability('no-disponible');
    } finally {
      setSending(false);
      inputRef.current?.focus();
    }
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      void submit(input);
    }
  };

  return (
    <div className="h-[calc(100vh-3.5rem)] flex flex-col">
      <header className="px-4 sm:px-6 py-3 border-b border-line/50 flex items-center gap-3 flex-wrap shrink-0">
        <h1 className="text-lg font-bold inline-flex items-center gap-2">
          <MessageSquare className="h-5 w-5 text-accent" aria-hidden /> Chat
        </h1>
        <AvailabilityChip state={availability} onRetry={probe} />
        <button
          className={`btn-ghost !py-1.5 !text-xs ml-auto hidden lg:inline-flex ${showGraph ? '!border-accent/50 !text-accent' : ''}`}
          onClick={() => setShowGraph((s) => !s)}
          aria-pressed={showGraph}
        >
          <Network className="h-3.5 w-3.5" aria-hidden /> {showGraph ? 'Ocultar grafo' : 'Mostrar grafo'}
        </button>
      </header>

      <div className="flex-1 flex min-h-0">
        {/* Columna de chat */}
        <div className="flex flex-col min-h-0 w-full lg:w-[400px] lg:shrink-0 lg:border-r border-line/50">
          <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4" aria-live="polite" aria-label="Conversación">
            {turns.length === 0 && (
              <div className="space-y-2">
                <p className="text-xs text-faint uppercase tracking-wide font-semibold">Probá preguntando</p>
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    className="panel block w-full text-left px-4 py-3 text-sm text-muted hover:text-ink hover:border-line transition-colors"
                    onClick={() => void submit(s)}
                  >
                    {s}
                  </button>
                ))}
                <p className="text-[11px] text-faint pt-1">
                  El chat activa el grafo: nombrá conceptos o áreas y mirá cómo se resaltan sus conexiones.
                </p>
              </div>
            )}

            <AnimatePresence initial={false}>
              {turns.map((t, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.22 }}
                  className={`flex ${t.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap ${
                    t.role === 'user' ? 'bg-accent text-white rounded-br-md' : 'panel rounded-bl-md'
                  }`}>
                    {t.text}
                    {t.role === 'assistant' && (
                      <div className="mt-2.5 flex flex-wrap gap-1.5 items-center">
                        {(t.provenance ?? []).map((p, j) => <ProvenanceBadge key={j} kind={p.kind} />)}
                        {t.degraded && (
                          <span className="chip bg-amber-400/15 text-amber-600 dark:text-amber-300 border border-amber-400/30">
                            <AlertTriangle className="h-3 w-3" aria-hidden /> degradado
                          </span>
                        )}
                      </div>
                    )}
                    {t.note && <p className="mt-2 text-[11px] text-faint">{t.note}</p>}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>

            {sending && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                <div className="panel rounded-2xl rounded-bl-md px-4 py-3 inline-flex items-center gap-2 text-sm text-muted">
                  <Spinner className="h-4 w-4" /> Pensando…
                </div>
              </motion.div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Banner de acción de grafo */}
          <AnimatePresence>
            {action && (
              <motion.div
                initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                className="mx-4 mb-2 panel px-3.5 py-2.5 flex items-center gap-2.5 border-accent/30"
              >
                <Network className="h-4 w-4 text-accent shrink-0" aria-hidden />
                <span className="text-xs flex-1 min-w-0">
                  <span className="text-faint">{actionVerb(action)} </span>
                  <span className="font-medium text-ink">{action.label}</span>
                </span>
                <button className="btn-primary !py-1 !px-2.5 !text-[11px] shrink-0" onClick={() => navigate(actionToUrl(action))}>
                  Abrir
                </button>
                <button className="btn-ghost !p-1 shrink-0" onClick={() => setAction(null)} aria-label="Quitar acción">
                  <X className="h-3 w-3" />
                </button>
              </motion.div>
            )}
          </AnimatePresence>

          {error && (
            <p role="alert" className="mx-4 mb-2 text-xs text-amber-600 dark:text-amber-300 bg-amber-400/10 border border-amber-400/30 rounded-lg px-3 py-2">
              {error}
            </p>
          )}

          <form className="px-4 pb-3 shrink-0" onSubmit={(e) => { e.preventDefault(); void submit(input); }}>
            <div className="panel flex items-end gap-2 p-2.5">
              <textarea
                ref={inputRef}
                rows={1}
                className="flex-1 bg-transparent resize-none outline-none text-sm px-2 py-1.5 max-h-32 placeholder:text-faint"
                placeholder="Escribí tu pregunta… (Enter envía)"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={onKeyDown}
                aria-label="Mensaje para el chat"
                disabled={sending}
              />
              <button
                type="submit"
                className="btn-primary !p-2.5 shrink-0 disabled:opacity-40 disabled:cursor-not-allowed"
                disabled={sending || !input.trim()}
                aria-label="Enviar mensaje"
              >
                <Send className="h-4 w-4" />
              </button>
            </div>
          </form>
        </div>

        {/* Panel de grafo en vivo (desktop) */}
        {showGraph && (
          <div className="hidden lg:flex flex-1 min-w-0 relative flex-col">
            <Suspense fallback={
              <div className="flex-1 bg-base flex items-center justify-center text-sm text-muted">
                <span className="inline-block h-5 w-5 rounded-full border-2 border-line border-t-accent animate-spin mr-2.5" />
                Cargando grafo 3D…
              </div>
            }>
              <Graph3D
                className="flex-1 bg-base"
                nodes={graph.nodes}
                edges={graph.edges}
                highlightUids={graphView.highlightUids}
                highlightEdgeUids={graphView.highlightEdgeUids}
                highlightAreas={graphView.highlightAreas}
                focusUid={graphView.focusUid}
                onSelect={(uid) => uid && navigate(`/graph/view/${uid}`)}
              />
            </Suspense>
            <div className="absolute left-3 top-3 panel px-3 py-1.5 text-[11px] text-muted max-w-[70%]">
              {action
                ? <span><span className="text-accent font-medium">{action.label}</span> · click en un nodo para abrir su vecindad</span>
                : <span>Nombrá conceptos o áreas en el chat para activar sus conexiones</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}