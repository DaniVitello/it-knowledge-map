/** /kb/c/:uid/:slug — ficha completa del concepto.
 * 10 secciones del contrato, marcas de integridad visibles, relaciones quoted,
 * fuentes, navegación prev/next y vista en el grafo.
 */
import { useMemo } from 'react';
import { Link, Navigate, useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { AlertTriangle, ArrowLeft, ArrowRight, ExternalLink, Hash, Network } from 'lucide-react';
import { useConcept, useRelease, useRelations } from '../lib/release';
import { SECTION_HINTS, SECTION_LABELS, SECTION_ORDER, canonicalSectionKey, type SectionKey } from '../lib/format';
import { AreaBadge, EmptyState, MarkBadge, PageSkeleton } from '../components/ui';
import Markdown from '../components/Markdown';
import RelationCard from '../components/RelationCard';
import { useRecordView } from '../lib/useExploration';

export default function Concept() {
  const { uid, slug } = useParams();
  const { byUid, byArea, areaByUid } = useRelease();
  const { data: ficha, isLoading, isError } = useConcept(uid);
  const { data: relations } = useRelations(Boolean(uid));

  const entry = uid ? byUid.get(uid) : undefined;
  useRecordView(ficha ? { type: 'concept', uid: ficha.uid, origin: 'manual' } : null, ficha?.title ?? '');

  const marksBySection = useMemo(() => {
    const map = new Map<string, string[]>();
    for (const m of ficha?.verification_marks ?? []) {
      const key = canonicalSectionKey(m.section) ?? m.section;
      if (!map.has(key)) map.set(key, []);
      map.get(key)!.push(m.kind);
    }
    return map;
  }, [ficha]);

  const conceptRelations = useMemo(() => {
    if (!relations || !uid) return [];
    return relations.filter((r) => r.source_uid === uid || r.target_uid === uid);
  }, [relations, uid]);

  const siblings = useMemo(() => {
    if (!entry?.area_uid) return { prev: undefined, next: undefined };
    const list = byArea.get(entry.area_uid) ?? [];
    const i = list.findIndex((c) => c.uid === uid);
    return { prev: i > 0 ? list[i - 1] : undefined, next: i >= 0 && i < list.length - 1 ? list[i + 1] : undefined };
  }, [entry, byArea, uid]);

  if (!uid || !entry) {
    return (
      <div className="p-8">
        <EmptyState title="Concepto no encontrado" action={<Link className="btn-primary" to="/kb">Ir a la Knowledge Base</Link>}>
          El uid “{uid}” no existe en este release.
        </EmptyState>
      </div>
    );
  }
  if (isLoading) return <PageSkeleton />;
  if (isError || !ficha) {
    return (
      <div className="p-8">
        <EmptyState title="No se pudo cargar la ficha">
          El archivo del concepto no está disponible en el release estático.
        </EmptyState>
      </div>
    );
  }
  // URL canónica: el slug correcto es el del release.
  if (slug !== ficha.slug) {
    return <Navigate to={`/kb/c/${ficha.uid}/${ficha.slug}`} replace />;
  }

  const area = ficha.area_uid ? areaByUid.get(ficha.area_uid) : undefined;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
      {/* Breadcrumb */}
      <nav aria-label="Miga de pan" className="flex items-center gap-1.5 text-sm text-muted mb-5 flex-wrap">
        <Link to="/kb" className="hover:text-ink inline-flex items-center gap-1">
          <ArrowLeft className="h-3.5 w-3.5" aria-hidden /> KB
        </Link>
        <span aria-hidden>/</span>
        {area && (
          <>
            <Link to={`/kb/${area.uid}`} className="hover:text-ink">{area.name}</Link>
            <span aria-hidden>/</span>
          </>
        )}
        <span className="text-ink font-medium truncate">{ficha.title}</span>
      </nav>

      <div className="grid gap-8 lg:grid-cols-[1fr_300px]">
        <article className="min-w-0">
          {/* Encabezado */}
          <motion.header initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.25 }} className="mb-6">
            <div className="flex items-start gap-3 flex-wrap mb-2">
              <h1 className="text-3xl font-bold tracking-tight">{ficha.title}</h1>
              {ficha.numero != null && (
                <span className="chip bg-raised/80 text-faint border border-line/50 mt-1.5">
                  <Hash className="h-3 w-3" aria-hidden />{String(ficha.numero).padStart(2, '0')}
                </span>
              )}
            </div>
            <div className="flex items-center gap-2 flex-wrap">
              <AreaBadge areaUid={ficha.area_uid} />
              {(ficha.aliases ?? []).map((a) => (
                <span key={a} className="chip bg-raised/70 text-muted border border-line/50">alias: {a}</span>
              ))}
              {(ficha.verification_marks ?? []).length > 0 && (
                <span className="chip bg-amber-400/15 text-amber-500 dark:text-amber-300 border border-amber-400/30">
                  <AlertTriangle className="h-3 w-3" aria-hidden />
                  {ficha.verification_marks!.length} marca(s) de integridad
                </span>
              )}
            </div>
            {(ficha.tags ?? []).length > 0 && (
              <p className="mt-2 text-xs text-faint font-mono truncate">{ficha.tags!.join(' · ')}</p>
            )}
            <div className="flex gap-2 mt-4">
              <Link to={`/graph/view/${ficha.uid}`} className="btn-ghost !py-1.5 text-xs">
                <Network className="h-3.5 w-3.5" aria-hidden /> Ver en el grafo
              </Link>
            </div>
          </motion.header>

          {/* Navegación de secciones */}
          <nav aria-label="Secciones de la ficha" className="flex flex-wrap gap-1.5 pb-2 mb-6 sticky top-14 z-20 bg-base/90 backdrop-blur-sm -mx-1 px-1">
            {SECTION_ORDER.map((key) => {
              const has = Boolean(ficha.sections?.[key]);
              return (
                <a
                  key={key}
                  href={`#sec-${key}`}
                  className={`chip whitespace-nowrap border transition-colors ${
                    has
                      ? 'bg-raised/70 border-line/60 text-muted hover:text-accent hover:border-accent/40'
                      : 'bg-transparent border-line/30 text-faint/60'
                  }`}
                >
                  {SECTION_LABELS[key]}
                </a>
              );
            })}
          </nav>

          {/* Secciones */}
          <div className="space-y-8">
            {SECTION_ORDER.map((key: SectionKey) => {
              const body = ficha.sections?.[key];
              const marks = marksBySection.get(key) ?? [];
              const isReview = key === 'preguntas_repaso';
              const sectionEl = (
                <section id={`sec-${key}`} aria-label={SECTION_LABELS[key]} className="scroll-mt-28">
                  <div className="flex items-center gap-2 mb-1 flex-wrap">
                    <h2 className="text-lg font-semibold">{SECTION_LABELS[key]}</h2>
                    {marks.map((kind, i) => <MarkBadge key={`${kind}-${i}`} kind={kind} />)}
                    {!body && <span className="text-[11px] text-faint chip bg-raised/50 border border-line/40">sin contenido</span>}
                  </div>
                  <p className="text-xs text-faint mb-2.5">{SECTION_HINTS[key]}</p>
                  {body ? (
                    isReview ? (
                      <details className="panel p-4">
                        <summary className="cursor-pointer text-sm text-muted select-none">
                          Mostrar preguntas (fuera del corpus de respuestas)
                        </summary>
                        <div className="mt-3"><Markdown text={body} /></div>
                      </details>
                    ) : (
                      <Markdown text={body} />
                    )
                  ) : (
                    <p className="text-sm text-faint italic">Esta sección no tiene contenido en el vault.</p>
                  )}
                </section>
              );
              return <div key={key}>{sectionEl}</div>;
            })}
          </div>

          {/* Prev / Next */}
          <nav aria-label="Conceptos vecinos del área" className="grid sm:grid-cols-2 gap-3 mt-10 pt-6 border-t border-line/50">
            {siblings.prev ? (
              <Link to={`/kb/c/${siblings.prev.uid}/${siblings.prev.slug}`} className="panel p-3.5 hover:border-line group">
                <span className="text-[11px] text-faint inline-flex items-center gap-1"><ArrowLeft className="h-3 w-3" aria-hidden /> Anterior</span>
                <span className="block text-sm font-medium truncate group-hover:text-accent">{siblings.prev.title}</span>
              </Link>
            ) : <span />}
            {siblings.next && (
              <Link to={`/kb/c/${siblings.next.uid}/${siblings.next.slug}`} className="panel p-3.5 hover:border-line group text-right">
                <span className="text-[11px] text-faint inline-flex items-center gap-1">Siguiente <ArrowRight className="h-3 w-3" aria-hidden /></span>
                <span className="block text-sm font-medium truncate group-hover:text-accent">{siblings.next.title}</span>
              </Link>
            )}
          </nav>
        </article>

        {/* Sidebar */}
        <aside className="space-y-5 lg:sticky lg:top-20 self-start">
          <section aria-label="Relaciones" className="panel p-4">
            <h2 className="text-sm font-semibold mb-3">
              Relaciones <span className="text-faint font-normal">({conceptRelations.length})</span>
            </h2>
            <div className="space-y-2.5 max-h-[420px] overflow-y-auto pr-1">
              {conceptRelations.map((r) => (
                <RelationCard key={r.uid} relation={r} perspectiveUid={ficha.uid} compact />
              ))}
              {conceptRelations.length === 0 && (
                <p className="text-xs text-faint">Este concepto no tiene relaciones en el release.</p>
              )}
            </div>
          </section>

          {(ficha.sources_detail ?? ficha.sources ?? []).length > 0 && (
            <section aria-label="Fuentes" className="panel p-4">
              <h2 className="text-sm font-semibold mb-2.5">Fuentes</h2>
              <ul className="space-y-1.5">
                {(ficha.sources_detail ?? []).map((s) => (
                  <li key={s.url}>
                    <a href={s.url} target="_blank" rel="noopener noreferrer" className="text-xs text-accent hover:underline inline-flex items-center gap-1 break-all">
                      <ExternalLink className="h-3 w-3 shrink-0" aria-hidden />{s.title || s.url}
                    </a>
                  </li>
                ))}
                {(ficha.sources_detail ?? []).length === 0 && (ficha.sources ?? []).map((url) => (
                  <li key={url}>
                    <a href={url} target="_blank" rel="noopener noreferrer" className="text-xs text-accent hover:underline break-all">{url}</a>
                  </li>
                ))}
              </ul>
            </section>
          )}

          <details className="panel p-4 text-xs text-muted space-y-1.5">
            <summary className="cursor-pointer select-none text-sm font-semibold text-ink">Detalle técnico del release</summary>
            <div className="mt-2 space-y-1.5">
              <p><span className="text-faint">uid:</span> <span className="font-mono">{ficha.uid}</span></p>
              <p><span className="text-faint">hash:</span> <span className="font-mono">{ficha.content_hash.slice(0, 12)}…</span></p>
              <p>
                <span className="text-faint">secciones:</span>{' '}
                {10 - (ficha.sections_missing ?? []).length}/10 completas
              </p>
              {(ficha.sections_missing ?? []).length > 0 && (
                <p className="text-faint">Faltan: {ficha.sections_missing!.join(', ')}</p>
              )}
            </div>
          </details>
        </aside>
      </div>
    </div>
  );
}