/** Shell de la app: sidebar de áreas, topbar con búsqueda global (Ctrl+K),
 * transiciones por ruta y navegación móvil. Accesible por teclado.
 */
import { useEffect, useState } from 'react';
import { NavLink, Outlet, useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { BookOpen, Home, Menu, MessageSquare, Moon, Network, Route, Search, Sun, X } from 'lucide-react';
import { useRelease } from '../lib/release';
import { ExplorationProvider } from '../lib/useExploration';
import { useTheme } from '../lib/theme';
import { areaColor } from '../lib/format';
import CommandPalette from './CommandPalette';

const NAV = [
  { to: '/', label: 'Inicio', icon: Home, end: true },
  { to: '/graph', label: 'Grafo', icon: Network },
  { to: '/kb', label: 'Knowledge Base', icon: BookOpen },
  { to: '/journey', label: 'Journey', icon: Route },
  { to: '/chat', label: 'Chat', icon: MessageSquare },
];

function navClass({ isActive }: { isActive: boolean }): string {
  return `flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
    isActive ? 'bg-accent/15 text-accent' : 'text-muted hover:text-ink hover:bg-raised/70'
  }`;
}

function SidebarContent({ onNavigate }: { onNavigate?: () => void }) {
  const { areas, manifest } = useRelease();
  return (
    <div className="flex flex-col h-full">
      <NavLink to="/" className="flex items-center gap-2.5 px-4 pt-5 pb-4" onClick={onNavigate}>
        <span className="h-9 w-9 rounded-xl bg-gradient-to-br from-accent to-violet-500 flex items-center justify-center shadow-glow">
          <Network className="h-5 w-5 text-white" aria-hidden />
        </span>
        <span>
          <span className="block font-semibold leading-tight">IT Knowledge Map</span>
          <span className="block text-[11px] text-faint">255 conceptos · v2</span>
        </span>
      </NavLink>

      <nav aria-label="Principal" className="px-3 space-y-0.5">
        {NAV.map(({ to, label, icon: Icon, end }) => (
          <NavLink key={to} to={to} end={end} className={navClass} onClick={onNavigate}>
            <Icon className="h-4 w-4" aria-hidden /> {label}
          </NavLink>
        ))}
      </nav>

      <div className="mt-5 px-3 flex-1 overflow-y-auto pb-4">
        <p className="px-3 mb-1.5 text-[11px] font-semibold uppercase tracking-wider text-faint">Áreas</p>
        <ul className="space-y-0.5">
          {areas.map((a) => (
            <li key={a.uid}>
              <NavLink to={`/kb/${a.uid}`} className={navClass} onClick={onNavigate} title={a.name}>
                <span aria-hidden className="h-2 w-2 rounded-full shrink-0" style={{ backgroundColor: areaColor(a.uid) }} />
                <span className="truncate">{a.name}</span>
                <span className="ml-auto text-xs text-faint tabular-nums">{a.count}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </div>

      <div className="px-4 py-3 border-t border-line/50 text-[11px] text-faint space-y-1">
        <p className="font-mono truncate" title={manifest.release_id}>release {manifest.release_id}</p>
        <NavLink to="/privacy" className="hover:text-muted underline-offset-2 hover:underline" onClick={onNavigate}>
          Privacidad
        </NavLink>
      </div>
    </div>
  );
}

function MobileTabBar() {
  const tabs = NAV.filter((n) => ['/', '/graph', '/kb', '/chat'].includes(n.to));
  return (
    <nav aria-label="Navegación móvil" className="lg:hidden fixed bottom-0 inset-x-0 z-40 border-t border-line/60 bg-surface/95 backdrop-blur flex">
      {tabs.map(({ to, label, icon: Icon, end }) => (
        <NavLink
          key={to}
          to={to}
          end={end}
          className={({ isActive }) =>
            `flex-1 flex flex-col items-center gap-0.5 py-2 text-[10px] font-medium ${isActive ? 'text-accent' : 'text-muted'}`
          }
        >
          <Icon className="h-5 w-5" aria-hidden />
          {label === 'Knowledge Base' ? 'KB' : label}
        </NavLink>
      ))}
    </nav>
  );
}

function ShellInner() {
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [mobileNav, setMobileNav] = useState(false);
  const { theme, toggle } = useTheme();
  const location = useLocation();

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setPaletteOpen((o) => !o);
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  useEffect(() => {
    setMobileNav(false);
    window.scrollTo({ top: 0 });
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex">
      <a href="#contenido" className="sr-only focus:not-sr-only focus:absolute focus:z-[100] focus:top-2 focus:left-2 btn-primary">
        Saltar al contenido
      </a>

      <aside className="hidden lg:flex w-64 shrink-0 flex-col border-r border-line/50 bg-surface/50 sticky top-0 h-screen">
        <SidebarContent />
      </aside>

      <AnimatePresence>
        {mobileNav && (
          <>
            <motion.div
              className="fixed inset-0 z-40 bg-black/50 lg:hidden"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              onClick={() => setMobileNav(false)}
              aria-hidden
            />
            <motion.aside
              className="fixed inset-y-0 left-0 z-50 w-72 bg-surface border-r border-line/60 lg:hidden"
              initial={{ x: '-100%' }} animate={{ x: 0 }} exit={{ x: '-100%' }}
              transition={{ type: 'spring', damping: 28, stiffness: 300 }}
              aria-label="Menú de navegación"
            >
              <button
                className="absolute top-3 right-3 btn-ghost !p-1.5"
                onClick={() => setMobileNav(false)}
                aria-label="Cerrar menú"
              >
                <X className="h-4 w-4" />
              </button>
              <SidebarContent onNavigate={() => setMobileNav(false)} />
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      <div className="flex-1 flex flex-col min-w-0">
        <header className="sticky top-0 z-30 border-b border-line/50 bg-base/80 backdrop-blur-md">
          <div className="flex items-center gap-2 px-4 h-14">
            <button className="btn-ghost !p-2 lg:hidden" onClick={() => setMobileNav(true)} aria-label="Abrir menú">
              <Menu className="h-4 w-4" />
            </button>
            <div className="flex-1" />
            <button
              className="btn-ghost !py-1.5 text-muted min-w-[180px] justify-start"
              onClick={() => setPaletteOpen(true)}
              aria-label="Buscar conceptos (Ctrl+K)"
            >
              <Search className="h-4 w-4" aria-hidden />
              <span className="text-sm">Buscar…</span>
              <kbd className="ml-auto hidden sm:inline text-[10px] border border-line/70 rounded px-1.5 py-0.5 text-faint">Ctrl K</kbd>
            </button>
            <button
              className="btn-ghost !p-2"
              onClick={toggle}
              aria-label={theme === 'dark' ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro'}
            >
              {theme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </button>
          </div>
        </header>

        <main id="contenido" className="flex-1 min-w-0 pb-16 lg:pb-0">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.18, ease: 'easeOut' }}
            >
              <Outlet />
            </motion.div>
          </AnimatePresence>
        </main>
      </div>

      <MobileTabBar />
      <CommandPalette open={paletteOpen} onClose={() => setPaletteOpen(false)} />
    </div>
  );
}

export default function Shell() {
  return (
    <ExplorationProvider>
      <ShellInner />
    </ExplorationProvider>
  );
}