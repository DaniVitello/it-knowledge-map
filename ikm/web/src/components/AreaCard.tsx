/** Tarjeta de área: color propio, conteo, framing y roles profesionales. */
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import type { AreaInfo } from '../lib/types';
import { areaColor, areaColorAlpha } from '../lib/format';

export default function AreaCard({ area, index = 0 }: { area: AreaInfo; index?: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: Math.min(index * 0.04, 0.4) }}
    >
      <Link
        to={`/kb/${area.uid}`}
        className="panel block p-4 h-full hover:border-line transition-colors group"
        style={{ boxShadow: `inset 0 1px 0 ${areaColorAlpha(area.uid, 0.25)}` }}
      >
        <div className="flex items-center gap-2.5 mb-2">
          <span
            aria-hidden
            className="h-8 w-8 rounded-lg flex items-center justify-center text-sm font-bold"
            style={{ backgroundColor: areaColorAlpha(area.uid, 0.16), color: areaColor(area.uid) }}
          >
            {String(area.order).padStart(2, '0')}
          </span>
          <div className="min-w-0">
            <h3 className="font-semibold text-sm leading-tight truncate group-hover:text-accent transition-colors">
              {area.name}
            </h3>
            <p className="text-xs text-faint">{area.count} conceptos</p>
          </div>
          <ArrowRight className="h-4 w-4 ml-auto text-faint group-hover:text-accent group-hover:translate-x-0.5 transition-all" aria-hidden />
        </div>
        {area.context_framing && (
          <p className="text-xs text-muted leading-relaxed line-clamp-2">{area.context_framing}</p>
        )}
        {area.professional_roles.length > 0 && (
          <p className="mt-2 text-[11px] text-faint truncate">{area.professional_roles.join(' · ')}</p>
        )}
      </Link>
    </motion.div>
  );
}