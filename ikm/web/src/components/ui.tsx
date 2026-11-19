/** UI compartida: badges, estados vacíos, skeletons, error boundary. */
import { Component, type ReactNode } from 'react';
import { AlertTriangle, Info, RefreshCw } from 'lucide-react';
import { useRelease } from '../lib/release';
import { areaColor, areaColorAlpha, markLabel } from '../lib/format';
import { PROVENANCE_LABELS, type ProvenanceKind } from '../lib/api';

export function Spinner({ className = 'h-5 w-5' }: { className?: string }) {
  return (
    <span
      role="status"
      aria-label="Cargando"
      className={`inline-block rounded-full border-2 border-line border-t-accent animate-spin ${className}`}
    />
  );
}

export function Skeleton({ className = '' }: { className?: string }) {
  return <div aria-hidden className={`skeleton ${className}`} />;
}

export function PageSkeleton() {
  return (
    <div className="p-6 max-w-5xl mx-auto space-y-4" role="status" aria-label="Cargando página">
      <Skeleton className="h-8 w-64" />
      <Skeleton className="h-4 w-96" />
      <div className="grid gap-3 sm:grid-cols-2 mt-6">
        <Skeleton className="h-28" />
        <Skeleton className="h-28" />
        <Skeleton className="h-28" />
        <Skeleton className="h-28" />
      </div>
    </div>
  );
}

export function EmptyState({ icon, title, children, action }: {
  icon?: ReactNode; title: string; children?: ReactNode; action?: ReactNode;
}) {
  return (
    <div className="panel p-8 text-center max-w-lg mx-auto">
      <div className="mx-auto mb-3 h-12 w-12 rounded-full bg-raised/80 flex items-center justify-center text-muted">
        {icon ?? <Info className="h-5 w-5" />}
      </div>
      <h2 className="font-semibold text-lg mb-1.5">{title}</h2>
      <div className="text-sm text-muted leading-relaxed">{children}</div>
      {action && <div className="mt-5">{action}</div>}
    </div>
  );
}

export function AreaBadge({ areaUid, showName = true }: { areaUid: string | null | undefined; showName?: boolean }) {
  const { areaByUid } = useRelease();
  const area = areaUid ? areaByUid.get(areaUid) : undefined;
  const name = area?.name ?? 'Sin área';
  return (
    <span
      className="chip"
      style={{ backgroundColor: areaColorAlpha(areaUid, 0.14), color: areaColor(areaUid) }}
      title={name}
    >
      <span aria-hidden className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: areaColor(areaUid) }} />
      {showName && name}
    </span>
  );
}

/** Las marcas de verificación son señales de integridad: siempre visibles. */
export function MarkBadge({ kind, section }: { kind: string; section?: string }) {
  return (
    <span
      className="chip bg-amber-400/15 text-amber-500 dark:text-amber-300 border border-amber-400/30"
      title={section ? `Sección: ${section}` : undefined}
    >
      <AlertTriangle className="h-3 w-3" aria-hidden />
      {markLabel(kind)}
      {section && <span className="opacity-70">· {section}</span>}
    </span>
  );
}

export function ProvenanceBadge({ kind }: { kind: ProvenanceKind }) {
  const styles: Record<ProvenanceKind, string> = {
    documented: 'bg-emerald-400/15 text-emerald-600 dark:text-emerald-300 border-emerald-400/30',
    general: 'bg-sky-400/15 text-sky-600 dark:text-sky-300 border-sky-400/30',
    inferred: 'bg-amber-400/15 text-amber-600 dark:text-amber-300 border-amber-400/30',
  };
  return (
    <span className={`chip border ${styles[kind]}`} title={PROVENANCE_LABELS[kind]}>
      {PROVENANCE_LABELS[kind]}
    </span>
  );
}

interface EBProps { children: ReactNode }
interface EBState { error: Error | null }

export class ErrorBoundary extends Component<EBProps, EBState> {
  state: EBState = { error: null };

  static getDerivedStateFromError(error: Error): EBState {
    return { error };
  }

  render() {
    if (this.state.error) {
      return (
        <div className="min-h-screen flex items-center justify-center p-6">
          <div className="panel max-w-md p-6 text-center">
            <AlertTriangle className="h-8 w-8 text-amber-400 mx-auto mb-3" />
            <h1 className="text-lg font-semibold mb-2">Algo se rompió en la vista</h1>
            <p className="text-sm text-muted mb-4 break-words">{this.state.error.message}</p>
            <button className="btn-primary" onClick={() => window.location.reload()}>
              <RefreshCw className="h-4 w-4" /> Recargar
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}