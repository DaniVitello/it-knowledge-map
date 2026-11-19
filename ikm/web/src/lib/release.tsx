/** Cliente del release estático + hooks (TanStack Query).
 * El sitio navegable NO depende del backend: todo sale de /release/*.json.
 * El release es inmutable -> staleTime Infinity, sin refetch.
 */
import { createContext, useContext, useMemo, type ReactNode } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import type {
  Manifest, ReleaseBootstrap, AreaInfo, GraphData, Ficha, RelationRecord, ClientIndex,
} from './types';

const BASE = `${import.meta.env.BASE_URL}release/`;

export class ReleaseError extends Error {
  constructor(public path: string, public status: number) {
    super(`No se pudo cargar ${path} (HTTP ${status})`);
    this.name = 'ReleaseError';
  }
}

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(BASE + path, { headers: { Accept: 'application/json' } });
  if (!res.ok) throw new ReleaseError(path, res.status);
  return (await res.json()) as T;
}

export const releaseKeys = {
  manifest: ['release', 'manifest'] as const,
  bootstrap: ['release', 'bootstrap'] as const,
  areas: ['release', 'areas'] as const,
  graph: ['release', 'graph'] as const,
  relations: ['release', 'relations'] as const,
  clientIndex: ['release', 'client-index'] as const,
  concept: (uid: string) => ['release', 'concept', uid] as const,
};

export function useManifest() {
  return useQuery({ queryKey: releaseKeys.manifest, queryFn: () => fetchJson<Manifest>('manifest.json') });
}
export function useBootstrap() {
  return useQuery({ queryKey: releaseKeys.bootstrap, queryFn: () => fetchJson<ReleaseBootstrap>('release.json') });
}
export function useAreas() {
  return useQuery({ queryKey: releaseKeys.areas, queryFn: () => fetchJson<AreaInfo[]>('areas.json') });
}
export function useGraph() {
  return useQuery({ queryKey: releaseKeys.graph, queryFn: () => fetchJson<GraphData>('graph.json') });
}
export function useRelations(enabled = true) {
  return useQuery({
    queryKey: releaseKeys.relations,
    queryFn: () => fetchJson<RelationRecord[]>('relations.json'),
    enabled,
  });
}
export function useClientIndex(enabled = true) {
  return useQuery({
    queryKey: releaseKeys.clientIndex,
    queryFn: () => fetchJson<ClientIndex>('client-index.json'),
    enabled,
  });
}
export function useConcept(uid: string | undefined) {
  return useQuery({
    queryKey: releaseKeys.concept(uid ?? ''),
    queryFn: () => fetchJson<Ficha>(`concepts/${uid}.json`),
    enabled: Boolean(uid),
  });
}

export interface ReleaseCore {
  manifest: Manifest;
  bootstrap: ReleaseBootstrap;
  areas: AreaInfo[];
  graph: GraphData;
  byUid: Map<string, ReleaseBootstrap['concepts'][number]>;
  byArea: Map<string, ReleaseBootstrap['concepts']>;
  areaByUid: Map<string, AreaInfo>;
}

const ReleaseContext = createContext<ReleaseCore | null>(null);

/** Carga los 4 archivos de arranque (§15.2) y los expone ya indexados. */
export function ReleaseProvider({ children }: { children: ReactNode }) {
  const manifest = useManifest();
  const bootstrap = useBootstrap();
  const areas = useAreas();
  const graph = useGraph();
  const qc = useQueryClient();

  const ready = manifest.isSuccess && bootstrap.isSuccess && areas.isSuccess && graph.isSuccess;
  const failed = manifest.isError || bootstrap.isError || areas.isError || graph.isError;
  const error = manifest.error ?? bootstrap.error ?? areas.error ?? graph.error;

  const core = useMemo<ReleaseCore | null>(() => {
    if (!ready) return null;
    const byUid = new Map(bootstrap.data!.concepts.map((c) => [c.uid, c]));
    const byArea = new Map<string, ReleaseBootstrap['concepts']>();
    for (const c of bootstrap.data!.concepts) {
      const k = c.area_uid ?? 'sin-area';
      if (!byArea.has(k)) byArea.set(k, []);
      byArea.get(k)!.push(c);
    }
    for (const list of byArea.values()) {
      list.sort((a, b) => (a.numero ?? 0) - (b.numero ?? 0) || a.title.localeCompare(b.title));
    }
    const areaByUid = new Map(areas.data!.map((a) => [a.uid, a]));
    return {
      manifest: manifest.data!,
      bootstrap: bootstrap.data!,
      areas: areas.data!,
      graph: graph.data!,
      byUid,
      byArea,
      areaByUid,
    };
  }, [ready, manifest.data, bootstrap.data, areas.data, graph.data]);

  if (failed) {
    return (
      <div className="min-h-screen flex items-center justify-center p-6">
        <div className="panel max-w-md p-6 text-center">
          <h1 className="text-lg font-semibold mb-2">No se pudo cargar el release</h1>
          <p className="text-sm text-muted mb-4">
            {error instanceof Error ? error.message : 'Error desconocido'}. Verificá que
            <code className="mx-1">npm run sync:release</code> haya copiado el release a
            <code className="mx-1">public/release/</code>.
          </p>
          <button className="btn-primary" onClick={() => qc.invalidateQueries({ queryKey: ['release'] })}>
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  if (!core) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-3" role="status" aria-label="Cargando">
        <div className="h-10 w-10 rounded-full border-2 border-line border-t-accent animate-spin" />
        <p className="text-sm text-muted">Cargando Knowledge Map…</p>
      </div>
    );
  }

  return <ReleaseContext.Provider value={core}>{children}</ReleaseContext.Provider>;
}

export function useRelease(): ReleaseCore {
  const ctx = useContext(ReleaseContext);
  if (!ctx) throw new Error('useRelease debe usarse dentro de <ReleaseProvider>');
  return ctx;
}