/** ExplorationState v1 (§15.4 / §6.6): serializable, versionado, en IndexedDB
 * del navegador, sin cuenta. Las vistas generadas por chat llevan origin:'chat'.
 * Si un uid guardado ya no existe en el release, se descarta y se avisa.
 */

export type ViewType = 'graph' | 'concept' | 'area' | 'path';
export type Origin = 'manual' | 'chat';

export interface ExplorationView {
  type: ViewType;
  uid?: string;
  area?: string;
  target?: string;
  origin: Origin;
}

export interface ExplorationEntry {
  id: string;
  view: ExplorationView;
  label: string;
  at: number;
}

export interface ExplorationState {
  version: 1;
  history: ExplorationEntry[];
}

export const HISTORY_CAP = 50;
const DB_NAME = 'ikm';
const DB_VERSION = 1;
const STORE = 'exploration';
const KEY = 'state';

export function emptyState(): ExplorationState {
  return { version: 1, history: [] };
}

let counter = 0;
function entryId(): string {
  counter += 1;
  return `e_${Date.now().toString(36)}_${counter}`;
}

/** Transición pura: agrega una vista al historial (dedupe de la última, cap fijo). */
export function appendView(state: ExplorationState, view: ExplorationView, label: string, at = Date.now()): ExplorationState {
  const last = state.history[state.history.length - 1];
  if (last && JSON.stringify(last.view) === JSON.stringify(view)) {
    return state;
  }
  const entry: ExplorationEntry = { id: entryId(), view, label, at };
  const history = [...state.history, entry].slice(-HISTORY_CAP);
  return { version: 1, history };
}

export interface PruneResult {
  state: ExplorationState;
  removed: number;
}

/** Descarta entradas cuyo uid ya no existe en el release (fallar abierto). */
export function pruneUnknown(state: ExplorationState, knownUids: Set<string>, knownAreas: Set<string>): PruneResult {
  const kept = state.history.filter((e) => {
    if (e.view.uid && !knownUids.has(e.view.uid)) return false;
    if (e.view.target && !knownUids.has(e.view.target)) return false;
    if (e.view.area && !knownAreas.has(e.view.area)) return false;
    return true;
  });
  return { state: { version: 1, history: kept }, removed: state.history.length - kept.length };
}

// --- IndexedDB (IO aislada; degradación a memoria si no está disponible) ---

function openDb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    if (typeof indexedDB === 'undefined') {
      reject(new Error('IndexedDB no disponible'));
      return;
    }
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = () => {
      if (!req.result.objectStoreNames.contains(STORE)) {
        req.result.createObjectStore(STORE);
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error ?? new Error('IndexedDB error'));
  });
}

export async function loadExploration(): Promise<ExplorationState> {
  try {
    const db = await openDb();
    return await new Promise<ExplorationState>((resolve) => {
      const tx = db.transaction(STORE, 'readonly');
      const req = tx.objectStore(STORE).get(KEY);
      req.onsuccess = () => {
        const raw = req.result as ExplorationState | undefined;
        resolve(raw && raw.version === 1 && Array.isArray(raw.history) ? raw : emptyState());
      };
      req.onerror = () => resolve(emptyState());
      tx.oncomplete = () => db.close();
    });
  } catch {
    return emptyState();
  }
}

export async function saveExploration(state: ExplorationState): Promise<void> {
  try {
    const db = await openDb();
    await new Promise<void>((resolve) => {
      const tx = db.transaction(STORE, 'readwrite');
      tx.objectStore(STORE).put(state, KEY);
      tx.oncomplete = () => { db.close(); resolve(); };
      tx.onerror = () => { db.close(); resolve(); };
    });
  } catch {
    // Sin IndexedDB la exploración sigue funcionando en memoria.
  }
}

export async function clearExploration(): Promise<void> {
  await saveExploration(emptyState());
}