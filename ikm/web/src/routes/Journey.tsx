/** /journey — Development Journey (C5/C6).
 * Estado honesto: los registros curados aún no existen en el release.
 * La ruta y la vista quedan listas para cuando el autor apruebe registros.
 */
import { Link } from 'react-router-dom';
import { Route as RouteIcon } from 'lucide-react';
import { useRelease } from '../lib/release';
import { EmptyState } from '../components/ui';
import { useRecordView } from '../lib/useExploration';

export default function Journey() {
  const { manifest } = useRelease();
  useRecordView(null, '');
  const records = manifest.counts.journey_records;

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10">
      <header className="mb-8 text-center">
        <h1 className="text-2xl font-bold mb-2">Development Journey</h1>
        <p className="text-sm text-muted leading-relaxed max-w-xl mx-auto">
          La historia de cómo se construyó este mapa: decisiones, bugs, arquitectura y
          lecciones, con evidencias (documentos, capturas, visualizaciones) y vínculos
          a los conceptos que explica.
        </p>
      </header>

      {records === 0 ? (
        <EmptyState
          icon={<RouteIcon className="h-5 w-5" />}
          title="Journey en curaduría"
          action={<Link to="/kb" className="btn-primary">Explorar la Knowledge Base</Link>}
        >
          Este release incluye <strong>0 registros aprobados</strong>. El material crudo
          (documentos del día a día del proyecto) existe, pero cada registro debe ser
          curado y aprobado por el autor antes de publicarse: el pipeline nunca escribe
          el Journey por su cuenta. Cuando haya registros aprobados, aparecerán acá como
          una cronología con evidencias.
        </EmptyState>
      ) : (
        <p className="text-sm text-muted text-center">
          {records} registros publicados. (La vista de cronología se habilita en la Entrega 2.)
        </p>
      )}
    </div>
  );
}