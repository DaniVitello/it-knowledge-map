/** Contexto de exploración: historial versionado en IndexedDB (§15.4).
 * record() es idempotente para vistas consecutivas idénticas.
 */
import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import {
  appendView, emptyState, loadExploration, pruneUnknown, saveExploration, clearExploration,
  type ExplorationState, type ExplorationView, type ExplorationEntry,
} from './exploration';
import { useRelease } from './release';

interface ExplorationCtx {
  state: ExplorationState;
  recent: ExplorationEntry[];
  record: (view: ExplorationView, label: string) => void;
  clear: () => void;
  prunedNotice: number;
}

const Ctx = createContext<ExplorationCtx | null>(null);

export function ExplorationProvider({ children }: { children: ReactNode }) {
  const { bootstrap, areas } = useRelease();
  const [state, setState] = useState<ExplorationState>(emptyState);
  const [prunedNotice, setPrunedNotice] = useState(0);
  const loaded = useRef(false);

  useEffect(() => {
    let alive = true;
    loadExploration().then((raw) => {
      if (!alive) return;
      const knownUids = new Set(bootstrap.concepts.map((c) => c.uid));
      const knownAreas = new Set(areas.map((a) => a.uid));
      const { state: pruned, removed } = pruneUnknown(raw, knownUids, knownAreas);
      setState(pruned);
      if (removed > 0) {
        setPrunedNotice(removed);
        void saveExploration(pruned);
      }
      loaded.current = true;
    });
    return () => { alive = false; };
  }, [bootstrap, areas]);

  const record = useCallback((view: ExplorationView, label: string) => {
    setState((prev) => {
      const next = appendView(prev, view, label);
      if (next !== prev) void saveExploration(next);
      return next;
    });
  }, []);

  const clear = useCallback(() => {
    setState(emptyState());
    void clearExploration();
  }, []);

  const value = useMemo<ExplorationCtx>(() => ({
    state,
    recent: [...state.history].reverse().slice(0, 8),
    record,
    clear,
    prunedNotice,
  }), [state, record, clear, prunedNotice]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useExploration(): ExplorationCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('useExploration requiere <ExplorationProvider>');
  return ctx;
}

/** Registra una vista al montar/cambiar el foco (una vez por combinación). */
export function useRecordView(view: ExplorationView | null, label: string) {
  const { record } = useExploration();
  const key = view ? JSON.stringify(view) : '';
  useEffect(() => {
    if (view && label) record(view, label);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key, label]);
}