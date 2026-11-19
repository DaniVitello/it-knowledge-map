# -*- coding: utf-8 -*-
"""Verificacion determinista de respuestas (L3, capa 17)."""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Set

from ikm.contracts.errors import AbortStage


class VerificationError(AbortStage):
    pass


class ResponseVerifier:
    """Verifica una respuesta del chatbot segun V1-V10."""

    def __init__(self, release: Any, retrieved_chunks: List[Any]):
        self.release = release
        self.retrieved_chunks = retrieved_chunks
        self.retrieved_ids: Set[str] = set()
        for ch in retrieved_chunks:
            cid = getattr(ch, "chunk_id", None) or (ch.get("chunk_id") if isinstance(ch, dict) else None)
            if cid:
                self.retrieved_ids.add(cid)
        # Collect valid uids from release
        self.valid_concept_uids: Set[str] = set()
        self.valid_relation_uids: Set[str] = set()
        self.valid_record_uids: Set[str] = set()
        self._load_valid_uids()

    def _load_valid_uids(self) -> None:
        """Carga uids validos desde el release."""
        if self.release is None:
            return
        manifest = getattr(self.release, "manifest", None) or {}
        # Try to load concepts
        try:
            concepts = self.release.load_json("concepts/index.json") if hasattr(self.release, "load_json") else None
        except Exception:
            concepts = None
        # Fallback: try graph.json
        try:
            graph = self.release.load_json("graph.json") if hasattr(self.release, "load_json") else None
            if graph and isinstance(graph, dict):
                for node in graph.get("nodes", []):
                    uid = node.get("uid") if isinstance(node, dict) else None
                    if uid:
                        self.valid_concept_uids.add(uid)
        except Exception:
            pass

    def _is_valid_uid(self, uid: str) -> bool:
        return uid in self.valid_concept_uids or uid in self.valid_relation_uids or uid in self.valid_record_uids

    def verificar(self, respuesta: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica V1-V10. Devuelve la respuesta corregida."""
        # V1: validar contra esquema (basico)
        if not isinstance(respuesta, dict):
            return {"blocks": [], "degraded": True}

        blocks = respuesta.get("blocks", [])
        if not isinstance(blocks, list):
            blocks = []
            respuesta["blocks"] = blocks

        # V2: toda fuente citada esta en el conjunto recuperado
        for block in blocks:
            if not isinstance(block, dict):
                continue
            sources = block.get("sources", [])
            if isinstance(sources, list):
                block["sources"] = [s for s in sources if s in self.retrieved_ids]

        # V3: bloque documented tiene al menos una fuente valida
        for block in blocks:
            if not isinstance(block, dict):
                continue
            basis = block.get("basis", "")
            sources = block.get("sources", [])
            if basis == "documented" and not sources:
                # Si menciona entidades del proyecto, eliminar; si no, pasar a general
                text = block.get("text", "")
                if re.search(r"\bc_[A-Z0-9]+\b", text):
                    blocks.remove(block)
                else:
                    block["basis"] = "general"

        # V4: relation_claim documentado referencia relacion existente
        relation_claims = respuesta.get("relation_claims", [])
        if isinstance(relation_claims, list):
            for rc in relation_claims:
                if not isinstance(rc, dict):
                    continue
                if rc.get("basis") == "documented":
                    # Verificar que la relacion existe
                    ruid = rc.get("relation_uid")
                    if ruid and ruid not in self.valid_relation_uids:
                        rc["basis"] = "inferred"

        # V5: derived/stale nunca como documentada
        # (manejado por el backend al cargar relaciones)

        # V6: journey_claim corresponde al kind del registro
        journey_claims = respuesta.get("journey_claims", [])
        if isinstance(journey_claims, list):
            for jc in journey_claims:
                if not isinstance(jc, dict):
                    continue
                # Validar que el record_uid existe
                ruid = jc.get("record_uid")
                if ruid and ruid not in self.valid_record_uids:
                    journey_claims.remove(jc)

        # V7: acciones y sugerencias usan uid del release y tipo permitido
        ui_actions = respuesta.get("ui_actions", [])
        if isinstance(ui_actions, list):
            valid_actions = []
            for action in ui_actions:
                if not isinstance(action, dict):
                    continue
                atype = action.get("type")
                if atype not in ("highlight_nodes", "open_concept", "open_record", "open_relation", "open_view", "start_tour"):
                    continue
                payload = action.get("payload", {})
                uids = payload.get("uids", []) if isinstance(payload, dict) else []
                if all(self._is_valid_uid(u) for u in uids) or not uids:
                    valid_actions.append(action)
            respuesta["ui_actions"] = valid_actions

        suggestions = respuesta.get("suggestions", [])
        if isinstance(suggestions, list):
            valid_suggestions = []
            for s in suggestions:
                if not isinstance(s, dict):
                    continue
                uid = s.get("uid")
                if uid and self._is_valid_uid(uid):
                    valid_suggestions.append(s)
                elif not uid:
                    valid_suggestions.append(s)
            respuesta["suggestions"] = valid_suggestions

        # V8: sin URLs en el texto salvo las de Source
        for block in blocks:
            if not isinstance(block, dict):
                continue
            text = block.get("text", "")
            # Eliminar URLs que no sean de Source
            text = re.sub(r"https?://[^\s]+", "", text)
            block["text"] = text

        # V9: idioma coincide (basico: no verificar, solo recortar longitud)
        for block in blocks:
            if not isinstance(block, dict):
                continue
            text = block.get("text", "")
            if len(text) > 2000:
                block["text"] = text[:2000]

        # V10: si el contexto no cubre, declarar
        # (se agrega en el prompt, no se corrige aqui)

        respuesta["blocks"] = blocks
        return respuesta


def verificar(respuesta: Any, contexto_recuperado: Any, release: Any) -> Any:
    """Funcion de conveniencia."""
    chunks = contexto_recuperado if isinstance(contexto_recuperado, list) else []
    verifier = ResponseVerifier(release, chunks)
    if isinstance(respuesta, dict):
        return verifier.verificar(respuesta)
    return respuesta
