import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../main'))
"""Tests de round-trip dataclass -> JSON -> dataclass para los contratos de Capa A."""
import json
from models import (
    ConceptMeta, Source, ResearchPlan, Synthesis, ValidationReport,
    WriteResult, ConceptState, Claim, Volatility, to_dict,
)
from state import ConceptStatus


def _roundtrip(obj):
    d = to_dict(obj)
    # serializar a JSON y deserializar
    s = json.dumps(d, ensure_ascii=False)
    data = json.loads(s)
    return data


def test_conceptmeta_roundtrip_has_aliases():
    cm = ConceptMeta(
        id="test-concept", title="Test", area="Software Engineering",
        note_path=__import__("pathlib").Path("C:/tmp/test.md"),
    )
    cm.concept_id = "test-concept"
    cm.path = "C:/tmp/test.md"
    cm.content_hash_outside_ai = "abc123"
    d = _roundtrip(cm)
    assert d["id"] == "test-concept"
    assert d["concept_id"] == "test-concept"
    assert d["path"] == "C:/tmp/test.md"
    assert d["content_hash_outside_ai"] == "abc123"


def test_source_roundtrip():
    s = Source(source_id="s01", url="https://example.com", title="Example",
               domain="example.com", level=1, kept=True,
               evaluation={"authority": 0.9})
    d = _roundtrip(s)
    assert d["source_id"] == "s01"
    assert d["domain"] == "example.com"
    assert d["level"] == 1
    assert d["kept"] is True
    assert d["evaluation"] == {"authority": 0.9}


def test_researchplan_roundtrip():
    rp = ResearchPlan(concept_id="c1", questions_by_dim={"accuracy": ["q1"]},
                     relation_questions=[{"with": "x", "ask": "how?"}],
                     queries=["site:example.com c1"], source_requirements={"min_level1_or_2": 2})
    d = _roundtrip(rp)
    assert d["concept_id"] == "c1"
    assert d["questions_by_dim"] == {"accuracy": ["q1"]}
    assert d["relation_questions"] == [{"with": "x", "ask": "how?"}]


def test_synthesis_claim_roundtrip():
    syn = Synthesis(concept_id="c1", title="T", markdown="# m",
                    claims=[Claim(text="claim1", source_ids=["s01"], unverified=False,
                                 claim_id="cl1", status="verified")],
                    unverified_items=["item1"])
    d = _roundtrip(syn)
    assert d["claims"][0]["text"] == "claim1"
    assert d["claims"][0]["claim_id"] == "cl1"
    assert d["claims"][0]["status"] == "verified"
    assert d["unverified_items"] == ["item1"]


def test_validationreport_roundtrip():
    vr = ValidationReport(concept_id="c1", is_valid=True, score=0.9,
                          blocking_failures=[], verdict="approved")
    d = _roundtrip(vr)
    assert d["concept_id"] == "c1"
    assert d["is_valid"] is True
    assert d["verdict"] == "approved"
    assert d["blocking_failures"] == []


def test_writeresult_roundtrip():
    wr = WriteResult(path=__import__("pathlib").Path("C:/tmp/out.md"),
                     ai_block_hash="hash1", outside_block_hash_before="h2",
                     outside_block_hash_after="h3", verified=True)
    d = _roundtrip(wr)
    assert d["ai_block_hash"] == "hash1"
    assert d["verified"] is True


def test_conceptstate_roundtrip():
    cs = ConceptState(concept_id="c1", status=ConceptStatus.PENDING,
                      failure={"phase": "research", "error": "timeout",
                               "attempts": 2, "retryable": True},
                      retries=2, last_good_state=ConceptStatus.PENDING)
    d = _roundtrip(cs)
    assert d["concept_id"] == "c1"
    assert d["failure"] == {"phase": "research", "error": "timeout",
                            "attempts": 2, "retryable": True}
    assert d["retries"] == 2


def test_validate_artifact_schema():
    from backend import validate_artifact_schema, SchemaError
    # valid
    validate_artifact_schema({"sources": []}, "sources")
    validate_artifact_schema({"concept_id": "c1", "answers": []}, "raw_research")
    # invalid
    try:
        validate_artifact_schema({"foo": "bar"}, "sources")
        assert False, "should raise"
    except (SchemaError, ValueError):
        pass
    # unknown schema: no raise
    validate_artifact_schema({"anything": 1}, "unknown_schema")
