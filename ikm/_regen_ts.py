# -*- coding: utf-8 -*-
"""Regenera schemas + tipos TS desde los contratos Pydantic."""
from ikm.contracts.generate import regenerar
r = regenerar("ikm/contracts/generated")
print("regenerado:", r["schemas"], "schemas,", r["ts"], "ts")
