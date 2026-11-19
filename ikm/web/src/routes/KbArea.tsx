/** /kb/:area — listado de conceptos de un área, en orden del vault. */
import { useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, ChevronRight, Search } from 'lucide-react';
import { useRelease } from '../lib/release';
import { normalizeText } from '../lib/search';
import { areaColor, areaColorAlpha } from '../lib/format';
import { EmptyState, MarkBadge } from '../components/ui';
import { useRecordView } from '../lib/useExploration';

export default function KbArea() {
  const { area: areaUid } = useParams();
  const { areaByUid, byArea } = useRelease();
  const area = areaUid ? areaByUid.get(areaUid) : undefined;
  const [filter, setFilter] = useState('');

  useRecordView(area ? { type: 'area', area: area.uid, origin: 'manual' } : null, area?.name ?? '');

  const concepts = useMemo(() => {
    const list = areaUid ? byArea.get(areaUid) ?? [] : [];
    const q = normalizeText(filter);
    return q ? list.filter((c) => normalizeText(c.title).includes(q)) : list;
  }, [areaUid, byArea, filter]);

  if (!area) {
    return (
      <div className="p-8">
        <EmptyState title="Área no encontrada" action={<Link className="btn-primary" to="/kb">Ver todas las áreas</Link>}>
          El área “{areaUid}” no existe en este release.
        </EmptyState>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
      <Link to="/kb" className="inline-flex items-center gap-1.5 text-sm text-muted hover:text-ink mb-5">
        <ArrowLeft className="h-3.5 w-3.5" aria-hidden /> Knowledge Base
      </Link>

      <header className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <span
            aria-hidden
            className="h-11 w-11 rounded-xl flex items-center justify-center font-bold"
            style={{ backgroundColor: areaColorAlpha(area.uid, 0.16), color: areaColor(area.uid) }}
          >
            {String(area.order).padStart(2, '0')}
          </span>
          <div>
            <h1 className="text-2xl font-bold leading-tight">{area.name}</h1>
            <p className="text-sm text-muted">{area.count} conceptos</p>
          </div>
        </div>
        {area.context_framing && <p className="text-sm text-muted leading-relaxed max-w-2xl">{area.context_framing}</p>}
        {area.professional_roles.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-3">
            {area.professional_roles.map((r) => (
              <span key={r} className="chip bg-raised/80 text-muted border border-line/50">{r}</span>
            ))}
          </div>
        )}
      </header>

      <div className="relative mb-4 max-w-sm">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-faint" aria-hidden />
        <input
          className="input !pl-9"
          placeholder="Filtrar en esta área…"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          aria-label="Filtrar conceptos del área"
        />
      </div>

      <ul className="space-y-1.5" aria-label={`Conceptos de ${area.name}`}>
        {concepts.map((c, i) => {
          return (
            <motion.li
              key={c.uid}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2, delay: Math.min(i * 0.02, 0.3) }}
            >
              <Link
                to={`/kb/c/${c.uid}/${c.slug}`}
                className="panel flex items-center gap-3 px-4 py-3 hover:border-line transition-colors group"
              >
                <span className="text-xs text-faint tabular-nums w-7 shrink-0">
                  {c.numero != null ? String(c.numero).padStart(2, '0') : '—'}
                </span>
                <span className="flex-1 min-w-0">
                  <span className="block text-sm font-medium truncate group-hover:text-accent transition-colors">{c.title}</span>
                  {c.sections_missing.length > 0 && (
                    <span className="block text-[11px] text-faint">
                      Faltan secciones: {c.sections_missing.join(', ')}
                    </span>
                  )}
                </span>
                {c.marks_count > 0 && <MarkBadge kind="sin_verificar" />}
                <ChevronRight className="h-4 w-4 text-faint group-hover:text-accent group-hover:translate-x-0.5 transition-all shrink-0" aria-hidden />
              </Link>
            </motion.li>
          );
        })}
        {concepts.length === 0 && (
          <li className="panel px-4 py-8 text-center text-sm text-muted">Ningún concepto coincide con “{filter}”.</li>
        )}
      </ul>
    </div>
  );
}