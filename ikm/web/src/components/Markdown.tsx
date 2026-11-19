/** Markdown seguro de las fichas: react-markdown (sin HTML crudo) + GFM.
 * Los wikilinks [[...]] se resuelven contra el release; los rotos se muestran
 * tachados, nunca como links falsos.
 */
import { useMemo } from 'react';
import { Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { useRelease } from '../lib/release';
import { buildTitleIndex, resolveWikiTarget, wikilinksToMarkdown } from '../lib/wikilinks';

export default function Markdown({ text }: { text: string }) {
  const { bootstrap } = useRelease();
  const titleIndex = useMemo(() => buildTitleIndex(bootstrap.concepts), [bootstrap]);
  const processed = useMemo(() => wikilinksToMarkdown(text || ''), [text]);

  return (
    <div className="prose-ikm">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ href, children }) => {
            if (href?.startsWith('ikm://')) {
              const target = decodeURIComponent(href.slice('ikm://'.length));
              const entry = resolveWikiTarget(target, titleIndex);
              if (entry) {
                return <Link to={`/kb/c/${entry.uid}/${entry.slug}`}>{children}</Link>;
              }
              return (
                <span className="text-faint line-through decoration-dotted" title="Link no resuelto en este release">
                  {children}
                </span>
              );
            }
            return (
              <a href={href} target="_blank" rel="noopener noreferrer">
                {children}
              </a>
            );
          },
        }}
      >
        {processed}
      </ReactMarkdown>
    </div>
  );
}