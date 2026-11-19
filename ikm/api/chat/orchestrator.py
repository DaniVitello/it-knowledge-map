# -*- coding: utf-8 -*-
"""Orquesta la consulta L0-L11 (L3, capa 19)."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ikm.contracts.config import Config
from ikm.contracts.errors import AbortStage
from ikm.api.chat.scope import clasificar_alcance
from ikm.api.limits.quotas import QuotaManager
from ikm.api.limits.budget import BudgetManager
from ikm.api.limits.abuse import AbuseTracker
from ikm.api.retrieval.bm25 import buscar_bm25
from ikm.api.retrieval.entities import enlazar_entidades
from ikm.api.retrieval.graph_expand import expandir_por_grafo
from ikm.api.retrieval.journey_expand import expandir_al_journey
from ikm.api.verify.verifier import verificar
from ikm.api.llm.adapter import LLMAdapter
from ikm.api.llm.prompts import render_p1, PROMPT_VERSION


class ChatOrchestrator:
    """Orquesta el pipeline de consulta L0-L11."""

    def __init__(self, config: Config, release: Any, quota_manager: QuotaManager,
                 budget_manager: BudgetManager, abuse_tracker: AbuseTracker,
                 llm_adapter: Optional[LLMAdapter] = None):
        self.config = config
        self.release = release
        self.quota = quota_manager
        self.budget = budget_manager
        self.abuse = abuse_tracker
        self.llm = llm_adapter
        self._chunks: List[Any] = []

    def set_chunks(self, chunks: List[Any]) -> None:
        self._chunks = chunks

    def procesar_consulta(self, user_id: str, ip: str, message: str,
                          release_id: str) -> Dict[str, Any]:
        """Pipeline L0-L11. Devuelve ChatResponse como dict."""
        # L0: Autenticacion (asumida por el caller)
        # L1: Validacion
        if len(message) > self.config.limites.max_message_chars:
            return self._error_response("message_too_long", 422)
        message = message.strip()
        if not message:
            return self._error_response("empty_message", 422)

        # L2: Limites baratos
        try:
            self.quota.verificar_limites_baratos(user_id, ip, message)
        except Exception as e:
            return self._error_response(str(e), 429, retry_after=getattr(e, "detalle", {}).get("retry_after"))

        # L3: Alcance preliminar
        scope = clasificar_alcance(message, None)
        if scope == "smalltalk":
            return self._smalltalk_response()
        if scope == "out":
            self.abuse.registrar_offtopic(user_id)
            return self._out_of_scope_response()

        # L4: Recuperacion
        entidades = enlazar_entidades(message, self._get_conceptos())
        chunks_recuperados = buscar_bm25(message, self._chunks, top_k=20)
        # Expansion por grafo
        relaciones = self._get_relaciones()
        chunks_expandidos = expandir_por_grafo(entidades, relaciones, self._chunks)
        # (chunks_expandidos se fusionan en el contexto)

        # L5: Reserva de presupuesto
        contexto_tokens = 2200
        estimacion = self.budget.estimar_tokens(message, contexto_tokens)
        try:
            reservation = self.budget.reservar_presupuesto(user_id, estimacion)
        except Exception as e:
            return self._degraded_response(message, chunks_recuperados, str(e))

        # L6: Armado del prompt
        allowed_uids = entidades + [c.get("entity_uid") if isinstance(c, dict) else getattr(c, "entity_uid", "") for c in chunks_recuperados[:5]]
        allowed_uids = list(set(u for u in allowed_uids if u))
        contexto_str = self._armar_contexto(chunks_recuperados, chunks_expandidos)
        prompt = render_p1(contexto_str, allowed_uids, "", message)

        # L7: Llamada al modelo
        if self.llm is None:
            return self._degraded_response(message, chunks_recuperados, "no_llm")
        try:
            llm_response = self.llm.chat_json([{"role": "user", "content": prompt}])
        except Exception as e:
            self.budget.liberar_reserva(reservation)
            return self._degraded_response(message, chunks_recuperados, str(e))

        # L8: Verificacion
        verified = verificar(llm_response, chunks_recuperados, self.release)

        # L9: Composicion
        # (resolver fuentes, filtrar acciones/sugerencias - ya hecho en verificar)

        # L10: Contabilidad
        tokens_reales = llm_response.get("usage", {}).get("total_tokens", estimacion)
        self.budget.contabilizar_uso_real(reservation, tokens_reales)
        self.quota.release_concurrency(user_id)

        # L11: Respuesta
        verified["conversation_id"] = "stub"
        verified["message_id"] = "stub"
        verified["release_id"] = release_id
        verified["limits"] = self.quota and {} or {}
        verified["degraded"] = False
        return verified

    def _get_conceptos(self) -> List[Any]:
        if self.release is None:
            return []
        try:
            return self.release.load_json("concepts/index.json") or []
        except Exception:
            return []

    def _get_relaciones(self) -> List[Any]:
        if self.release is None:
            return []
        try:
            data = self.release.load_json("relations.json")
            if isinstance(data, dict):
                return data.get("relations", [])
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _armar_contexto(self, chunks: List[Any], expandidos: List[Any]) -> str:
        partes = []
        for ch in chunks[:10]:
            texto = getattr(ch, "text", None) or (ch.get("text") if isinstance(ch, dict) else "") or ""
            cid = getattr(ch, "chunk_id", None) or (ch.get("chunk_id") if isinstance(ch, dict) else "") or ""
            clase = getattr(ch, "source_class", None) or (ch.get("source_class") if isinstance(ch, dict) else "A") or "A"
            partes.append(f'<doc id="{cid}" class="{clase}">{texto}</doc>')
        return "\n".join(partes)

    def _error_response(self, reason: str, status: int, retry_after: Any = None) -> Dict[str, Any]:
        return {
            "error": reason,
            "status": status,
            "retry_after": retry_after,
            "degraded": True,
        }

    def _smalltalk_response(self) -> Dict[str, Any]:
        return {
            "blocks": [{"text": "Hola! Soy el asistente de IT Knowledge Map. Preguntame sobre ingenieria de software.", "basis": "general", "sources": []}],
            "scope": {"class": "smalltalk", "offtopic_today": 0},
            "degraded": False,
        }

    def _out_of_scope_response(self) -> Dict[str, Any]:
        return {
            "blocks": [{"text": "Esa consulta esta fuera del alcance de IT Knowledge Map. Preguntame sobre ingenieria de software.", "basis": "general", "sources": []}],
            "scope": {"class": "out", "offtopic_today": 0},
            "degraded": False,
        }

    def _degraded_response(self, message: str, chunks: List[Any], reason: str) -> Dict[str, Any]:
        # Respuesta de recuperacion sin modelo
        pasajes = []
        for ch in chunks[:5]:
            texto = getattr(ch, "text", None) or (ch.get("text") if isinstance(ch, dict) else "") or ""
            pasajes.append(texto[:300])
        return {
            "blocks": [{"text": "\n".join(pasajes) if pasajes else "No hay documentacion disponible.", "basis": "documented", "sources": []}],
            "scope": {"class": "in_project", "offtopic_today": 0},
            "degraded": True,
            "degraded_reason": reason,
        }


def procesar_consulta(payload: Any) -> Any:
    """Funcion de conveniencia (stub)."""
    return {"status": "not_implemented"}
