# -*- coding: utf-8 -*-
"""Entidades del servicio: tablas de base de datos (L0.3).

Solo definen contratos. El acceso a datos y las migraciones son L5.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UserStatus(str, Enum):
    active = "active"
    suspended = "suspended"
    deleted = "deleted"


class User(_Base):
    id: str = Field(min_length=1)
    google_sub: str = Field(min_length=1)
    email: str = Field(min_length=1)
    email_verified: bool
    status: UserStatus = UserStatus.active
    created_at: datetime
    last_seen_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class Session(_Base):
    id_hash: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    created_at: datetime
    expires_at: datetime
    last_seen_at: Optional[datetime] = None
    ip_hash: Optional[str] = None
    ua_hash: Optional[str] = None
    revoked_at: Optional[datetime] = None


class WindowKind(str, Enum):
    hour = "hour"
    day = "day"


class UsageWindow(_Base):
    user_id: str = Field(min_length=1)
    window_kind: WindowKind
    window_start: datetime
    requests: int = Field(default=0, ge=0)
    tokens: int = Field(default=0, ge=0)
    offtopic: int = Field(default=0, ge=0)


class GlobalUsage(_Base):
    day: str = Field(min_length=1)
    requests: int = Field(default=0, ge=0)
    tokens: int = Field(default=0, ge=0)
    cost_estimate: float = Field(default=0.0, ge=0)


class Conversation(_Base):
    id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    release_id: str = Field(min_length=1)
    created_at: datetime
    last_message_at: Optional[datetime] = None


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class Message(_Base):
    id: str = Field(min_length=1)
    conversation_id: str = Field(min_length=1)
    role: MessageRole
    text: str = Field(default="")
    blocks: List[Dict[str, Any]] = Field(default_factory=list)
    ui_actions: List[Dict[str, Any]] = Field(default_factory=list)
    scope_class: Optional[str] = None
    tokens_in: int = Field(default=0, ge=0)
    tokens_out: int = Field(default=0, ge=0)
    cached: bool = False
    degraded: bool = False
    retrieval_trace: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    expires_at: Optional[datetime] = None


class AbuseKind(str, Enum):
    rate_limit = "rate_limit"
    offtopic = "offtopic"
    csrf = "csrf"
    auth_failure = "auth_failure"
    manual = "manual"


class AbuseEvent(_Base):
    id: str = Field(min_length=1)
    user_id: Optional[str] = None
    ip_hash: str = Field(min_length=1)
    kind: AbuseKind
    created_at: datetime


class IpWindow(_Base):
    ip_hash: str = Field(min_length=1)
    window_start: datetime
    requests: int = Field(default=0, ge=0)
