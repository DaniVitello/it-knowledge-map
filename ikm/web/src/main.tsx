import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MotionConfig } from 'framer-motion';
import App from './App';
import { ReleaseProvider } from './lib/release';
import { ErrorBoundary } from './components/ui';
import './styles/index.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // El release es inmutable: no refetch, sin reintentos agresivos.
      staleTime: Infinity,
      gcTime: 1000 * 60 * 30,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <MotionConfig reducedMotion="user">
          <BrowserRouter>
            <ReleaseProvider>
              <App />
            </ReleaseProvider>
          </BrowserRouter>
        </MotionConfig>
      </QueryClientProvider>
    </ErrorBoundary>
  </React.StrictMode>,
);