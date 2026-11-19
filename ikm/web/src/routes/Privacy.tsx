/** /privacy — política de privacidad del sitio estático. */
import { Shield } from 'lucide-react';

export default function Privacy() {
  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-10">
      <h1 className="text-2xl font-bold mb-6 inline-flex items-center gap-2.5">
        <Shield className="h-6 w-6 text-accent" aria-hidden /> Privacidad
      </h1>
      <div className="panel p-6 space-y-5 text-sm leading-relaxed text-muted">
        <section>
          <h2 className="font-semibold text-ink mb-1.5">Sin cuentas, sin tracking</h2>
          <p>
            El sitio navegable es 100% estático: no requiere inicio de sesión, no usa cookies
            de terceros, no incluye analytics ni envía datos de navegación a ningún servidor.
          </p>
        </section>
        <section>
          <h2 className="font-semibold text-ink mb-1.5">Tu exploración queda en tu navegador</h2>
          <p>
            El historial de exploración (conceptos y vistas recientes) se guarda en IndexedDB
            de tu navegador, sin cuenta y sin salir de tu dispositivo. Podés borrarlo desde
            la paleta de búsqueda o limpiando los datos del sitio. El tema elegido se guarda
            en localStorage.
          </p>
        </section>
        <section>
          <h2 className="font-semibold text-ink mb-1.5">Chat (opcional)</h2>
          <p>
            Si usás el chat, tus mensajes se envían al backend del proyecto para generar una
            respuesta con el modelo configurado. El chat requiere sesión cuando está habilitado
            en producción y tiene límites de consumo. Las respuestas se etiquetan por procedencia
            (documentado / general / inferencia) y nunca se almacenan como contenido del mapa.
          </p>
        </section>
        <section>
          <h2 className="font-semibold text-ink mb-1.5">Contenido</h2>
          <p>
            Las fichas provienen del vault personal del autor (IT-Mind-Map), procesadas por un
            pipeline determinista con compuerta de publicación: sin canarios, sin secretos,
            con hashes verificables. Las afirmaciones sin fuente llevan marca visible
            «sin verificar».
          </p>
        </section>
      </div>
    </div>
  );
}