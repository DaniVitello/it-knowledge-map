/** Relación entre conceptos con su explicación quoted (C4).
 * Perspectiva: desde qué concepto se mira. La explicación se cita, no se inventa.
 */
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import type { RelationRecord } from '../lib/types';
import { useRelease } from '../lib/release';
import { cleanExplanationText } from '../lib/wikilinks';
import { areaColor, relationTypeLabel } from '../lib/format';

export default function RelationCard({ relation, perspectiveUid, compact = false }: {
  relation: RelationRecord;
  perspectiveUid?: string;
  compact?: boolean;
}) {
  const { byUid } = useRelease();
  const source = byUid.get(relation.source_uid);
  const target = byUid.get(relation.target_uid);
  const other = perspectiveUid === relation.source_uid ? target : source;
  const otherUid = perspectiveUid === relation.source_uid ? relation.target_uid : relation.source_uid;
  const explanation = relation.explanation;
  const text = explanation ? cleanExplanationText(explanation.text) : '';

  if (!source || !target) return null;

  return (
    <div className={compact ? 'py-2' : 'panel p-3.5'}>
      <div className="flex items-center gap-1.5 text-sm flex-wrap">
        {perspectiveUid ? (
          <span className="inline-flex items-center gap-1.5 min-w-0">
            <span aria-hidden className="h-1.5 w-1.5 rounded-full shrink-0" style={{ backgroundColor: areaColor(other?.area_uid) }} />
            <Link
              to={`/kb/c/${otherUid}/${other?.slug ?? ''}`}
              className="font-medium text-accent hover:underline underline-offset-2 truncate"
            >
              {other?.title ?? otherUid}
            </Link>
          </span>
        ) : (
          <>
            <Link to={`/kb/c/${source.uid}/${source.slug}`} className="font-medium hover:text-accent truncate">
              {source.title}
            </Link>
            <ArrowRight className="h-3.5 w-3.5 text-faint shrink-0" aria-hidden />
            <Link to={`/kb/c/${target.uid}/${target.slug}`} className="font-medium hover:text-accent truncate">
              {target.title}
            </Link>
          </>
        )}
        <span className="chip bg-raised/80 text-muted border border-line/50 !text-[10px]">
          {relationTypeLabel(relation.type ?? 'untyped')}
        </span>
        {relation.cross_area && (
          <span className="chip bg-violet-400/10 text-violet-500 dark:text-violet-300 border border-violet-400/25 !text-[10px]">
            cross-área
          </span>
        )}
      </div>
      {text && (
        <p className="mt-1.5 text-xs text-muted leading-relaxed">{text}</p>
      )}
    </div>
  );
}