/** Colores del modo Obsidian: por defecto todos los nodos del mismo color
 * (mono), editable por el usuario (global + por área, como los grupos de
 * Obsidian). Persiste en localStorage. */
import { useCallback, useEffect, useState } from 'react';

const KEY = 'ikm-obsidian-colors-v2';

export interface ObsidianColors {
  mono: string;
  areas: Record<string, string>;
}

const DEFAULT: ObsidianColors = { mono: '#94a3b8', areas: {} };

function load(): ObsidianColors {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) {
      const p = JSON.parse(raw);
      return { mono: typeof p.mono === 'string' ? p.mono : DEFAULT.mono, areas: p.areas && typeof p.areas === 'object' ? p.areas : {} };
    }
  } catch { /* ignore */ }
  return { ...DEFAULT, areas: {} };
}

export function useObsidianColors() {
  const [colors, setColors] = useState<ObsidianColors>(load);
  useEffect(() => {
    try { localStorage.setItem(KEY, JSON.stringify(colors)); } catch { /* ignore */ }
  }, [colors]);
  const setMono = useCallback((c: string) => setColors((s) => ({ ...s, mono: c })), []);
  const setArea = useCallback((uid: string, c: string | null) => setColors((s) => {
    const areas = { ...s.areas };
    if (c) areas[uid] = c; else delete areas[uid];
    return { ...s, areas };
  }), []);
  const reset = useCallback(() => setColors({ ...DEFAULT, areas: {} }), []);
  return { colors, setMono, setArea, reset };
}