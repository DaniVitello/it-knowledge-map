/** /kb — índice general: áreas + listado completo filtrable. */
import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { Search } from 'lucide-react';
import { useRelease } from '../lib/release';
import { normalizeText } from '../lib/search';
import AreaCard from '../components/AreaCard';
import { AreaBadge, MarkBadge } from '../components/ui';
import { useRecordView } from '../lib/useExploration';

export default function KbIndex() {
  const { areas, bootstrap } = useRelease();
  const [filter, setFilter] = useState('');
  useRecordView(null, '');

  const concepts = useMemo(() => {
    const q = normalizeText(filter);
    const all = [...bootstrap.concepts].sort((a, b) => a.title.localeCompare(b.title));
    if (!q) return all;
    return all.filter((c) => normalizeText(c.title).includes(q));
  }, [bootstrap, filter]);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
      <header className="mb-6">
        <h1 className="text-2xl font-bold mb-1">Knowledge Base</h1>
        <p className="text-sm text-muted">
          {bootstrap.concepts.length} conceptos en {areas.length} áreas. Cada ficha tiene 10 secciones
          y sus relaciones con el resto del mapa.
        </p>
      </header>

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 mb-10">
        {areas.map((a, i) => <AreaCard key={a.uid} area={a} index={i} />)}
      </div>

      <section aria-label="Todos los conceptos">
        <div className="flex flex-wrap items-center gap-3 mb-4">
          <h2 className="text-lg font-semibold">Todos los conceptos</h2>
          <div className="relative ml-auto w-full sm:w-72">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-faint" aria-hidden />
            <input
              className="input !pl-9"
              placeholder="Filtrar por título…"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              aria-label="Filtrar conceptos por título"
            />
          </div>
        </div>

        <ul className="panel divide-y divide-line/40 overflow-hidden">
          {concepts.map((c) => (
            <li key={c.uid}>
              <Link
                to={`/kb/c/${c.uid}/${c.slug}`}
                className="flex items-center gap-3 px-4 py-2.5 hover:bg-raised/50 transition-colors"
              >
                <span className="text-sm font-medium truncate flex-1">{c.title}</span>
                {c.marks_count > 0 && <MarkBadge kind="sin_verificar" />}
                <AreaBadge areaUid={c.area_uid} />
              </Link>
            </li>
          ))}
          {concepts.length === 0 && (
            <li className="px-4 py-8 text-center text-sm text-muted">Ningún concepto coincide con “{filter}”.</li>
          )}
        </ul>
      </section>
    </div>
  );
}