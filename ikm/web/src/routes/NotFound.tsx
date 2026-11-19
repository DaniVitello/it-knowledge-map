/** 404 — ruta no encontrada. */
import { Link } from 'react-router-dom';
import { Compass } from 'lucide-react';
import { EmptyState } from '../components/ui';

export default function NotFound() {
  return (
    <div className="p-10">
      <EmptyState
        icon={<Compass className="h-5 w-5" />}
        title="Esta ruta no existe"
        action={<Link to="/" className="btn-primary">Volver al inicio</Link>}
      >
        La página que buscás no está en el mapa. Probá con la búsqueda global (Ctrl+K).
      </EmptyState>
    </div>
  );
}