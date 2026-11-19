/** Paleta de comandos (Ctrl+K): búsqueda global de conceptos + áreas +
 * acciones + exploración reciente. Teclado primero: ↑↓ Enter Esc.
 */
import { useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { BookOpen, Clock, CornerDownLeft, MessageSquare, Network, Route, Search, Shield } from 'lucide-react';
import { useRelease, useClientIndex } from '../lib/release';
import { buildSearchIndex, search } from '../lib/search';
import { useExploration } from '../lib/useExploration';
import { areaColor } from '../lib/format';
import type { ExplorationEntry } from '../lib/exploration';

interface Item {
  key: string;
  kind: 'concept' | 'area' | 'action' | 'recent';
  title: string;
  subtitle?: string;
  areaUid?: string | null;
  to: string;
}

const ACTIONS: Item[] = [
  { key: 'a-graph', kind: 'action', title: 'Ir al grafo completo', subtitle: '255 nodos · 913 relaciones', to: '/graph' },
  { key: 'a-kb', kind: 'action', title: 'Explorar Knowledge Base', subtitle: 'Conceptos por área', to: '/kb' },
  { key: 'a-journey', kind: 'action', title: 'Development Journey', subtitle: 'Cómo se construyó este mapa', to: '/journey' },
  { key: 'a-chat', kind: 'action', title: 'Abrir chat', subtitle: 'Preguntá sobre el mapa', to: '/chat' },
  { key: 'a-privacy', kind: 'action', title: 'Política de privacidad', to: '/privacy' },
];

function entryToItem(e: ExplorationEntry, slugOf: (uid: string) => string): Item | null {
  const v = e.view;
  if (v.type === 'concept' && v.uid) {
    return { key: e.id, kind: 'recent', title: e.label, subtitle: 'Concepto reciente', to: `/kb/c/${v.uid}/${slugOf(v.uid)}` };
  }
  if (v.type === 'area' && v.area) {
    return { key: e.id, kind: 'recent', title: e.label, subtitle: 'Área reciente', to: `/kb/${v.area}` };
  }
  if (v.type === 'graph') {
    return { key: e.id, kind: 'recent', title: e.label, subtitle: 'Vista de grafo reciente', to: v.uid ? `/graph/view/${v.uid}` : '/graph' };
  }
  if (v.type === 'path' && v.uid && v.target) {
    return { key: e.id, kind: 'recent', title: e.label, subtitle: 'Camino reciente', to: `/graph?from=${v.uid}&to=${v.target}` };
  }
  return null;
}

export default function CommandPalette({ open, onClose }: { open: boolean; onClose: () => void }) {
  const { bootstrap, areas, byUid } = useRelease();
  const { recent } = useExploration();
  const navigate = useNavigate();
  const [q, setQ] = useState('');
  const [active, setActive] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLUListElement>(null);
  const restoreFocus = useRef<HTMLElement | null>(null);

  const { data: clientIndex } = useClientIndex(open);
  const index = useMemo(() => buildSearchIndex(bootstrap, clientIndex ?? null), [bootstrap, clientIndex]);

  const items = useMemo<Item[]>(() => {
    const slugOf = (uid: string) => byUid.get(uid)?.slug ?? '';
    if (!q.trim()) {
      const recents = recent.map((e) => entryToItem(e, slugOf)).filter((x): x is Item => x !== null);
      return [...recents, ...ACTIONS];
    }
    const lower = q.toLowerCase();
    const conceptItems: Item[] = search(index, q, { limit: 9 }).map((r) => ({
      key: r.uid, kind: 'concept', title: r.title,
      subtitle: r.snippet, areaUid: r.areaUid,
      to: `/kb/c/${r.uid}/${r.slug}`,
    }));
    const areaItems: Item[] = areas
      .filter((a) => a.name.toLowerCase().includes(lower) || a.uid.includes(lower))
      .slice(0, 3)
      .map((a) => ({ key: `area-${a.uid}`, kind: 'area', title: a.name, subtitle: `${a.count} conceptos`, areaUid: a.uid, to: `/kb/${a.uid}` }));
    const actionItems = ACTIONS.filter((a) => a.title.toLowerCase().includes(lower));
    return [...conceptItems, ...areaItems, ...actionItems];
  }, [q, index, areas, recent, byUid]);

  useEffect(() => {
    if (open) {
      restoreFocus.current = document.activeElement as HTMLElement | null;
      setQ('');
      setActive(0);
      const t = setTimeout(() => inputRef.current?.focus(), 30);
      return () => clearTimeout(t);
    }
    restoreFocus.current?.focus?.();
  }, [open]);

  useEffect(() => setActive(0), [q]);

  useEffect(() => {
    const el = listRef.current?.querySelector<HTMLElement>(`[data-idx="${active}"]`);
    el?.scrollIntoView({ block: 'nearest' });
  }, [active]);

  const go = (item: Item | undefined) => {
    if (!item) return;
    navigate(item.to);
    onClose();
  };

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActive((a) => (items.length ? (a + 1) % items.length : 0));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActive((a) => (items.length ? (a - 1 + items.length) % items.length : 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      go(items[active]);
    } else if (e.key === 'Escape') {
      e.preventDefault();
      onClose();
    }
  };

  const iconFor = (item: Item) => {
    if (item.kind === 'recent') return <Clock className="h-4 w-4 text-faint" aria-hidden />;
    if (item.kind === 'area') return <BookOpen className="h-4 w-4" style={{ color: areaColor(item.areaUid) }} aria-hidden />;
    if (item.kind === 'action') {
      if (item.to === '/graph') return <Network className="h-4 w-4 text-muted" aria-hidden />;
      if (item.to === '/chat') return <MessageSquare className="h-4 w-4 text-muted" aria-hidden />;
      if (item.to === '/journey') return <Route className="h-4 w-4 text-muted" aria-hidden />;
      if (item.to === '/privacy') return <Shield className="h-4 w-4 text-muted" aria-hidden />;
      return <BookOpen className="h-4 w-4 text-muted" aria-hidden />;
    }
    return <Search className="h-4 w-4 text-faint" aria-hidden />;
  };

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-[60] flex items-start justify-center px-4 pt-[12vh]"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          transition={{ duration: 0.12 }}
        >
          <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} aria-hidden />
          <motion.div
            role="dialog"
            aria-modal="true"
            aria-label="Búsqueda global"
            className="relative w-full max-w-xl panel shadow-panel overflow-hidden"
            initial={{ opacity: 0, scale: 0.97, y: -6 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.98 }}
            transition={{ duration: 0.14, ease: 'easeOut' }}
            onKeyDown={onKeyDown}
          >
            <div className="flex items-center gap-2.5 px-4 border-b border-line/50">
              <Search className="h-4 w-4 text-faint shrink-0" aria-hidden />
              <input
                ref={inputRef}
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder="Buscar conceptos, áreas, acciones…"
                className="w-full bg-transparent py-3.5 text-sm outline-none placeholder:text-faint"
                aria-label="Texto de búsqueda"
                autoComplete="off"
                spellCheck={false}
              />
              <kbd className="text-[10px] border border-line/70 rounded px-1.5 py-0.5 text-faint shrink-0">Esc</kbd>
            </div>

            <ul ref={listRef} role="listbox" aria-label="Resultados" className="max-h-[46vh] overflow-y-auto p-1.5">
              {items.length === 0 && (
                <li className="px-3 py-8 text-center text-sm text-muted">
                  Sin resultados para “{q}”. Probá con otro término.
                </li>
              )}
              {items.map((item, i) => (
                <li
                  key={item.key}
                  data-idx={i}
                  role="option"
                  aria-selected={i === active}
                  className={`flex items-center gap-3 rounded-lg px-3 py-2.5 cursor-pointer ${i === active ? 'bg-accent/15' : 'hover:bg-raised/60'}`}
                  onMouseEnter={() => setActive(i)}
                  onClick={() => go(item)}
                >
                  {iconFor(item)}
                  <span className="min-w-0 flex-1">
                    <span className="block text-sm font-medium truncate">{item.title}</span>
                    {item.subtitle && <span className="block text-xs text-muted truncate">{item.subtitle}</span>}
                  </span>
                  {item.areaUid && item.kind === 'concept' && (
                    <span aria-hidden className="h-2 w-2 rounded-full shrink-0" style={{ backgroundColor: areaColor(item.areaUid) }} />
                  )}
                  {i === active && <CornerDownLeft className="h-3.5 w-3.5 text-faint shrink-0" aria-hidden />}
                </li>
              ))}
            </ul>

            <div className="flex items-center gap-3 px-4 py-2 border-t border-line/50 text-[11px] text-faint">
              <span><kbd className="border border-line/70 rounded px-1">↑↓</kbd> navegar</span>
              <span><kbd className="border border-line/70 rounded px-1">Enter</kbd> abrir</span>
              <span className="ml-auto">{items.length} resultados</span>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}