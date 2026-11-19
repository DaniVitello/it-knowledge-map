// Sincroniza el release estático más reciente hacia web/public/release/.
// El frontend navegable depende SOLO de estos archivos (Entrega 1, sin backend).
// Uso: npm run sync:release  (o node scripts/sync-release.mjs [release-id])
import { cpSync, mkdirSync, readFileSync, existsSync, rmSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const webRoot = resolve(here, '..');
const releasesDir = resolve(webRoot, '../workdir/releases');
const dest = join(webRoot, 'public', 'release');

const wanted = process.argv[2];
let releaseId = wanted;
if (!releaseId) {
  const latestPath = join(releasesDir, 'latest.json');
  if (!existsSync(latestPath)) {
    console.error('No existe latest.json. Corré el release build primero (py -m ikm.content.cli release build).');
    process.exit(1);
  }
  releaseId = JSON.parse(readFileSync(latestPath, 'utf-8')).release_id;
}

const src = join(releasesDir, releaseId);
if (!existsSync(join(src, 'manifest.json'))) {
  console.error(`Release ${releaseId} no encontrado en ${src}`);
  process.exit(1);
}

// Copia todo excepto el índice BM25 del backend (pesado, no lo usa el cliente).
mkdirSync(dest, { recursive: true });
const skip = new Set(['lexical-index.json']);
const entries = cpSync(src, dest, {
  recursive: true,
  filter: (s) => !skip.has(s.split(/[\\/]/).pop()),
});
void entries;

const manifest = JSON.parse(readFileSync(join(dest, 'manifest.json'), 'utf-8'));
console.log(`Release ${releaseId} sincronizado -> public/release/`);
console.log(`  conceptos=${manifest.counts.concepts} relaciones=${manifest.counts.relations} chunks=${manifest.counts.chunks} archivos=${manifest.files.length}`);