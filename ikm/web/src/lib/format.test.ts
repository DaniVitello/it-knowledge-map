import { describe, expect, it } from 'vitest';
import { canonicalSectionKey, markLabel, relationTypeLabel, areaColor } from './format';

describe('canonicalSectionKey', () => {
  it('mapea headings humanos a claves canónicas', () => {
    expect(canonicalSectionKey('Estado actual')).toBe('estado_actual');
    expect(canonicalSectionKey('Errores comunes')).toBe('errores_comunes');
    expect(canonicalSectionKey('Ideas clave')).toBe('ideas_clave');
  });
  it('normaliza tildes', () => {
    expect(canonicalSectionKey('Cómo funciona')).toBe('como_funciona');
    expect(canonicalSectionKey('Ejemplo mínimo')).toBe('ejemplo_minimo');
  });
  it('descarta sufijos entre paréntesis', () => {
    expect(canonicalSectionKey('Detalles (avanzado)')).toBe('detalles');
  });
  it('heading desconocido -> null', () => {
    expect(canonicalSectionKey('Sección inventada')).toBeNull();
    expect(canonicalSectionKey('')).toBeNull();
  });
});

describe('etiquetas', () => {
  it('markLabel traduce las marcas de integridad', () => {
    expect(markLabel('sin_verificar')).toBe('Sin verificar');
    expect(markLabel('verificar')).toBe('Verificar');
  });
  it('relationTypeLabel traduce tipos conocidos', () => {
    expect(relationTypeLabel('prerequisite')).toBe('Prerrequisito');
    expect(relationTypeLabel('untyped')).toBe('Relación');
  });
  it('areaColor usa el token del área con fallback', () => {
    expect(areaColor('frontend')).toContain('--area-frontend');
    expect(areaColor(null)).toContain('148 163 184');
  });
});