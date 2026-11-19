# -*- coding: utf-8 -*-
"""BM25 sobre los chunks (L3, capa 16)."""
from __future__ import annotations

import math
from typing import Any, Dict, List



def _tokenizar(texto: str) -> List[str]:
    import re
    return re.findall(r"\w+", (texto or "").lower())


class BM25Index:
    """Indice BM25 sobre una lista de chunks."""

    def __init__(self, chunks: List[Any]):
        self.chunks = chunks
        self.doc_tokens: List[List[str]] = []
        self.doc_lengths: List[int] = []
        self.avg_dl: float = 0.0
        self.idf: Dict[str, float] = {}
        self._build()

    def _build(self) -> None:
        for ch in self.chunks:
            texto = getattr(ch, "text", None) or (ch.get("text") if isinstance(ch, dict) else "") or ""
            toks = _tokenizar(texto)
            self.doc_tokens.append(toks)
            self.doc_lengths.append(len(toks))

        n = len(self.doc_tokens)
        if n == 0:
            return
        self.avg_dl = sum(self.doc_lengths) / n

        # Document frequency
        df: Dict[str, int] = {}
        for toks in self.doc_tokens:
            for t in set(toks):
                df[t] = df.get(t, 0) + 1

        # IDF
        for t, d in df.items():
            self.idf[t] = math.log((n - d + 0.5) / (d + 0.5) + 1)

    def score(self, query: str, doc_index: int) -> float:
        """Calcula el score BM25 de un documento para una query."""
        if doc_index >= len(self.doc_tokens):
            return 0.0
        k1 = 1.5
        b = 0.75
        toks = self.doc_tokens[doc_index]
        dl = self.doc_lengths[doc_index]
        tf_map: Dict[str, int] = {}
        for t in toks:
            tf_map[t] = tf_map.get(t, 0) + 1

        q_tokens = _tokenizar(query)
        score = 0.0
        for qt in q_tokens:
            if qt not in self.idf:
                continue
            tf = tf_map.get(qt, 0)
            idf = self.idf[qt]
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * (dl / self.avg_dl)) if self.avg_dl > 0 else 1
            score += idf * (numerator / denominator)
        return score

    def buscar(self, query: str, top_k: int = 20) -> List[Dict[str, Any]]:
        """Devuelve los top_k chunks por BM25."""
        scores = []
        for i in range(len(self.chunks)):
            s = self.score(query, i)
            if s > 0:
                scores.append((s, i))
        scores.sort(key=lambda x: -x[0])
        result = []
        for s, i in scores[:top_k]:
            ch = self.chunks[i]
            result.append({
                "chunk": ch,
                "score": s,
                "index": i,
            })
        return result


def buscar_bm25(pregunta: str, chunks: List[Any], top_k: int = 20) -> List[Any]:
    """Funcion de conveniencia: busca en chunks por BM25."""
    index = BM25Index(chunks)
    return index.buscar(pregunta, top_k)


