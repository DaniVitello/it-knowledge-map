import { describe, expect, it } from 'vitest';
import { appendView, emptyState, pruneUnknown, HISTORY_CAP } from './exploration';

describe('appendView', () => {
  it('agrega una vista al historial', () => {
    const s1 = appendView(emptyState(), { type: 'concept', uid: 'c_A', origin: 'manual' }, 'A');
    expect(s1.history).toHaveLength(1);
    expect(s1.history[0].label).toBe('A');
    expect(s1.version).toBe(1);
  });

  it('dedupe vistas consecutivas idénticas', () => {
    const view = { type: 'graph' as const, origin: 'manual' as const };
    const s1 = appendView(emptyState(), view, 'Grafo');
    const s2 = appendView(s1, view, 'Grafo');
    expect(s2).toBe(s1);
  });

  it('respeta el cap de historial', () => {
    let s = emptyState();
    for (let i = 0; i < HISTORY_CAP + 10; i++) {
      s = appendView(s, { type: 'concept', uid: `c_${i}`, origin: 'manual' }, `C${i}`);
    }
    expect(s.history).toHaveLength(HISTORY_CAP);
    expect(s.history[s.history.length - 1].label).toBe(`C${HISTORY_CAP + 9}`);
  });

  it('conserva origin chat', () => {
    const s = appendView(emptyState(), { type: 'graph', uid: 'c_A', origin: 'chat' }, 'Desde chat');
    expect(s.history[0].view.origin).toBe('chat');
  });
});

describe('pruneUnknown', () => {
  it('descarta uids y áreas que ya no existen', () => {
    let s = emptyState();
    s = appendView(s, { type: 'concept', uid: 'c_VIVE', origin: 'manual' }, 'Vive');
    s = appendView(s, { type: 'concept', uid: 'c_MURIO', origin: 'manual' }, 'Murió');
    s = appendView(s, { type: 'area', area: 'networking', origin: 'manual' }, 'Networking');
    s = appendView(s, { type: 'area', area: 'vieja-area', origin: 'manual' }, 'Vieja');
    const { state, removed } = pruneUnknown(s, new Set(['c_VIVE']), new Set(['networking']));
    expect(removed).toBe(2);
    expect(state.history).toHaveLength(2);
  });

  it('sin cambios no reporta removed', () => {
    const s = appendView(emptyState(), { type: 'graph', origin: 'manual' }, 'Grafo');
    const { removed } = pruneUnknown(s, new Set(), new Set());
    expect(removed).toBe(0);
  });
});