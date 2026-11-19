/** /journey/r/:uid/:slug — registro individual del Journey.
 * Sin registros en el release actual: estado honesto, nunca contenido inventado.
 */
import { Link, useParams } from 'react-router-dom';
import { EmptyState } from '../components/ui';

export default function JourneyRecord() {
  const { uid } = useParams();
  return (
    <div className="p-8">
      <EmptyState
        title="Registro no disponible"
        action={<Link to="/journey" className="btn-primary">Volver al Journey</Link>}
      >
        El registro “{uid}” no existe en este release. Los registros del Journey se
        publican solo después de la curaduría y aprobación del autor.
      </EmptyState>
    </div>
  );
}