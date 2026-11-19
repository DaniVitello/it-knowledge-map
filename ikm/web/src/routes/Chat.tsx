/** /chat — cliente de chat (Capa 20b, Entrega 3).
 * Estados explícitos: disponible / degradado / no-disponible.
 * Procedencia visible por respuesta; nunca se muestra output sin verificar
 * como si fuera documentado. Sin backend, el sitio sigue siendo navegable.
 */
import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { AlertTriangle, MessageSquare, RefreshCw, Send, WifiOff } from 'lucide-react';
import {
  probeChatAvailability, sendChat, ChatApiError,
  type ChatAvailability, type ChatTurn,
} from '../lib/api';
import { ProvenanceBadge, Spinner } from '../components/ui';
import { useRecordView } from '../lib/useExploration';

const SUGGESTIONS = [
  '¿Qué es HTTP y cómo se relaciona con DNS?',
  'Explicame la diferencia entre frontend y backend',
  '¿Qué conceptos debería estudiar primero para AI Engineering?',
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
  const [availability, setAvailability] = useState<ChatAvailability>('comprobando');
  const [turns, setTurns] = useState<ChatTurn[]>([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useRecordView(null, '');

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
    if (availability === 'no-disponible') {
      setError('El backend de chat no está corriendo. Levantalo con: py -m uvicorn ikm.api.main:app --port 8000');
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
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8 flex flex-col min-h-[calc(100vh-9.5rem)] lg:min-h-[calc(100vh-7rem)]">
      <header className="mb-5">
        <div className="flex items-center gap-3 flex-wrap mb-1.5">
          <h1 className="text-2xl font-bold inline-flex items-center gap-2">
            <MessageSquare className="h-6 w-6 text-accent" aria-hidden /> Chat
          </h1>
          <AvailabilityChip state={availability} onRetry={probe} />
        </div>
        <p className="text-sm text-muted leading-relaxed">
          Preguntá sobre los conceptos del mapa. Cada respuesta muestra su procedencia:
          <strong className="text-ink"> documentado</strong> (citado del release),
          <strong className="text-ink"> general</strong> (conocimiento del modelo) o
          <strong className="text-ink"> inferencia</strong>. El chat es una vía adicional:
          el sitio completo funciona sin backend.
        </p>
      </header>

      {availability === 'no-disponible' && turns.length === 0 && (
        <div className="panel p-6 text-center mb-5">
          <WifiOff className="h-8 w-8 text-faint mx-auto mb-3" aria-hidden />
          <h2 className="font-semibold mb-1.5">El backend de chat no está disponible</h2>
          <p className="text-sm text-muted mb-4">
            Mientras tanto, podés explorar el mapa completo sin conexión al servidor.
          </p>
          <div className="flex justify-center gap-2 flex-wrap">
            <Link to="/graph" className="btn-primary">Explorar el grafo</Link>
            <Link to="/kb" className="btn-ghost">Knowledge Base</Link>
            <button className="btn-ghost" onClick={probe}><RefreshCw className="h-4 w-4" /> Reintentar</button>
          </div>
        </div>
      )}

      {/* Mensajes */}
      <div className="flex-1 space-y-4 mb-5" aria-live="polite" aria-label="Conversación">
        {turns.length === 0 && availability !== 'no-disponible' && (
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
                t.role === 'user'
                  ? 'bg-accent text-white rounded-br-md'
                  : 'panel rounded-bl-md'
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

      {error && (
        <p role="alert" className="mb-3 text-sm text-amber-600 dark:text-amber-300 bg-amber-400/10 border border-amber-400/30 rounded-lg px-3.5 py-2.5">
          {error}
        </p>
      )}

      {/* Entrada */}
      <form
        className="panel flex items-end gap-2 p-2.5"
        onSubmit={(e) => { e.preventDefault(); void submit(input); }}
      >
        <textarea
          ref={inputRef}
          rows={1}
          className="flex-1 bg-transparent resize-none outline-none text-sm px-2 py-1.5 max-h-32 placeholder:text-faint"
          placeholder={availability === 'no-disponible' ? 'Chat no disponible — explorá el mapa mientras tanto' : 'Escribí tu pregunta… (Enter envía, Shift+Enter salto de línea)'}
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
      </form>
      <p className="mt-2 text-[11px] text-faint text-center">
        Las respuestas del modelo pueden contener errores: verificá contra las fichas del mapa.
      </p>
    </div>
  );
}