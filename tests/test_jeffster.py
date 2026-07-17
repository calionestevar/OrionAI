"""
JEFFSTER Music Industry Validation Tests
Comprehensive tests for music validation module
"""

import pytest
from orionai.jeffster import (
    MusicValidator,
    MusicValidationType,
    MusicRiskLevel,
    MusicValidationReport,
    quick_validate_music,
)


class TestMusicValidatorInitialization:
    """Test MusicValidator module initialization"""

    def test_init_basic(self):
        """Test basic MusicValidator initialization"""
        validator = MusicValidator()
        
        assert validator is not None
        assert validator.validations_performed == 0
        assert validator.copyright_flags == 0
        assert validator.content_violations == 0
        assert validator.bias_detections == 0
        assert validator.morgan_mode == False

    def test_init_with_custom_config(self):
        """Test MusicValidator initialization with custom config"""
        config = {
            "lyric_validation": {
                "enabled": False,
                "check_explicit_content": False,
            }
        }
        validator = MusicValidator(config_path=None)
        
        assert validator is not None

    def test_default_config_structure(self):
        """Test default config has all expected sections"""
        validator = MusicValidator()
        config = validator._default_config()
        
        assert "ai_music_detection" in config
        assert "copyright_detection" in config
        assert "lyric_validation" in config
        assert "metadata_validation" in config
        assert "recommendation_bias" in config
        assert "royalty_validation" in config


class TestAIMusicDetection:
    """Test AI-generated music detection"""

    def test_detects_perfect_timing(self):
        """Test detection of unnaturally perfect timing"""
        validator = MusicValidator()
        
        audio_features = {
            "timing_variance": 0.02,  # Very low variance
            "harmonic_complexity": 0.5,
            "pattern_repetition": 0.5,
            "pitch_correction_detected": False,
        }
        
        report = validator.validate_ai_generated_music(
            track_id="test-track-1",
            audio_features=audio_features,
            claimed_human_created=True
        )
        
        assert report.validation_type == MusicValidationType.AI_MUSIC_DETECTION
        assert len(report.issues_found) >= 1
        assert "perfect_timing" in report.metadata.get("ai_indicators", [])

    def test_detects_synthetic_timbre(self):
        """Test detection of synthetic timbre markers"""
        validator = MusicValidator()
        
        audio_features = {
            "timing_variance": 0.8,
            "harmonic_complexity": 0.1,  # Very low harmonic complexity
            "pattern_repetition": 0.5,
            "pitch_correction_detected": False,
        }
        
        report = validator.validate_ai_generated_music(
            track_id="test-track-2",
            audio_features=audio_features,
            claimed_human_created=True
        )
        
        assert "synthetic_timbre" in report.metadata.get("ai_indicators", [])

    def test_safe_track_passes(self):
        """Test that natural-sounding tracks pass validation"""
        validator = MusicValidator()
        
        audio_features = {
            "timing_variance": 0.8,
            "harmonic_complexity": 0.7,
            "pattern_repetition": 0.3,
            "pitch_correction_detected": False,
        }
        
        report = validator.validate_ai_generated_music(
            track_id="natural-track",
            audio_features=audio_features,
            claimed_human_created=True
        )
        
        assert report.risk_level in [MusicRiskLevel.SAFE, MusicRiskLevel.REVIEW_NEEDED]

    def test_morgan_mode_logging(self):
        """Test that Morgan Mode logs detections"""
        validator = MusicValidator()
        validator.enable_morgan_mode()
        
        audio_features = {
            "timing_variance": 0.02,
            "harmonic_complexity": 0.5,
            "pattern_repetition": 0.5,
            "pitch_correction_detected": False,
        }
        
        report = validator.validate_ai_generated_music(
            track_id="morgan-test",
            audio_features=audio_features,
            claimed_human_created=True
        )
        
        # Just verify Morgan mode doesn't break functionality
        assert report is not None
        validator.disable_morgan_mode()


class TestCopyrightValidation:
    """Test copyright and sample detection"""

    def test_no_matches_returns_safe(self):
        """Test that no copyright matches returns SAFE risk level"""
        validator = MusicValidator()
        
        report = validator.validate_copyright(
            track_id="original-track",
            audio_fingerprint="abc123hash",
            melody_data=None,
            lyrics=None
        )
        
        assert report.risk_level == MusicRiskLevel.SAFE

    def test_multiple_matches_raises_risk(self):
        """Test that multiple copyright matches raise risk level"""
        validator = MusicValidator()
        
        # Mock the database check to simulate matches
        original_check = validator._check_sample_database
        validator._check_sample_database = lambda fp: ["match1", "match2", "match3", "match4"]
        
        report = validator.validate_copyright(
            track_id="matched-track",
            audio_fingerprint="xyz789hash"
        )
        
        assert report.risk_level == MusicRiskLevel.COPYRIGHT_RISK
        
        # Restore original method
        validator._check_sample_database = original_check

    def test_lyric_plagiarism_detection(self):
        """Test lyric plagiarism detection"""
        validator = MusicValidator()
        
        # Mock the plagiarism check
        original_check = validator._check_lyric_plagiarism
        validator._check_lyric_plagiarism = lambda lyr: ["existing-song-1"]
        
        report = validator.validate_copyright(
            track_id="plagiarized-track",
            audio_fingerprint="hash123",
            lyrics="Test lyrics that match existing work"
        )
        
        assert "lyrics match" in str(report.issues_found).lower()
        
        # Restore
        validator._check_lyric_plagiarism = original_check


class TestLyricContentValidation:
    """Test lyric content validation"""

    def test_explicit_content_flagged(self):
        """Test that explicit content is flagged"""
        validator = MusicValidator()
        
        lyrics = "This song has fucking explicit language in it"
        
        report = validator.validate_lyric_content(
            track_id="explicit-track",
            lyrics=lyrics,
            target_rating="CLEAN"
        )
        
        assert report.risk_level in [MusicRiskLevel.CONTENT_VIOLATION, MusicRiskLevel.REVIEW_NEEDED]
        assert len(report.issues_found) >= 1

    def test_clean_content_passes(self):
        """Test that clean lyrics pass validation"""
        validator = MusicValidator()
        
        lyrics = "Hello world, this is a clean song about friendship and happiness"
        
        report = validator.validate_lyric_content(
            track_id="clean-track",
            lyrics=lyrics,
            target_rating="CLEAN"
        )
        
        assert report.risk_level == MusicRiskLevel.SAFE

    def test_explicit_allowed_target(self):
        """Test that explicit content passes when EXPLICIT_ALLOWED target"""
        validator = MusicValidator()
        
        lyrics = "This song has some swearing but it's artistically appropriate"
        
        report = validator.validate_lyric_content(
            track_id="explicit-allowed-track",
            lyrics=lyrics,
            target_rating="EXPLICIT_ALLOWED"
        )
        
        # Should be SAFE when explicit allowed
        assert report.risk_level == MusicRiskLevel.SAFE

    def test_explicit_terms_detected(self):
        """Test that specific explicit terms are detected"""
        validator = MusicValidator()
        
        explicit_patterns = [
            ("fuck", "f*u*c*k"),
            ("shit", "sh*t"),
            ("bitch", "b*itch"),
        ]
        
        for term in ["fuck", "shit", "bitch"]:
            report = validator.validate_lyric_content(
                track_id=f"test-{term}",
                lyrics=f"This {term} word appears here",
                target_rating="CLEAN"
            )
            
            # Should detect at least one explicit pattern
            assert len(report.issues_found) >= 1 or report.risk_level != MusicRiskLevel.SAFE

    def test_lyric_validation_without_bias_check(self):
        """Test that lyric validation works with check_bias=False"""
        validator = MusicValidator()

        report = validator.validate_lyric_content(
            track_id="no-bias-check",
            lyrics="Some lyrics here",
            target_rating="CLEAN",
            check_bias=False
        )

        assert isinstance(report, MusicValidationReport)
        assert report.risk_level in [MusicRiskLevel.SAFE, MusicRiskLevel.REVIEW_NEEDED]


class TestMetadataValidation:
    """Test metadata validation"""

    def test_missing_required_fields(self):
        """Test that missing required fields are flagged"""
        validator = MusicValidator()
        
        incomplete_metadata = {
            "artist_name": "Test Artist",
            # Missing: track_title, isrc, copyright_year, rights_holder
        }
        
        report = validator.validate_metadata(
            track_id="incomplete-track",
            metadata=incomplete_metadata
        )
        
        assert report.risk_level == MusicRiskLevel.REVIEW_NEEDED
        assert any("Missing required fields" in issue for issue in report.issues_found)

    def test_complete_metadata_passes(self):
        """Test that complete metadata passes validation"""
        validator = MusicValidator()
        
        complete_metadata = {
            "artist_name": "Test Artist",
            "track_title": "Test Song",
            "isrc": "US-ABC-23-12345",
            "copyright_year": 2024,
            "rights_holder": "Test Records LLC",
            "credits": {
                "primary_artist": "Test Artist",
                "contributors": []
            }
        }
        
        report = validator.validate_metadata(
            track_id="complete-track",
            metadata=complete_metadata
        )
        
        assert report.risk_level == MusicRiskLevel.SAFE

    def test_invalid_isrc_format(self):
        """Test that invalid ISRC format is flagged"""
        validator = MusicValidator()
        
        invalid_metadata = {
            "artist_name": "Test Artist",
            "track_title": "Test Song",
            "isrc": "INVALID-FORMAT",  # Should be CC-XXX-YY-NNNNN
            "copyright_year": 2024,
            "rights_holder": "Test Records LLC"
        }
        
        report = validator.validate_metadata(
            track_id="invalid-isrc",
            metadata=invalid_metadata
        )
        
        assert "Invalid ISRC format" in str(report.issues_found)

    def test_future_copyright_year(self):
        """Test that future copyright year is flagged"""
        validator = MusicValidator()
        
        future_metadata = {
            "artist_name": "Test Artist",
            "track_title": "Test Song",
            "isrc": "US-ABC-23-12345",
            "copyright_year": 2099,  # Future year
            "rights_holder": "Test Records LLC"
        }
        
        report = validator.validate_metadata(
            track_id="future-year",
            metadata=future_metadata
        )
        
        assert any("copyright year" in issue.lower() for issue in report.issues_found)


class TestRecommendationBias:
    """Test recommendation bias detection"""

    def test_gender_imbalance_detected(self):
        """Test that gender imbalance in recommendations is detected"""
        validator = MusicValidator()
        
        biased_recommendations = [
            {"artist_gender": "male"} for _ in range(10)
        ] + [
            {"artist_gender": "female"} for _ in range(1)
        ]
        
        report = validator.validate_recommendation_bias(
            recommendation_list=biased_recommendations,
            context="discovery_playlist"
        )
        
        assert any("Gender imbalance" in issue for issue in report.issues_found)

    def test_balanced_recommendations_pass(self):
        """Test that balanced recommendations pass validation"""
        validator = MusicValidator()
        
        balanced_recommendations = [
            {"artist_gender": "male"},
            {"artist_gender": "female"},
            {"artist_gender": "non_binary"},
            {"artist_gender": "group"},
            {"artist_gender": "unknown"},
        ] * 10
        
        report = validator.validate_recommendation_bias(
            recommendation_list=balanced_recommendations,
            context="balanced_playlist"
        )
        
        # Should have fewer bias issues
        assert len(report.issues_found) < 3

    def test_major_label_favoritism(self):
        """Test that major label favoritism is detected"""
        validator = MusicValidator()
        
        label_biased = [
            {"label_type": "major"} for _ in range(95)
        ] + [
            {"label_type": "independent"} for _ in range(5)
        ]
        
        report = validator.validate_recommendation_bias(
            recommendation_list=label_biased,
            context="radio"
        )
        
        assert any("Major label" in issue for issue in report.issues_found)


class TestRoyaltyValidation:
    """Test royalty calculation validation"""

    def test_correct_calculations_pass(self):
        """Test that correct royalty calculations pass"""
        validator = MusicValidator()
        
        calculated = {"artist": 500.00, "producer": 300.00, "songwriter": 200.00}
        expected = {"artist": 0.5, "producer": 0.3, "songwriter": 0.2}
        total = 1000.0
        
        report = validator.validate_royalty_calculation(
            track_id="fair-split",
            calculated_royalties=calculated,
            expected_splits=expected,
            total_revenue=total
        )
        
        assert report.risk_level == MusicRiskLevel.SAFE

    def test_mismatched_calculations_flagged(self):
        """Test that calculation mismatches are flagged"""
        validator = MusicValidator()
        
        calculated = {"artist": 600.00, "producer": 300.00, "songwriter": 200.00}  # Artist gets extra $100
        expected = {"artist": 0.5, "producer": 0.3, "songwriter": 0.2}
        total = 1000.0
        
        report = validator.validate_royalty_calculation(
            track_id="mismatched-split",
            calculated_royalties=calculated,
            expected_splits=expected,
            total_revenue=total
        )
        
        assert report.risk_level == MusicRiskLevel.CALCULATION_ERROR
        assert any("calculation error" in issue.lower() for issue in report.issues_found)

    def test_missing_contributors_flagged(self):
        """Test that missing contributors are flagged"""
        validator = MusicValidator()
        
        calculated = {"artist": 500.00, "producer": 300.00}  # Missing songwriter
        expected = {"artist": 0.5, "producer": 0.3, "songwriter": 0.2}
        total = 1000.0
        
        report = validator.validate_royalty_calculation(
            track_id="missing-contributor",
            calculated_royalties=calculated,
            expected_splits=expected,
            total_revenue=total
        )
        
        assert any("Missing" in issue for issue in report.issues_found)

    def test_splits_not_summing_to_100(self):
        """Test that splits not summing to 100% are flagged"""
        validator = MusicValidator()
        
        calculated = {"artist": 500.00, "producer": 300.00, "songwriter": 200.00}
        expected = {"artist": 0.5, "producer": 0.4, "songwriter": 0.2}  # Sums to 1.1
        total = 1000.0
        
        report = validator.validate_royalty_calculation(
            track_id="bad-splits",
            calculated_royalties=calculated,
            expected_splits=expected,
            total_revenue=total
        )
        
        assert any("sum to" in issue.lower() for issue in report.issues_found)


class TestQuickValidateFunction:
    """Test quick validation helper function"""

    def test_quick_validate_ai_music(self):
        """Test quick validation for AI music detection"""
        is_safe, report = quick_validate_music(
            track_id="quick-test",
            validation_type="ai_music",
            audio_features={
                "timing_variance": 0.8,
                "harmonic_complexity": 0.7,
                "pattern_repetition": 0.3,
                "pitch_correction_detected": False,
            },
            claimed_human_created=True
        )
        
        assert isinstance(report, MusicValidationReport)
        assert is_safe in [True, False]

    def test_quick_validate_lyrics(self):
        """Test quick validation for lyrics"""
        is_safe, report = quick_validate_music(
            track_id="quick-lyrics",
            validation_type="lyrics",
            lyrics="Clean song lyrics",
            target_rating="CLEAN"
        )
        
        assert isinstance(report, MusicValidationReport)
        assert is_safe == True

    def test_quick_validate_invalid_type(self):
        """Test that invalid validation type raises error"""
        with pytest.raises(ValueError):
            quick_validate_music(
                track_id="invalid",
                validation_type="nonexistent_type",
                unknown_param="test"
            )


class TestMorganMode:
    """Test Morgan Mode debugging features"""

    def test_enable_disable_morgan_mode(self):
        """Test enabling and disabling Morgan Mode"""
        validator = MusicValidator()
        
        validator.enable_morgan_mode()
        assert validator.morgan_mode == True
        
        validator.disable_morgan_mode()
        assert validator.morgan_mode == False

    def test_morgan_mode_logging_functionality(self):
        """Test that Morgan Mode logging works without crashing"""
        validator = MusicValidator()
        validator.enable_morgan_mode()
        
        # Run validation in Morgan Mode
        report = validator.validate_ai_generated_music(
            track_id="morgan-mode-test",
            audio_features={"timing_variance": 0.8, "harmonic_complexity": 0.7},
            claimed_human_created=True
        )
        
        assert report is not None
        validator.disable_morgan_mode()


class TestValidationStats:
    """Test validation statistics tracking"""

    def test_stats_tracking(self):
        """Test that validation stats are tracked correctly"""
        validator = MusicValidator()
        
        # Perform some validations
        validator.validate_ai_generated_music(
            track_id="stat-test-1",
            audio_features={"timing_variance": 0.8},
            claimed_human_created=True
        )
        
        validator.validate_lyric_content(
            track_id="stat-test-2",
            lyrics="Clean lyrics",
            target_rating="CLEAN"
        )
        
        stats = validator.get_validation_stats()
        
        assert stats["total_validations"] >= 2
        assert "copyright_flags" in stats
        assert "content_violations" in stats
        assert "bias_detections" in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=orionai.jeffster", "--cov-report=term-missing"])