/** Presentación: etiquetas de secciones, colores por área, marcas de integridad. */
import type { ConceptSections } from '@contracts/index';

export type SectionKey = keyof ConceptSections;

export const SECTION_ORDER: SectionKey[] = [
  'objetivo', 'ideas_clave', 'como_funciona', 'detalles', 'ejemplo_minimo',
  'errores_comunes', 'estado_actual', 'conexiones', 'ruta_estudio', 'preguntas_repaso',
];

export const SECTION_LABELS: Record<SectionKey, string> = {
  objetivo: 'Objetivo',
  ideas_clave: 'Ideas clave',
  como_funciona: 'Cómo funciona',
  detalles: 'Detalles',
  ejemplo_minimo: 'Ejemplo mínimo',
  errores_comunes: 'Errores comunes',
  estado_actual: 'Estado actual',
  conexiones: 'Conexiones',
  ruta_estudio: 'Ruta de estudio',
  preguntas_repaso: 'Preguntas de repaso',
};

export const SECTION_HINTS: Record<SectionKey, string> = {
  objetivo: 'Para qué sirve y qué problema resuelve',
  ideas_clave: 'Los conceptos nucleares, en una lista',
  como_funciona: 'El mecanismo, paso a paso',
  detalles: 'Matices y profundidad técnica',
  ejemplo_minimo: 'El caso más chico que lo muestra',
  errores_comunes: 'Dónde se suele equivocar la gente',
  estado_actual: 'Madurez y vigencia del concepto',
  conexiones: 'Cómo se enlaza con otros conceptos',
  ruta_estudio: 'Por dónde seguir aprendiendo',
  preguntas_repaso: 'Para autoevaluarte (fuera del corpus de respuestas)',
};

const AREA_FALLBACK = '148 163 184';

/** Color CSS del área (variable de tokens.css). */
export function areaColor(areaUid: string | null | undefined): string {
  if (!areaUid) return `rgb(${AREA_FALLBACK})`;
  return `rgb(var(--area-${areaUid}, ${AREA_FALLBACK}))`;
}

export function areaColorAlpha(areaUid: string | null | undefined, alpha: number): string {
  if (!areaUid) return `rgb(${AREA_FALLBACK} / ${alpha})`;
  return `rgb(var(--area-${areaUid}, ${AREA_FALLBACK}) / ${alpha})`;
}

export function markLabel(kind: string): string {
  if (kind === 'sin_verificar') return 'Sin verificar';
  if (kind === 'verificar') return 'Verificar';
  return kind;
}

/** Normaliza un heading de sección del vault a su clave canónica del contrato.
 * Las marcas de verificación guardan el heading humano ("Estado actual");
 * las secciones usan snake_case ("estado_actual"). Sin tildes ni sufijos.
 */
export function canonicalSectionKey(raw: string): SectionKey | null {
  const norm = (raw || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\(.*?\)/g, '')
    .trim()
    .replace(/\s+/g, '_');
  return SECTION_ORDER.find((k) => k === norm) ?? null;
}

export function relationTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    untyped: 'Relación',
    prerequisite: 'Prerrequisito',
    builds_on: 'Se apoya en',
    alternative_to: 'Alternativa a',
    part_of: 'Parte de',
    uses: 'Usa',
    contrasts_with: 'Contrasta con',
    evolves_to: 'Evoluciona a',
  };
  return labels[type] ?? type;
}

export function formatCount(n: number): string {
  return new Intl.NumberFormat('es-AR').format(n);
}