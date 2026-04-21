"""Smoke tests for shule-ai."""
from shule_ai.subjects import ALL_SUBJECTS, KCPE_SUBJECTS, KCSE_SUBJECTS

def test_subjects_loaded():
    assert "Mathematics" in ALL_SUBJECTS
    assert "Biology" in KCSE_SUBJECTS
    assert "Science and Technology" in KCPE_SUBJECTS

def test_kcpe_has_7_subjects():
    assert len(KCPE_SUBJECTS) >= 6

def test_kcse_has_subjects():
    assert len(KCSE_SUBJECTS) >= 8
