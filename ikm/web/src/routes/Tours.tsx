/** /tours/:id — recorridos guiados. Diferido: no hay tours en el release actual. */
import { Link, useParams } from 'react-router-dom';
import { Compass } from 'lucide-react';
import { EmptyState } from '../components/ui';

export default function Tours() {
  const { id } = useParams();
  return (
    <div className="p-8">
      <EmptyState
        icon={<Compass className="h-5 w-5" />}
        title="Recorridos guiados — próximamente"
        action={<Link to="/graph" className="btn-primary">Explorar el grafo libremente</Link>}
      >
        El recorrido “{id}” aún no está publicado. Los tours son secuencias curadas de
        conceptos y registros del Journey; se habilitan cuando el release los incluya.
      </EmptyState>
    </div>
  );
}