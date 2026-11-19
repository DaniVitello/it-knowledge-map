import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Privacy from '../routes/Privacy';
import NotFound from '../routes/NotFound';
import JourneyRecord from '../routes/JourneyRecord';

describe('vistas estáticas sin contexto de release', () => {
  it('Privacy renderiza las secciones clave', () => {
    render(<MemoryRouter><Privacy /></MemoryRouter>);
    expect(screen.getByText('Sin cuentas, sin tracking')).toBeInTheDocument();
    expect(screen.getByText(/IndexedDB/)).toBeInTheDocument();
  });

  it('NotFound ofrece volver al inicio', () => {
    render(<MemoryRouter><NotFound /></MemoryRouter>);
    expect(screen.getByText('Esta ruta no existe')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Volver al inicio' })).toHaveAttribute('href', '/');
  });

  it('JourneyRecord no inventa contenido para un uid inexistente', () => {
    render(
      <MemoryRouter initialEntries={['/journey/r/j_x/nope']}>
        <JourneyRecord />
      </MemoryRouter>,
    );
    expect(screen.getByText('Registro no disponible')).toBeInTheDocument();
  });
});