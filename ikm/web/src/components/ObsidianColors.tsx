/** Editor de color del modo Obsidian: color uniforme global + colores por área
 * (como los grupos de Obsidian). Los cambios se aplican en vivo al grafo. */
import { RotateCcw } from 'lucide-react';
import type { ObsidianColors } from '../lib/obsidianColors';

export default function ObsidianColorPanel({ colors, setMono, setArea, reset, areas }: {
  colors: ObsidianColors;
  setMono: (c: string) => void;
  setArea: (uid: string, c: string | null) => void;
  reset: () => void;
  areas: { uid: string; name: string }[];
}) {
  return (
    <div className="absolute right-3 top-3 z-30 panel p-3 w-64 max-h-[75%] overflow-y-auto" role="dialog" aria-label="Colores del grafo Obsidian">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-xs font-semibold uppercase tracking-wide text-faint">Color de nodos</h3>
        <button className="btn-ghost !p-1" onClick={reset} title="Restablecer color uniforme" aria-label="Restablecer color uniforme">
          <RotateCcw className="h-3.5 w-3.5" />
        </button>
      </div>
      <label className="flex items-center justify-between gap-2 text-xs text-muted mb-3">
        <span>Uniforme (todos)</span>
        <input
          type="color"
          value={colors.mono}
          onChange={(e) => setMono(e.target.value)}
          className="h-7 w-10 cursor-pointer rounded border border-line/50 bg-transparent"
          aria-label="Color uniforme de todos los nodos"
        />
      </label>
      <p className="text-[11px] text-faint mb-2">Por área (opcional, como los grupos de Obsidian):</p>
      <div className="space-y-1.5">
        {areas.map((a) => (
          <label key={a.uid} className="flex items-center justify-between gap-2 text-xs text-muted">
            <span className="truncate">{a.name}</span>
            <span className="flex items-center gap-1 shrink-0">
              <input
                type="color"
                value={colors.areas[a.uid] ?? colors.mono}
                onChange={(e) => setArea(a.uid, e.target.value)}
                className="h-6 w-8 cursor-pointer rounded border border-line/50 bg-transparent"
                aria-label={`Color de ${a.name}`}
              />
              {colors.areas[a.uid] && (
                <button
                  className="text-faint hover:text-ink text-sm leading-none px-0.5"
                  onClick={() => setArea(a.uid, null)}
                  title="Quitar color de área"
                  aria-label={`Quitar color de ${a.name}`}
                >×</button>
              )}
            </span>
          </label>
        ))}
      </div>
    </div>
  );
}