/** Cliente de la API de chat (Capa 20b). El sitio navegable funciona sin
 * backend; el chat informa su estado: disponible / degradado / no-disponible.
 * Nunca inventa respuestas: si el backend no está, se dice.
 */

export type ChatAvailability = 'disponible' | 'degradado' | 'no-disponible' | 'comprobando';

export type ProvenanceKind = 'documented' | 'general' | 'inferred';

export interface Provenance {
  kind: ProvenanceKind;
  chunkIds?: string[];
}

export interface ChatReply {
  text: string;
  provenance: Provenance[];
  degraded: boolean;
  note?: string;
}

export interface ChatTurn {
  role: 'user' | 'assistant';
  text: string;
  provenance?: Provenance[];
  degraded?: boolean;
  note?: string;
}

const API_BASE = '/api';
// El backend expone /health en la raíz (sin prefijo /api) y /api/chat con prefijo.
const HEALTH_URL = '/health';
const PROBE_TIMEOUT_MS = 2500;

async function fetchWithTimeout(url: string, ms: number, init?: RequestInit): Promise<Response> {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), ms);
  try {
    return await fetch(url, { ...init, signal: ctrl.signal });
  } finally {
    clearTimeout(timer);
  }
}

/** Sondea /health. Distingue caído (no-disponible) de stub sin LLM (degradado). */
export async function probeChatAvailability(): Promise<ChatAvailability> {
  try {
    const res = await fetchWithTimeout(HEALTH_URL, PROBE_TIMEOUT_MS);
    if (!res.ok) return 'no-disponible';
    const data = (await res.json()) as Record<string, unknown>;
    // El backend actual es un stub: /health responde pero el chat no tiene LLM real.
    const status = String(data.status ?? data.state ?? '').toLowerCase();
    if (status === 'degraded' || data.llm === false || data.stub === true) return 'degradado';
    return 'disponible';
  } catch {
    return 'no-disponible';
  }
}

interface RawChatBlock {
  text?: string;
  basis?: string;
  sources?: string[];
}

interface RawChatResponse {
  reply?: string;
  text?: string;
  message?: string;
  response?: string;
  blocks?: RawChatBlock[];
  provenance?: { kind?: string; chunk_ids?: string[] }[];
  degraded?: boolean;
}

function basisToKind(basis: string): ProvenanceKind {
  const b = (basis || '').toLowerCase();
  if (b === 'documented' || b === 'quoted' || b === 'documental') return 'documented';
  if (b === 'inferred' || b === 'inferencia') return 'inferred';
  return 'general';
}

/** Envía un mensaje al orquestador. Respuesta sin procedencia => general + aviso. */
export async function sendChat(message: string, history: ChatTurn[]): Promise<ChatReply> {
  const res = await fetchWithTimeout(`${API_BASE}/chat`, 30000, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify({
      message,
      history: history.slice(-10).map((t) => ({ role: t.role, content: t.text })),
    }),
  });
  if (res.status === 401 || res.status === 403) {
    throw new ChatApiError('requiere-login', 'El chat requiere iniciar sesión.');
  }
  if (res.status === 429) {
    throw new ChatApiError('limite', 'Límite de consumo alcanzado. Probá más tarde.');
  }
  if (!res.ok) {
    throw new ChatApiError('http', `El backend respondió HTTP ${res.status}.`);
  }
  const data = (await res.json()) as RawChatResponse;
  let text: string;
  let provenance: Provenance[];

  if (Array.isArray(data.blocks)) {
    // Forma real del orquestador: bloques con text + basis + sources.
    text = data.blocks.map((b) => b.text ?? '').filter(Boolean).join('\n\n');
    const kinds = new Set<ProvenanceKind>();
    const chunkIds: string[] = [];
    for (const b of data.blocks) {
      kinds.add(basisToKind(b.basis ?? ''));
      for (const s of b.sources ?? []) chunkIds.push(s);
    }
    provenance = [...kinds].map((kind) => ({
      kind,
      chunkIds: kind === 'documented' && chunkIds.length ? chunkIds : undefined,
    }));
  } else {
    text = data.reply ?? data.text ?? data.message ?? data.response ?? '';
    provenance = (data.provenance ?? [])
      .filter((p) => p.kind === 'documented' || p.kind === 'general' || p.kind === 'inferred')
      .map((p) => ({ kind: p.kind as ProvenanceKind, chunkIds: p.chunk_ids }));
  }

  if (provenance.length === 0) {
    return {
      text,
      provenance: [{ kind: 'general' }],
      degraded: true,
      note: 'Respuesta sin etiquetas de procedencia: el backend de chat aún está en desarrollo.',
    };
  }
  return { text, provenance, degraded: Boolean(data.degraded) };
}

export class ChatApiError extends Error {
  constructor(public code: 'requiere-login' | 'limite' | 'http' | 'red', message: string) {
    super(message);
    this.name = 'ChatApiError';
  }
}

export const PROVENANCE_LABELS: Record<ProvenanceKind, string> = {
  documented: 'Documentado en el mapa',
  general: 'Conocimiento general del modelo',
  inferred: 'Inferencia (no almacenada)',
};