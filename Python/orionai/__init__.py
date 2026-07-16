"""
OrionAI Python Wrapper
Chuck-Style AI Oversight for Any Industry

Industry-agnostic AI validation, monitoring, and safety system.

Usage:
    >>> from orionai import OrionAI, ValidationResult
    >>> orion = OrionAI()
    >>> report = orion.monitor_ai_decision("ChatBot", "Hello!")
    >>> print(report.result)

Features:
- Core output validation (OrionAI)
- Model-level transparency (Genesis)
- Music industry validation (Jeffster)
"""

from .orionai import (
    OrionAI,
    ValidationResult,
    ValidationReport,
    CaseyProtocol,
    RingIntel,
    NerdHerd,
    validate_ai_output,
    __version__,
)

from .genesis import (
    Genesis,
    GenesisRecommendation,
    GenesisReport,
    BiasMetric,
    FairnessMetric,
    FactualityIssue,
    SourceComposition,
    ExcludedSources,
)

from .jeffster import (
    MusicValidator,
    MusicValidationType,
    MusicRiskLevel,
    MusicValidationReport,
    quick_validate_music,
)

# Package metadata
__author__ = "Sam Patchet"
__version__ = "1.0.0"
__all__ = [
    "OrionAI",
    "ValidationResult",
    "ValidationReport",
    "CaseyProtocol",
    "RingIntel",
    "NerdHerd",
    "validate_ai_output",
    "__version__",
]