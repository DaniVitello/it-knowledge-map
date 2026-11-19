/** Presentación (/): hero, métricas del release, áreas y cómo leer el mapa. */
import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { animate, motion, useMotionValue, useReducedMotion, useTransform } from 'framer-motion';
import { AlertTriangle, BookOpen, Network, Quote, Sparkles } from 'lucide-react';
import { useRelease } from '../lib/release';
import { formatCount } from '../lib/format';
import AreaCard from '../components/AreaCard';
import { useRecordView } from '../lib/useExploration';

/** Cuenta desde 0 hasta el valor real al montar (respeta reduced-motion). */
function CountUp({ to, format }: { to: number; format: (n: number) => string }) {
  const reduced = useReducedMotion();
  const mv = useMotionValue(reduced ? to : 0);
  const text = useTransform(mv, (v) => format(Math.round(v)));
  useEffect(() => {
    if (reduced) { mv.set(to); return; }
    const c = animate(mv, to, { duration: 1.2, ease: [0.22, 1, 0.36, 1] });
    return () => c.stop();
  }, [to, reduced, mv]);
  return <motion.span>{text}</motion.span>;
}

function Stat({ value, label, delay, format }: { value: number; label: string; delay: number; format: (n: number) => string }) {
  return (
    <motion.div
      className="panel px-5 py-4 text-center"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, delay }}
    >
      <p className="text-2xl font-bold tabular-nums text-accent"><CountUp to={value} format={format} /></p>
      <p className="text-xs text-muted mt-0.5">{label}</p>
    </motion.div>
  );
}

export default function Home() {
  const { manifest, areas, bootstrap } = useRelease();
  useRecordView(null, '');
  const counts = manifest.counts;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-10">
      {/* Hero */}
      <section className="relative text-center mb-12">
        <div
          aria-hidden
          className="hero-aurora absolute inset-x-0 -top-10 h-64 pointer-events-none"
          style={{ background: 'radial-gradient(ellipse 60% 50% at 50% 0%, rgb(var(--c-accent) / 0.16), transparent)' }}
        />
        <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <p className="chip bg-accent/12 text-accent border border-accent/25 mx-auto mb-4">
            <Sparkles className="h-3 w-3" aria-hidden /> Knowledge Map v2 · release estático
          </p>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight mb-4">
            IT Knowledge Map
          </h1>
          <p className="text-muted max-w-2xl mx-auto leading-relaxed">
            {formatCount(counts.concepts)} conceptos de una carrera IT, conectados por{' '}
            {formatCount(counts.relations)} relaciones con su explicación. Explorá el grafo,
            leé las fichas y recorré el journey de cómo se construyó este mapa.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-3 mt-7">
            <Link to="/graph" className="btn-primary !px-5 !py-2.5">
              <Network className="h-4 w-4" aria-hidden /> Explorar el grafo
            </Link>
            <Link to="/kb" className="btn-ghost !px-5 !py-2.5">
              <BookOpen className="h-4 w-4" aria-hidden /> Knowledge Base
            </Link>
          </div>
        </motion.div>
      </section>

      {/* Métricas */}
      <section aria-label="Métricas del release" className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-12">
        <Stat value={counts.concepts} label="Conceptos" delay={0.05} format={formatCount} />
        <Stat value={counts.relations} label="Relaciones" delay={0.1} format={formatCount} />
        <Stat value={counts.areas} label="Áreas" delay={0.15} format={formatCount} />
        <Stat value={counts.chunks} label="Fragmentos indexados" delay={0.2} format={formatCount} />
      </section>

      {/* Áreas */}
      <section aria-label="Áreas de conocimiento" className="mb-12">
        <div className="flex items-baseline justify-between mb-4">
          <h2 className="text-xl font-semibold">Áreas de conocimiento</h2>
          <Link to="/kb" className="text-sm text-accent hover:underline underline-offset-2">Ver todos los conceptos</Link>
        </div>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {areas.map((a, i) => <AreaCard key={a.uid} area={a} index={i} />)}
        </div>
      </section>

      {/* Cómo leer el mapa */}
      <section aria-label="Cómo leer este mapa" className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Cómo leer este mapa</h2>
        <div className="grid gap-3 md:grid-cols-3">
          <div className="panel p-5">
            <BookOpen className="h-5 w-5 text-accent mb-2.5" aria-hidden />
            <h3 className="font-semibold text-sm mb-1.5">Fichas con 10 secciones</h3>
            <p className="text-xs text-muted leading-relaxed">
              Cada concepto tiene objetivo, ideas clave, cómo funciona, ejemplo mínimo,
              errores comunes y más. Navegá por área o buscá con <kbd className="border border-line/70 rounded px-1">Ctrl K</kbd>.
            </p>
          </div>
          <div className="panel p-5">
            <Quote className="h-5 w-5 text-accent mb-2.5" aria-hidden />
            <h3 className="font-semibold text-sm mb-1.5">Relaciones explicadas</h3>
            <p className="text-xs text-muted leading-relaxed">
              Los links entre conceptos vienen del autor del vault y se muestran con su
              explicación citada (<em>quoted</em>). Nada se inventa: lo no documentado se etiqueta.
            </p>
          </div>
          <div className="panel p-5">
            <AlertTriangle className="h-5 w-5 text-amber-400 mb-2.5" aria-hidden />
            <h3 className="font-semibold text-sm mb-1.5">Integridad visible</h3>
            <p className="text-xs text-muted leading-relaxed">
              Las afirmaciones sin fuente llevan marca <em>sin verificar</em>. El release es
              inmutable y su hash se verifica contra el vault original.
            </p>
          </div>
        </div>
      </section>

      <footer className="text-center text-xs text-faint pt-4 border-t border-line/40">
        Release <span className="font-mono">{manifest.release_id}</span> · {formatCount(bootstrap.concepts.length)} fichas ·
        sitio estático sin backend · schema v{manifest.schema_version}
      </footer>
    </div>
  );
}