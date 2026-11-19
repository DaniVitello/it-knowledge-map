import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import Shell from './components/Shell';
import { PageSkeleton } from './components/ui';
import Home from './routes/Home';
import KbIndex from './routes/KbIndex';
import KbArea from './routes/KbArea';
import Privacy from './routes/Privacy';
import NotFound from './routes/NotFound';

// Carga diferida: grafo (canvas), ficha (markdown) y chat no pesan en el arranque (§15.5).
const Concept = lazy(() => import('./routes/Concept'));
const GraphPage = lazy(() => import('./routes/GraphPage'));
const Chat = lazy(() => import('./routes/Chat'));
const Journey = lazy(() => import('./routes/Journey'));
const JourneyRecord = lazy(() => import('./routes/JourneyRecord'));
const Tours = lazy(() => import('./routes/Tours'));

export default function App() {
  return (
    <Routes>
      <Route element={<Shell />}>
        <Route index element={<Home />} />
        <Route path="kb" element={<KbIndex />} />
        <Route path="kb/:area" element={<KbArea />} />
        <Route path="kb/c/:uid/:slug" element={<Suspense fallback={<PageSkeleton />}><Concept /></Suspense>} />
        <Route path="graph" element={<Suspense fallback={<PageSkeleton />}><GraphPage /></Suspense>} />
        <Route path="graph/view/:uid" element={<Suspense fallback={<PageSkeleton />}><GraphPage /></Suspense>} />
        <Route path="journey" element={<Suspense fallback={<PageSkeleton />}><Journey /></Suspense>} />
        <Route path="journey/r/:uid/:slug" element={<Suspense fallback={<PageSkeleton />}><JourneyRecord /></Suspense>} />
        <Route path="tours/:id" element={<Suspense fallback={<PageSkeleton />}><Tours /></Suspense>} />
        <Route path="chat" element={<Suspense fallback={<PageSkeleton />}><Chat /></Suspense>} />
        <Route path="privacy" element={<Privacy />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}