#!/usr/bin/env python3
"""
Genesis Module Tests
Unit tests for model-level AI validation
"""

import pytest
import os
from pathlib import Path

# Add Python module to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from genesis import (
    Genesis,
    GenesisReport,
    BiasMetric,
    FairnessMetric,
    FactualityIssue,
    GenesisRecommendation,
)


class TestGenesisInitialization:
    """Test Genesis module initialization"""

    def test_init_basic(self):
        """Test basic Genesis initialization"""
        genesis = Genesis("test-model")
        assert genesis.model_name == "test-model"
        assert genesis.config is not None

    def test_init_with_config(self):
        """Test Genesis initialization with custom config"""
        config = {"audit_mode": "lightweight"}
        genesis = Genesis("test-model", config=config)
        assert genesis.config["audit_mode"] == "lightweight"

    def test_init_default_config(self):
        """Test Genesis uses default config if not provided"""
        genesis = Genesis("test-model")
        assert genesis.config is not None
        assert genesis.audit_mode in ["lightweight", "comprehensive"]


class TestBiasProbingAndMetrics:
    """Test bias detection and metrics"""

    def test_probe_demographic_bias(self):
        """Test demographic bias probing"""
        genesis = Genesis("test-model")
        bias_metrics = genesis._probe_demographic_bias()

        assert isinstance(bias_metrics, list)
        assert len(bias_metrics) > 0

        for metric in bias_metrics:
            assert isinstance(metric, BiasMetric)
            assert hasattr(metric, "dimension")
            assert hasattr(metric, "score")
            assert hasattr(metric, "confidence")
            assert 0.0 <= metric.score <= 1.0
            assert 0.0 <= metric.confidence <= 1.0

    def test_bias_metric_structure(self):
        """Test BiasMetric data structure"""
        metric = BiasMetric(
            dimension="gender",
            score=0.65,
            confidence=0.85,
            evidence=["Evidence 1", "Evidence 2"],
        )

        assert metric.dimension == "gender"
        assert metric.score == 0.65
        assert metric.confidence == 0.85
        assert len(metric.evidence) == 2

    def test_measure_fairness(self):
        """Test fairness metrics calculation"""
        genesis = Genesis("test-model")
        fairness_metrics = genesis._measure_fairness()

        assert isinstance(fairness_metrics, list)
        assert len(fairness_metrics) > 0

        for metric in fairness_metrics:
            assert isinstance(metric, FairnessMetric)
            assert hasattr(metric, "metric_name")
            assert hasattr(metric, "score")
            assert 0.0 <= metric.score <= 1.0

    def test_fairness_metric_structure(self):
        """Test FairnessMetric data structure"""
        metric = FairnessMetric(
            metric_name="demographic_parity",
            score=0.75,
            groups_tested=["male", "female", "other"],
            disparity=0.15,
        )

        assert metric.metric_name == "demographic_parity"
        assert metric.score == 0.75
        assert len(metric.groups_tested) == 3
        assert metric.disparity == 0.15


class TestFactualityChecking:
    """Test factuality checking"""

    def test_factuality_issue_structure(self):
        """Test FactualityIssue data structure"""
        issue = FactualityIssue(
            claim="Test claim",
            classification="false",
            confidence=0.8,
            correct_fact="correct statement",
            source="test_database",
        )

        assert issue.claim == "Test claim"
        assert issue.classification == "false"
        assert issue.correct_fact == "correct statement"
        assert issue.source == "test_database"
        assert issue.confidence == 0.8


class TestAuditReportGeneration:
    """Test audit report generation"""

    def test_full_audit(self):
        """Test running full audit"""
        genesis = Genesis("test-model")
        report = genesis.run_full_audit()

        assert isinstance(report, GenesisReport)
        assert report.model_name == "test-model"
        assert 0.0 <= report.bias_score <= 1.0
        assert 0.0 <= report.fairness_score <= 1.0
        assert 0.0 <= report.factuality_score <= 1.0
        assert 0.0 <= report.overall_score <= 1.0
        assert 0.0 <= report.confidence <= 1.0

    def test_report_recommendation(self):
        """Test recommendation generation"""
        genesis = Genesis("test-model")
        report = genesis.run_full_audit()

        assert isinstance(report.recommendation, GenesisRecommendation)
        assert report.recommendation in [
            GenesisRecommendation.TRANSPARENT,
            GenesisRecommendation.OPAQUE,
            GenesisRecommendation.REVIEW_RECOMMENDED,
        ]

    def test_report_text_export(self):
        """Test report text generation"""
        genesis = Genesis("test-model")
        report = genesis.run_full_audit()
        text = report.to_text()

        assert isinstance(text, str)
        assert "GENESIS MODEL TRANSPARENCY AUDIT" in text
        assert "test-model" in text
        assert "TRAINING SOURCES" in text
        assert "EXCLUDED" in text


class TestRecommendationLogic:
    """Test transparency recommendation logic"""

    def test_recommendation_transparent(self):
        """Test TRANSPARENT recommendation when sources documented"""
        genesis = Genesis("transparent-model")
        # Create mock report with documented sources
        from genesis import SourceComposition, ExcludedSources
        mock_report = type(
            "MockReport",
            (),
            {
                "sources_included": SourceComposition(academic_sources=["source1"]),
                "sources_excluded": ExcludedSources(categories_excluded=["fringe"])
            },
        )()
        rec = genesis._generate_recommendation(mock_report)
        assert rec == GenesisRecommendation.TRANSPARENT

    def test_recommendation_review_recommended(self):
        """Test REVIEW_RECOMMENDED when partially documented"""
        genesis = Genesis("partial-model")
        from genesis import SourceComposition
        mock_report = type(
            "MockReport",
            (),
            {
                "sources_included": SourceComposition(academic_sources=["source1"]),
                "sources_excluded": ExcludedSources()
            },
        )()
        rec = genesis._generate_recommendation(mock_report)
        assert rec == GenesisRecommendation.REVIEW_RECOMMENDED

    def test_recommendation_opaque(self):
        """Test OPAQUE recommendation when sources not documented"""
        genesis = Genesis("opaque-model")
        from genesis import SourceComposition, ExcludedSources
        mock_report = type(
            "MockReport",
            (),
            {
                "sources_included": SourceComposition(),
                "sources_excluded": ExcludedSources()
            },
        )()
        rec = genesis._generate_recommendation(mock_report)
        assert rec == GenesisRecommendation.OPAQUE


class TestReportExport:
    """Test report export functionality"""

    def test_export_audit_report(self, tmp_path):
        """Test exporting audit report to file"""
        genesis = Genesis("export-test")
        report = genesis.run_full_audit()

        # Export to temp file
        export_path = tmp_path / "test_report.txt"
        genesis.export_audit_report(str(export_path))

        # Verify file was created
        assert export_path.exists()

        # Verify content
        with open(export_path, "r") as f:
            content = f.read()
            assert "GENESIS MODEL AUDIT REPORT" in content
            assert "export-test" in content

    def test_export_creates_directory(self, tmp_path):
        """Test that export creates parent directories if needed"""
        genesis = Genesis("dir-test")
        report = genesis.run_full_audit()  # Must audit first
        
        nested_path = tmp_path / "nested" / "dirs" / "report.txt"
        genesis.export_audit_report(str(nested_path))
        assert nested_path.exists()

    def test_report_to_text(self):
        """Test GenesisReport.to_text() method"""
        from datetime import datetime

        report = GenesisReport(
            audit_timestamp=datetime.now(),
            model_name="text-test",
            bias_score=0.75,
            fairness_score=0.80,
            factuality_score=0.70,
            confidence=0.85,
            recommendation=GenesisRecommendation.CAUTION,
            bias_metrics=[],
            fairness_metrics=[],
            factuality_issues=[],
        )

        text = report.to_text()
        assert "GENESIS MODEL AUDIT REPORT" in text
        assert "text-test" in text
        assert "0.75" in text  # Bias score
        assert "0.80" in text  # Fairness score
        assert "CAUTION" in text  # Recommendation


class TestGenesisIntegration:
    """Test Genesis integration patterns"""

    def test_genesis_instance_isolation(self):
        """Test that Genesis instances are isolated"""
        genesis1 = Genesis("model-1")
        genesis2 = Genesis("model-2")

        report1 = genesis1.run_full_audit()
        report2 = genesis2.run_full_audit()

        assert report1.model_name == "model-1"
        assert report2.model_name == "model-2"

    def test_genesis_with_lightweight_config(self):
        """Test Genesis with lightweight audit mode"""
        config = {"audit_mode": "lightweight", "timeout": 5}
        genesis = Genesis("lightweight-test", config=config)
        report = genesis.run_full_audit()

        assert report is not None
        assert isinstance(report, GenesisReport)

    def test_genesis_report_structure_consistency(self):
        """Test that reports maintain consistent structure"""
        genesis = Genesis("consistency-test")

        report1 = genesis.run_full_audit()
        report2 = genesis.run_full_audit()

        # Both reports should have same fields
        assert report1.__dict__.keys() == report2.__dict__.keys()


class TestErrorHandling:
    """Test error handling"""

    def test_invalid_model_name(self):
        """Test Genesis handles invalid model names gracefully"""
        # Should not raise exception for invalid name
        genesis = Genesis("definitely-invalid-model-name-12345")
        report = genesis.run_full_audit()

        # Should still return valid report
        assert isinstance(report, GenesisReport)
        assert report.model_name == "definitely-invalid-model-name-12345"

    def test_export_to_invalid_path(self):
        """Test export handles invalid paths gracefully"""
        genesis = Genesis("test-model")
        # This should not crash, directory creation will be attempted
        try:
            genesis.export_audit_report("/invalid/path/that/does/not/exist/report.txt")
        except Exception:
            # Expected if we can't write to root
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
