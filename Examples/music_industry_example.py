"""
ORIONAI MUSIC INDUSTRY EXAMPLE
================================
Demonstrates AI validation for music streaming platforms, labels, and rights management.

"Sarah, I'm detecting some very suspicious patterns in this royalty calculation..."

This example showcases:
1. AI-generated music detection
2. Copyright/sample violation checks
3. Lyric content validation
4. Metadata verification
5. Recommendation bias detection
6. Royalty calculation validation

Author: OrionAI Framework
License: MIT
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Python'))

from jeffster import (
    MusicValidator,
    MusicValidationType,
    MusicRiskLevel,
    quick_validate_music
)


def print_header(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_report(report):
    """Pretty print validation report"""
    print(f"Track ID: {report.track_id}")
    print(f"Validation Type: {report.validation_type.value}")
    print(f"Risk Level: {report.risk_level.value.upper()}")
    print(f"Confidence: {report.confidence_score:.2%}")
    print(f"\nIssues Found ({len(report.issues_found)}):")
    for issue in report.issues_found:
        print(f"  - {issue}")
    print(f"\nRecommendations ({len(report.recommendations)}):")
    for rec in report.recommendations:
        print(f"  ✓ {rec}")
    print(f"\nTimestamp: {report.timestamp}")
    print("-" * 70)


def scenario_1_streaming_platform():
    """Scenario 1: Streaming Platform - AI Music Detection"""
    print_header("SCENARIO 1: Streaming Platform - AI-Generated Music Detection")
    print("A streaming service needs to verify if uploaded tracks are AI-generated")
    print("to comply with disclosure requirements and artist agreements.\n")
    
    validator = MusicValidator()
    
    # Test Case 1: Suspicious AI-generated track
    print("[TEST 1] Analyzing track with AI generation indicators...\n")
    
    ai_track_features = {
        'timing_variance': 0.02,  # Very precise timing
        'harmonic_complexity': 0.25,  # Low complexity
        'pattern_repetition': 0.85,  # High repetition
        'pitch_correction_detected': True,
        'pitch_perfection': 0.98  # Unnaturally perfect
    }
    
    report1 = validator.validate_ai_generated_music(
        track_id="TR-2025-001",
        audio_features=ai_track_features,
        claimed_human_created=True
    )
    
    print_report(report1)
    
    # Test Case 2: Likely human-created track
    print("\n[TEST 2] Analyzing track with human performance characteristics...\n")
    
    human_track_features = {
        'timing_variance': 0.15,  # Natural variation
        'harmonic_complexity': 0.72,  # Rich harmonics
        'pattern_repetition': 0.35,  # Varied composition
        'pitch_correction_detected': True,
        'pitch_perfection': 0.75  # Some imperfections
    }
    
    report2 = validator.validate_ai_generated_music(
        track_id="TR-2025-002",
        audio_features=human_track_features,
        claimed_human_created=True
    )
    
    print_report(report2)


def scenario_2_record_label():
    """Scenario 2: Record Label - Copyright & Sample Clearance"""
    print_header("SCENARIO 2: Record Label - Copyright Validation")
    print("A label needs to verify a new track doesn't contain unauthorized")
    print("samples or copyright violations before distribution.\n")
    
    validator = MusicValidator()
    
    # Test Case 1: Track with potential copyright issues
    print("[TEST] Checking for copyright violations...\n")
    
    report = validator.validate_copyright(
        track_id="TR-2025-003",
        audio_fingerprint="a1b2c3d4e5f6g7h8",  # Simulated fingerprint
        melody_data=[60, 62, 64, 65, 67],  # C major scale snippet
        lyrics="Lyrics that reference famous song lines"
    )
    
    print_report(report)


def scenario_3_content_moderation():
    """Scenario 3: Content Moderation - Lyric Validation"""
    print_header("SCENARIO 3: Content Moderation - Lyric Validation")
    print("Platform needs to validate lyric content for explicit material,")
    print("hate speech, and cultural sensitivity before publishing.\n")
    
    validator = MusicValidator()
    
    # Test Case 1: Clean lyrics with potential issues
    print("[TEST 1] Validating lyrics for CLEAN rating...\n")
    
    clean_lyrics = """
    Living my life in the fast lane
    Rolling with my crew, we don't play games
    Nike on my feet, Gucci on my wrist
    Women should stay home, that's on my list
    """
    
    report1 = validator.validate_lyric_content(
        track_id="TR-2025-004",
        lyrics=clean_lyrics,
        target_rating="CLEAN",
        check_bias=True
    )
    
    print_report(report1)
    
    # Test Case 2: Explicit content detection
    print("\n[TEST 2] Detecting explicit content...\n")
    
    explicit_lyrics = """
    This track is too explicit for a family-friendly example
    But it contains profanity like f*ck and sh*t
    """
    
    report2 = validator.validate_lyric_content(
        track_id="TR-2025-005",
        lyrics=explicit_lyrics,
        target_rating="CLEAN",
        check_bias=False
    )
    
    print_report(report2)


def scenario_4_metadata_verification():
    """Scenario 4: Distribution Platform - Metadata Validation"""
    print_header("SCENARIO 4: Distribution Platform - Metadata Verification")
    print("Digital distributor validates track metadata for completeness")
    print("and accuracy before sending to streaming services.\n")
    
    validator = MusicValidator()
    
    # Test Case 1: Incomplete metadata
    print("[TEST 1] Checking metadata with missing fields...\n")
    
    incomplete_metadata = {
        'artist_name': 'The Intersect Band',
        'track_title': 'Morgan\'s Theme',
        # Missing ISRC
        'copyright_year': 2025,
        # Missing rights_holder
        'credits': {
            'primary_artist': 'The Intersect Band',
            'contributors': [
                {'name': 'Producer 1', 'role': 'producer', 'verified': True},
                {'name': 'Engineer 1', 'role': 'engineer', 'verified': False}
            ]
        }
    }
    
    report1 = validator.validate_metadata(
        track_id="TR-2025-006",
        metadata=incomplete_metadata
    )
    
    print_report(report1)
    
    # Test Case 2: Complete and valid metadata
    print("\n[TEST 2] Checking complete metadata...\n")
    
    complete_metadata = {
        'artist_name': 'The Intersect Band',
        'track_title': 'Morgan\'s Theme',
        'isrc': 'US-ABC-25-12345',
        'copyright_year': 2025,
        'rights_holder': 'OrionAI Records',
        'publisher': 'Casey Music Publishing',
        'label': 'Buy More Records',
        'credits': {
            'primary_artist': 'The Intersect Band',
            'contributors': [
                {'name': 'Producer 1', 'role': 'producer', 'verified': True},
                {'name': 'Engineer 1', 'role': 'engineer', 'verified': True}
            ]
        }
    }
    
    report2 = validator.validate_metadata(
        track_id="TR-2025-007",
        metadata=complete_metadata
    )
    
    print_report(report2)


def scenario_5_recommendation_system():
    """Scenario 5: Streaming Service - Recommendation Bias Detection"""
    print_header("SCENARIO 5: Streaming Service - Recommendation Bias")
    print("Streaming platform validates AI recommendation algorithm for")
    print("fairness, diversity, and absence of bias.\n")
    
    validator = MusicValidator()
    
    # Test Case 1: Biased recommendations
    print("[TEST 1] Analyzing recommendations with bias...\n")
    
    biased_recommendations = [
        {'artist': 'Artist 1', 'artist_gender': 'male', 'artist_region': 'US', 
         'label_type': 'major', 'release_year': 2024, 'stream_count': 5000000},
        {'artist': 'Artist 2', 'artist_gender': 'male', 'artist_region': 'US', 
         'label_type': 'major', 'release_year': 2024, 'stream_count': 4500000},
        {'artist': 'Artist 3', 'artist_gender': 'male', 'artist_region': 'US', 
         'label_type': 'major', 'release_year': 2023, 'stream_count': 6000000},
        {'artist': 'Artist 4', 'artist_gender': 'male', 'artist_region': 'US', 
         'label_type': 'major', 'release_year': 2024, 'stream_count': 3500000},
        {'artist': 'Artist 5', 'artist_gender': 'male', 'artist_region': 'US', 
         'label_type': 'major', 'release_year': 2023, 'stream_count': 7000000},
        {'artist': 'Artist 6', 'artist_gender': 'male', 'artist_region': 'UK', 
         'label_type': 'major', 'release_year': 2024, 'stream_count': 4000000},
        {'artist': 'Artist 7', 'artist_gender': 'male', 'artist_region': 'US', 
         'label_type': 'major', 'release_year': 2024, 'stream_count': 5500000},
        {'artist': 'Artist 8', 'artist_gender': 'female', 'artist_region': 'US', 
         'label_type': 'major', 'release_year': 2024, 'stream_count': 3000000},
        {'artist': 'Artist 9', 'artist_gender': 'male', 'artist_region': 'US', 
         'label_type': 'major', 'release_year': 2023, 'stream_count': 6500000},
        {'artist': 'Artist 10', 'artist_gender': 'male', 'artist_region': 'US', 
         'label_type': 'major', 'release_year': 2024, 'stream_count': 4800000}
    ]
    
    report1 = validator.validate_recommendation_bias(
        recommendation_list=biased_recommendations,
        context="discover_weekly"
    )
    
    print_report(report1)
    
    # Test Case 2: Diverse recommendations
    print("\n[TEST 2] Analyzing diverse recommendations...\n")
    
    diverse_recommendations = [
        {'artist': 'Artist A', 'artist_gender': 'female', 'artist_region': 'Brazil', 
         'label_type': 'independent', 'release_year': 2020, 'stream_count': 500000},
        {'artist': 'Artist B', 'artist_gender': 'male', 'artist_region': 'Nigeria', 
         'label_type': 'independent', 'release_year': 2022, 'stream_count': 250000},
        {'artist': 'Artist C', 'artist_gender': 'non_binary', 'artist_region': 'Japan', 
         'label_type': 'major', 'release_year': 2019, 'stream_count': 3000000},
        {'artist': 'Artist D', 'artist_gender': 'female', 'artist_region': 'India', 
         'label_type': 'independent', 'release_year': 2023, 'stream_count': 150000},
        {'artist': 'Artist E', 'artist_gender': 'male', 'artist_region': 'France', 
         'label_type': 'major', 'release_year': 2021, 'stream_count': 2000000},
        {'artist': 'Artist F', 'artist_gender': 'female', 'artist_region': 'South Korea', 
         'label_type': 'major', 'release_year': 2024, 'stream_count': 5000000},
        {'artist': 'Artist G', 'artist_gender': 'group', 'artist_region': 'UK', 
         'label_type': 'independent', 'release_year': 2018, 'stream_count': 800000},
        {'artist': 'Artist H', 'artist_gender': 'male', 'artist_region': 'Jamaica', 
         'label_type': 'independent', 'release_year': 2022, 'stream_count': 400000},
        {'artist': 'Artist I', 'artist_gender': 'female', 'artist_region': 'Mexico', 
         'label_type': 'independent', 'release_year': 2023, 'stream_count': 350000},
        {'artist': 'Artist J', 'artist_gender': 'male', 'artist_region': 'Australia', 
         'label_type': 'major', 'release_year': 2020, 'stream_count': 1500000}
    ]
    
    report2 = validator.validate_recommendation_bias(
        recommendation_list=diverse_recommendations,
        context="release_radar"
    )
    
    print_report(report2)


def scenario_6_royalty_system():
    """Scenario 6: Rights Management - Royalty Calculation Validation"""
    print_header("SCENARIO 6: Rights Management - Royalty Validation")
    print("Rights management organization validates AI-calculated royalty")
    print("splits and ensures all contributors are paid correctly.\n")
    
    validator = MusicValidator()
    
    # Test Case 1: Incorrect royalty calculation
    print("[TEST 1] Detecting royalty calculation error...\n")
    
    expected_splits = {
        'Artist': 0.50,      # 50%
        'Producer': 0.25,    # 25%
        'Songwriter': 0.20,  # 20%
        'Label': 0.05        # 5%
    }
    
    # AI system made calculation errors
    incorrect_royalties = {
        'Artist': 12000.00,      # Should be $10,000 (50% of $20k)
        'Producer': 4500.00,     # Should be $5,000 (25% of $20k)
        'Songwriter': 3000.00,   # Should be $4,000 (20% of $20k)
        # Label payment missing!
    }
    
    report1 = validator.validate_royalty_calculation(
        track_id="TR-2025-008",
        calculated_royalties=incorrect_royalties,
        expected_splits=expected_splits,
        total_revenue=20000.00
    )
    
    print_report(report1)
    
    # Test Case 2: Correct royalty calculation
    print("\n[TEST 2] Verifying correct royalty calculation...\n")
    
    correct_royalties = {
        'Artist': 10000.00,
        'Producer': 5000.00,
        'Songwriter': 4000.00,
        'Label': 1000.00
    }
    
    report2 = validator.validate_royalty_calculation(
        track_id="TR-2025-009",
        calculated_royalties=correct_royalties,
        expected_splits=expected_splits,
        total_revenue=20000.00
    )
    
    print_report(report2)


def scenario_7_quick_validation():
    """Scenario 7: Quick Validation Helper"""
    print_header("SCENARIO 7: Quick Validation API")
    print("Using the quick_validate_music() helper for rapid checks.\n")
    
    # Quick AI music check
    print("[TEST 1] Quick AI music detection...\n")
    
    is_safe, report = quick_validate_music(
        track_id="TR-QUICK-001",
        validation_type="ai_music",
        audio_features={
            'timing_variance': 0.01,
            'harmonic_complexity': 0.20,
            'pattern_repetition': 0.90,
            'pitch_correction_detected': True,
            'pitch_perfection': 0.99
        },
        claimed_human_created=True
    )
    
    print(f"Safe for distribution: {is_safe}")
    print_report(report)
    
    # Quick metadata check
    print("\n[TEST 2] Quick metadata validation...\n")
    
    is_safe2, report2 = quick_validate_music(
        track_id="TR-QUICK-002",
        validation_type="metadata",
        metadata={
            'artist_name': 'Chuck & Sarah',
            'track_title': 'The Intersect',
            'isrc': 'US-XYZ-25-00001',
            'copyright_year': 2025,
            'rights_holder': 'OrionAI Music',
            'publisher': 'Casey Publishing',
            'label': 'Nerd Herd Records'
        }
    )
    
    print(f"Metadata complete: {is_safe2}")
    print_report(report2)


def show_validation_stats():
    """Display validation statistics"""
    print_header("VALIDATION STATISTICS")
    
    validator = MusicValidator()
    
    # Run a few validations
    validator.validate_ai_generated_music("TR-001", {'timing_variance': 0.1}, True)
    validator.validate_copyright("TR-002", "fingerprint123")
    validator.validate_lyric_content("TR-003", "Clean lyrics here", "CLEAN")
    
    stats = validator.get_validation_stats()
    
    print(f"Total Validations: {stats['total_validations']}")
    print(f"Copyright Flags: {stats['copyright_flags']}")
    print(f"Content Violations: {stats['content_violations']}")
    print(f"Bias Detections: {stats['bias_detections']}")


def main():
    """Run all music industry validation scenarios"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  ORIONAI MUSIC INDUSTRY VALIDATION EXAMPLES".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("║" + '  "Guys, I know kung fu... and music industry AI validation."'.center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    try:
        scenario_1_streaming_platform()
        scenario_2_record_label()
        scenario_3_content_moderation()
        scenario_4_metadata_verification()
        scenario_5_recommendation_system()
        scenario_6_royalty_system()
        scenario_7_quick_validation()
        show_validation_stats()
        
        print_header("ALL SCENARIOS COMPLETED")
        print("✓ AI-Generated Music Detection")
        print("✓ Copyright & Sample Validation")
        print("✓ Lyric Content Validation")
        print("✓ Metadata Verification")
        print("✓ Recommendation Bias Detection")
        print("✓ Royalty Calculation Validation")
        print("✓ Quick Validation API")
        print("\nOrionAI Music Industry validation is ready for deployment!")
        print("\nIntegrate with:")
        print("  - Streaming platforms (Spotify, Apple Music, Tidal)")
        print("  - Record labels and distributors")
        print("  - Rights management organizations")
        print("  - Content moderation systems")
        print("  - Royalty calculation engines")
        
    except Exception as e:
        print(f"\n[!] ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
