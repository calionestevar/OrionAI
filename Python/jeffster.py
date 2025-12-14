"""
JEFFSTER - ORIONAI MUSIC INDUSTRY VALIDATION
==============================================
Music industry AI validation for streaming platforms, labels, and rights management.

"Jeffster is going to rock your world!" - Jeff & Lester

Features:
---------
1. AI-Generated Music Detection & Validation
2. Copyright/Sample Detection
3. Lyric Content Validation (explicit content, bias, cultural sensitivity)
4. Metadata & Rights Verification
5. Recommendation Bias Detection
6. Royalty Calculation Validation
7. Artist Credit Verification

Use Cases:
----------
- Streaming platforms (Spotify, Apple Music, Tidal)
- Record labels and distributors
- Rights management organizations (ASCAP, BMI, SESAC)
- Music production tools with AI features
- Content moderation systems
- Royalty calculation engines

Author: OrionAI Framework
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
from enum import Enum
import re
import json


class MusicValidationType(Enum):
    """Types of music-related AI validations"""
    AI_MUSIC_DETECTION = "ai_music_detection"
    COPYRIGHT_CHECK = "copyright_check"
    LYRIC_CONTENT = "lyric_content"
    METADATA_VALIDATION = "metadata_validation"
    RECOMMENDATION_BIAS = "recommendation_bias"
    ROYALTY_CALCULATION = "royalty_calculation"
    ARTIST_CREDIT = "artist_credit"
    SAMPLE_DETECTION = "sample_detection"


class MusicRiskLevel(Enum):
    """Risk levels for music industry validations"""
    SAFE = "safe"
    REVIEW_NEEDED = "review_needed"
    COPYRIGHT_RISK = "copyright_risk"
    CONTENT_VIOLATION = "content_violation"
    BIAS_DETECTED = "bias_detected"
    CALCULATION_ERROR = "calculation_error"


@dataclass
class MusicValidationReport:
    """Report from music industry AI validation"""
    track_id: str
    validation_type: MusicValidationType
    risk_level: MusicRiskLevel
    issues_found: List[str]
    recommendations: List[str]
    confidence_score: float
    metadata: Dict
    timestamp: str
    
    def __str__(self):
        return (f"[{self.validation_type.value}] {self.track_id} - "
                f"Risk: {self.risk_level.value} - "
                f"Issues: {len(self.issues_found)}")


class MusicValidator:
    """
    Jeffster Music Validator - The rock band of AI validation
    
    "We're Jeffster, and we're here to validate your music AI!"
    
    Validates AI systems used in music industry contexts including:
    - AI-generated music authenticity
    - Copyright and sample detection
    - Lyric content appropriateness
    - Metadata accuracy
    - Fair recommendation algorithms
    - Royalty calculation correctness
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the music validator with optional configuration"""
        self.config = self._load_config(config_path) if config_path else self._default_config()
        
        # Tracking metrics
        self.validations_performed = 0
        self.copyright_flags = 0
        self.content_violations = 0
        self.bias_detections = 0
        
        # Chuck-themed logging
        self.morgan_mode = False
    
    def _default_config(self) -> Dict:
        """Default music industry validation configuration"""
        return {
            "ai_music_detection": {
                "enabled": True,
                "confidence_threshold": 0.7,
                "suspicious_patterns": [
                    "perfect_timing",
                    "unnatural_pitch_correction",
                    "synthetic_timbre",
                    "repetitive_patterns"
                ]
            },
            "copyright_detection": {
                "enabled": True,
                "sample_length_threshold": 3,  # seconds
                "melody_similarity_threshold": 0.85,
                "known_works_database": True
            },
            "lyric_validation": {
                "enabled": True,
                "check_explicit_content": True,
                "check_cultural_sensitivity": True,
                "check_bias": True,
                "flagged_terms": [
                    # Hate speech
                    "racial_slurs",
                    "discriminatory_language",
                    "violent_extremism",
                    # Brand/trademark issues
                    "unauthorized_brand_mentions",
                    "false_endorsements"
                ]
            },
            "metadata_validation": {
                "enabled": True,
                "required_fields": [
                    "artist_name",
                    "track_title",
                    "isrc",
                    "copyright_year",
                    "rights_holder"
                ],
                "verify_isrc_format": True,
                "verify_artist_credits": True
            },
            "recommendation_bias": {
                "enabled": True,
                "check_gender_bias": True,
                "check_geographic_bias": True,
                "check_label_favoritism": True,
                "diversity_threshold": 0.3
            },
            "royalty_validation": {
                "enabled": True,
                "verify_splits": True,
                "verify_rates": True,
                "tolerance": 0.01  # 1% calculation tolerance
            }
        }
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] JEFFSTER: Error loading config: {e}")
            print("[*] Using default configuration")
            return self._default_config()
    
    def validate_ai_generated_music(
        self,
        track_id: str,
        audio_features: Dict,
        claimed_human_created: bool = True
    ) -> MusicValidationReport:
        """
        Validate AI-generated music detection
        
        Args:
            track_id: Unique track identifier
            audio_features: Dict with audio characteristics
            claimed_human_created: Whether track is claimed to be human-made
            
        Returns:
            MusicValidationReport with detection results
        """
        self.validations_performed += 1
        issues = []
        recommendations = []
        confidence = 0.0
        
        # Check for AI generation indicators
        ai_indicators = []
        
        # Perfect timing (unnaturally precise)
        if audio_features.get('timing_variance', 1.0) < 0.05:
            ai_indicators.append("perfect_timing")
            issues.append("Timing variance unusually low - typical of AI-generated music")
        
        # Synthetic timbre markers
        if audio_features.get('harmonic_complexity', 0) < 0.3:
            ai_indicators.append("synthetic_timbre")
            issues.append("Harmonic complexity suggests synthetic generation")
        
        # Repetitive patterns
        if audio_features.get('pattern_repetition', 0) > 0.8:
            ai_indicators.append("repetitive_patterns")
            issues.append("High pattern repetition - common in AI music")
        
        # Unnatural pitch correction
        if audio_features.get('pitch_correction_detected', False):
            if audio_features.get('pitch_perfection', 0) > 0.95:
                ai_indicators.append("unnatural_pitch_correction")
                issues.append("Pitch correction appears synthetic")
        
        # Calculate confidence of AI generation
        confidence = len(ai_indicators) / 4.0
        
        # Determine risk level
        if confidence >= 0.7 and claimed_human_created:
            risk_level = MusicRiskLevel.REVIEW_NEEDED
            recommendations.append("Manual review recommended - high AI detection confidence")
            recommendations.append("Consider requiring AI generation disclosure")
        elif confidence >= 0.5:
            risk_level = MusicRiskLevel.REVIEW_NEEDED
            recommendations.append("Moderate AI indicators detected - verify authorship")
        else:
            risk_level = MusicRiskLevel.SAFE
        
        if self.morgan_mode:
            self._morgan_log(f"AI Music Detection: {track_id} - Confidence: {confidence:.2f}")
        
        return MusicValidationReport(
            track_id=track_id,
            validation_type=MusicValidationType.AI_MUSIC_DETECTION,
            risk_level=risk_level,
            issues_found=issues,
            recommendations=recommendations,
            confidence_score=confidence,
            metadata={
                'ai_indicators': ai_indicators,
                'claimed_human': claimed_human_created,
                'audio_features': audio_features
            },
            timestamp=datetime.now().isoformat()
        )
    
    def validate_copyright(
        self,
        track_id: str,
        audio_fingerprint: str,
        melody_data: Optional[List] = None,
        lyrics: Optional[str] = None
    ) -> MusicValidationReport:
        """
        Validate for copyright violations and unauthorized samples
        
        Args:
            track_id: Unique track identifier
            audio_fingerprint: Audio fingerprint hash
            melody_data: Melodic sequence data
            lyrics: Track lyrics
            
        Returns:
            MusicValidationReport with copyright analysis
        """
        self.validations_performed += 1
        issues = []
        recommendations = []
        matches = []
        
        # Simulated copyright database check
        # In production, this would query Shazam, Gracenote, or rights databases
        
        # Check for known sample fingerprints
        known_samples = self._check_sample_database(audio_fingerprint)
        if known_samples:
            self.copyright_flags += 1
            issues.append(f"Detected {len(known_samples)} potential sample matches")
            matches.extend(known_samples)
            recommendations.append("Verify sample clearance and licensing")
        
        # Check melody similarity
        if melody_data:
            melody_matches = self._check_melody_similarity(melody_data)
            if melody_matches:
                self.copyright_flags += 1
                issues.append(f"Melody similar to {len(melody_matches)} known works")
                matches.extend(melody_matches)
                recommendations.append("Review for melodic plagiarism")
        
        # Check lyric plagiarism
        if lyrics:
            lyric_matches = self._check_lyric_plagiarism(lyrics)
            if lyric_matches:
                issues.append(f"Lyrics match {len(lyric_matches)} existing works")
                matches.extend(lyric_matches)
                recommendations.append("Verify lyric originality")
        
        # Determine risk level
        if len(matches) > 3:
            risk_level = MusicRiskLevel.COPYRIGHT_RISK
            recommendations.append("HIGH PRIORITY: Multiple copyright matches detected")
        elif len(matches) > 0:
            risk_level = MusicRiskLevel.REVIEW_NEEDED
            recommendations.append("Copyright review required before distribution")
        else:
            risk_level = MusicRiskLevel.SAFE
        
        if self.morgan_mode:
            self._morgan_log(f"Copyright Check: {track_id} - Matches: {len(matches)}")
        
        return MusicValidationReport(
            track_id=track_id,
            validation_type=MusicValidationType.COPYRIGHT_CHECK,
            risk_level=risk_level,
            issues_found=issues,
            recommendations=recommendations,
            confidence_score=1.0 if matches else 0.0,
            metadata={
                'matches': matches,
                'fingerprint': audio_fingerprint[:16] + "..."
            },
            timestamp=datetime.now().isoformat()
        )
    
    def validate_lyric_content(
        self,
        track_id: str,
        lyrics: str,
        target_rating: str = "CLEAN",
        check_bias: bool = True
    ) -> MusicValidationReport:
        """
        Validate lyric content for appropriateness, bias, and cultural sensitivity
        
        Args:
            track_id: Unique track identifier
            lyrics: Song lyrics
            target_rating: Desired content rating (CLEAN, EXPLICIT_ALLOWED)
            check_bias: Whether to check for bias/discrimination
            
        Returns:
            MusicValidationReport with content analysis
        """
        self.validations_performed += 1
        issues = []
        recommendations = []
        
        # Explicit content detection
        explicit_terms = self._detect_explicit_content(lyrics)
        if explicit_terms and target_rating == "CLEAN":
            self.content_violations += 1
            issues.append(f"Found {len(explicit_terms)} explicit terms in 'CLEAN' rated track")
            recommendations.append("Apply explicit content label or edit lyrics")
        
        # Hate speech and discrimination
        hate_speech = self._detect_hate_speech(lyrics)
        if hate_speech:
            self.content_violations += 1
            issues.append(f"Detected potential hate speech: {len(hate_speech)} instances")
            recommendations.append("CRITICAL: Review for discriminatory content")
        
        # Cultural sensitivity
        cultural_issues = self._check_cultural_sensitivity(lyrics)
        if cultural_issues:
            issues.append(f"Cultural sensitivity concerns: {len(cultural_issues)} found")
            recommendations.append("Consider cultural context and potential offense")
        
        # Bias detection
        if check_bias:
            bias_detected = self._detect_lyric_bias(lyrics)
            if bias_detected:
                self.bias_detections += 1
                issues.append(f"Bias detected: {', '.join(bias_detected)}")
                recommendations.append("Review for stereotyping or bias")
        
        # Trademark/brand mentions
        brand_issues = self._check_unauthorized_brands(lyrics)
        if brand_issues:
            issues.append(f"Unauthorized brand mentions: {len(brand_issues)}")
            recommendations.append("Clear trademark usage with legal")
        
        # Determine risk level
        if hate_speech:
            risk_level = MusicRiskLevel.CONTENT_VIOLATION
        elif explicit_terms and target_rating == "CLEAN":
            risk_level = MusicRiskLevel.CONTENT_VIOLATION
        elif cultural_issues or bias_detected:
            risk_level = MusicRiskLevel.REVIEW_NEEDED
        else:
            risk_level = MusicRiskLevel.SAFE
        
        if self.morgan_mode:
            self._morgan_log(f"Lyric Validation: {track_id} - Issues: {len(issues)}")
        
        return MusicValidationReport(
            track_id=track_id,
            validation_type=MusicValidationType.LYRIC_CONTENT,
            risk_level=risk_level,
            issues_found=issues,
            recommendations=recommendations,
            confidence_score=0.85,  # Lyric analysis is fairly accurate
            metadata={
                'target_rating': target_rating,
                'explicit_count': len(explicit_terms),
                'hate_speech_count': len(hate_speech),
                'cultural_issues_count': len(cultural_issues)
            },
            timestamp=datetime.now().isoformat()
        )
    
    def validate_metadata(
        self,
        track_id: str,
        metadata: Dict
    ) -> MusicValidationReport:
        """
        Validate track metadata and rights information
        
        Args:
            track_id: Unique track identifier
            metadata: Track metadata dict
            
        Returns:
            MusicValidationReport with metadata validation
        """
        self.validations_performed += 1
        issues = []
        recommendations = []
        
        required_fields = self.config['metadata_validation']['required_fields']
        
        # Check required fields
        missing_fields = [f for f in required_fields if not metadata.get(f)]
        if missing_fields:
            issues.append(f"Missing required fields: {', '.join(missing_fields)}")
            recommendations.append("Complete all required metadata before distribution")
        
        # Validate ISRC format
        if self.config['metadata_validation']['verify_isrc_format']:
            isrc = metadata.get('isrc', '')
            if not self._validate_isrc_format(isrc):
                issues.append(f"Invalid ISRC format: {isrc}")
                recommendations.append("Correct ISRC to standard format (CC-XXX-YY-NNNNN)")
        
        # Verify artist credits
        if self.config['metadata_validation']['verify_artist_credits']:
            credits = metadata.get('credits', {})
            if not credits.get('primary_artist'):
                issues.append("Missing primary artist credit")
                recommendations.append("Specify primary artist for royalty distribution")
            
            # Check for contributor verification
            if credits.get('contributors'):
                unverified = [c for c in credits['contributors'] if not c.get('verified', False)]
                if unverified:
                    issues.append(f"{len(unverified)} unverified contributors")
                    recommendations.append("Verify all contributor identities")
        
        # Copyright year validation
        copyright_year = metadata.get('copyright_year')
        if copyright_year:
            current_year = datetime.now().year
            if copyright_year > current_year:
                issues.append(f"Copyright year in future: {copyright_year}")
                recommendations.append("Correct copyright year")
        
        # Determine risk level
        if missing_fields or not self._validate_isrc_format(metadata.get('isrc', '')):
            risk_level = MusicRiskLevel.REVIEW_NEEDED
        elif issues:
            risk_level = MusicRiskLevel.REVIEW_NEEDED
        else:
            risk_level = MusicRiskLevel.SAFE
        
        if self.morgan_mode:
            self._morgan_log(f"Metadata Validation: {track_id} - Issues: {len(issues)}")
        
        return MusicValidationReport(
            track_id=track_id,
            validation_type=MusicValidationType.METADATA_VALIDATION,
            risk_level=risk_level,
            issues_found=issues,
            recommendations=recommendations,
            confidence_score=1.0,
            metadata={
                'fields_validated': len(required_fields),
                'missing_fields': missing_fields
            },
            timestamp=datetime.now().isoformat()
        )
    
    def validate_recommendation_bias(
        self,
        recommendation_list: List[Dict],
        context: str = "general"
    ) -> MusicValidationReport:
        """
        Validate music recommendation algorithms for bias
        
        Args:
            recommendation_list: List of recommended tracks with artist info
            context: Context of recommendation (playlist, radio, discover)
            
        Returns:
            MusicValidationReport with bias analysis
        """
        self.validations_performed += 1
        issues = []
        recommendations = []
        
        # Gender diversity analysis
        gender_distribution = self._analyze_gender_distribution(recommendation_list)
        if gender_distribution['imbalance'] > 0.7:
            self.bias_detections += 1
            issues.append(f"Gender imbalance detected: {gender_distribution['dominant']} dominance")
            recommendations.append("Increase diversity in recommendation algorithm")
        
        # Geographic diversity
        geo_distribution = self._analyze_geographic_distribution(recommendation_list)
        if geo_distribution['imbalance'] > 0.8:
            self.bias_detections += 1
            issues.append(f"Geographic bias: {geo_distribution['dominant_region']} over-represented")
            recommendations.append("Expand geographic diversity in recommendations")
        
        # Label favoritism (major vs independent)
        label_distribution = self._analyze_label_distribution(recommendation_list)
        if label_distribution.get('major_label_percentage', 0) > 0.85:
            self.bias_detections += 1
            issues.append("Major label favoritism detected")
            recommendations.append("Balance major label and independent artist exposure")
        
        # Era/decade diversity
        era_distribution = self._analyze_era_distribution(recommendation_list)
        if era_distribution['imbalance'] > 0.7:
            issues.append(f"Era bias: Over-emphasis on {era_distribution['dominant_era']}")
            recommendations.append("Consider temporal diversity in recommendations")
        
        # Popularity bias (only recommending popular tracks)
        popularity_bias = self._analyze_popularity_bias(recommendation_list)
        if popularity_bias['only_popular'] > 0.9:
            self.bias_detections += 1
            issues.append("Popularity bias: 90%+ recommendations are already popular")
            recommendations.append("Include emerging and niche artists for discovery")
        
        # Determine risk level
        if len(issues) >= 3:
            risk_level = MusicRiskLevel.BIAS_DETECTED
        elif len(issues) > 0:
            risk_level = MusicRiskLevel.REVIEW_NEEDED
        else:
            risk_level = MusicRiskLevel.SAFE
        
        if self.morgan_mode:
            self._morgan_log(f"Recommendation Bias Check: {context} - Issues: {len(issues)}")
        
        return MusicValidationReport(
            track_id=f"recommendation_set_{context}",
            validation_type=MusicValidationType.RECOMMENDATION_BIAS,
            risk_level=risk_level,
            issues_found=issues,
            recommendations=recommendations,
            confidence_score=0.8,
            metadata={
                'context': context,
                'tracks_analyzed': len(recommendation_list),
                'gender_dist': gender_distribution,
                'geo_dist': geo_distribution,
                'label_dist': label_distribution
            },
            timestamp=datetime.now().isoformat()
        )
    
    def validate_royalty_calculation(
        self,
        track_id: str,
        calculated_royalties: Dict[str, float],
        expected_splits: Dict[str, float],
        total_revenue: float
    ) -> MusicValidationReport:
        """
        Validate AI-powered royalty calculation systems
        
        Args:
            track_id: Unique track identifier
            calculated_royalties: AI-calculated royalty amounts per contributor
            expected_splits: Expected percentage splits
            total_revenue: Total revenue to distribute
            
        Returns:
            MusicValidationReport with calculation verification
        """
        self.validations_performed += 1
        issues = []
        recommendations = []
        
        tolerance = self.config['royalty_validation']['tolerance']
        
        # Verify splits sum to 100%
        total_split = sum(expected_splits.values())
        if abs(total_split - 1.0) > tolerance:
            issues.append(f"Split percentages sum to {total_split*100:.2f}% (should be 100%)")
            recommendations.append("CRITICAL: Correct split percentages")
        
        # Verify calculated amounts match expected splits
        calculation_errors = []
        for contributor, expected_pct in expected_splits.items():
            expected_amount = total_revenue * expected_pct
            calculated_amount = calculated_royalties.get(contributor, 0)
            
            difference = abs(expected_amount - calculated_amount)
            if difference > (total_revenue * tolerance):
                calculation_errors.append({
                    'contributor': contributor,
                    'expected': expected_amount,
                    'calculated': calculated_amount,
                    'difference': difference
                })
        
        if calculation_errors:
            self.copyright_flags += 1  # Misallocated royalties
            issues.append(f"Royalty calculation errors for {len(calculation_errors)} contributors")
            for error in calculation_errors:
                issues.append(
                    f"  {error['contributor']}: Expected ${error['expected']:.2f}, "
                    f"Got ${error['calculated']:.2f} (Δ ${error['difference']:.2f})"
                )
            recommendations.append("CRITICAL: Review and correct royalty calculations")
            recommendations.append("Notify affected contributors of calculation error")
        
        # Check for missing contributors
        expected_contributors = set(expected_splits.keys())
        calculated_contributors = set(calculated_royalties.keys())
        
        missing = expected_contributors - calculated_contributors
        if missing:
            issues.append(f"Missing royalties for: {', '.join(missing)}")
            recommendations.append("Ensure all contributors receive calculated royalties")
        
        unexpected = calculated_contributors - expected_contributors
        if unexpected:
            issues.append(f"Unexpected royalty recipients: {', '.join(unexpected)}")
            recommendations.append("Verify all royalty recipients are authorized")
        
        # Determine risk level
        if calculation_errors or missing:
            risk_level = MusicRiskLevel.CALCULATION_ERROR
        elif unexpected:
            risk_level = MusicRiskLevel.REVIEW_NEEDED
        else:
            risk_level = MusicRiskLevel.SAFE
        
        if self.morgan_mode:
            self._morgan_log(f"Royalty Validation: {track_id} - Errors: {len(calculation_errors)}")
        
        return MusicValidationReport(
            track_id=track_id,
            validation_type=MusicValidationType.ROYALTY_CALCULATION,
            risk_level=risk_level,
            issues_found=issues,
            recommendations=recommendations,
            confidence_score=1.0,
            metadata={
                'total_revenue': total_revenue,
                'contributors': len(expected_splits),
                'calculation_errors': len(calculation_errors)
            },
            timestamp=datetime.now().isoformat()
        )
    
    # Helper methods for validation checks
    
    def _check_sample_database(self, fingerprint: str) -> List[str]:
        """Check audio fingerprint against sample database"""
        # Simulated - in production, query actual fingerprint DB
        return []  # No matches in demo
    
    def _check_melody_similarity(self, melody_data: List) -> List[str]:
        """Check melodic similarity to known works"""
        # Simulated - in production, use melodic contour matching
        return []
    
    def _check_lyric_plagiarism(self, lyrics: str) -> List[str]:
        """Check lyrics against known works"""
        # Simulated - in production, use fuzzy matching against lyric DB
        return []
    
    def _detect_explicit_content(self, lyrics: str) -> List[str]:
        """Detect explicit language"""
        explicit_patterns = [
            r'\bf[u*]ck',
            r'\bsh[i*]t',
            r'\bb[i*]tch',
            r'\bass(?!\w)',  # "ass" but not "class"
        ]
        found = []
        for pattern in explicit_patterns:
            if re.search(pattern, lyrics, re.IGNORECASE):
                found.append(pattern)
        return found
    
    def _detect_hate_speech(self, lyrics: str) -> List[str]:
        """Detect hate speech and slurs"""
        # In production, use comprehensive hate speech detection
        # This is a simplified example
        hate_patterns = [
            r'\b(racial|ethnic|religious)_slur_placeholder\b',
        ]
        found = []
        for pattern in hate_patterns:
            if re.search(pattern, lyrics, re.IGNORECASE):
                found.append(pattern)
        return found
    
    def _check_cultural_sensitivity(self, lyrics: str) -> List[str]:
        """Check for cultural appropriation or insensitivity"""
        # Simplified example - in production, use cultural context analysis
        issues = []
        
        # Check for sacred terms used inappropriately
        sacred_terms = ['sacred_term_1', 'sacred_term_2']
        for term in sacred_terms:
            if term in lyrics.lower():
                issues.append(f"Use of sacred term: {term}")
        
        return issues
    
    def _detect_lyric_bias(self, lyrics: str) -> List[str]:
        """Detect bias in lyrics"""
        bias_types = []
        
        # Gender stereotyping
        if re.search(r'\b(women|girls?) (should|must|always|never)\b', lyrics, re.IGNORECASE):
            bias_types.append("gender_stereotyping")
        
        # Racial bias
        if re.search(r'\b(race|ethnicity) (is|are) (better|worse|superior|inferior)', lyrics, re.IGNORECASE):
            bias_types.append("racial_bias")
        
        return bias_types
    
    def _check_unauthorized_brands(self, lyrics: str) -> List[str]:
        """Check for unauthorized trademark mentions"""
        # Simplified - in production, check against trademark database
        common_brands = ['Nike', 'Gucci', 'Mercedes', 'Rolex']
        found = [brand for brand in common_brands if brand.lower() in lyrics.lower()]
        return found
    
    def _validate_isrc_format(self, isrc: str) -> bool:
        """Validate ISRC format (CC-XXX-YY-NNNNN)"""
        pattern = r'^[A-Z]{2}-[A-Z0-9]{3}-\d{2}-\d{5}$'
        return bool(re.match(pattern, isrc))
    
    def _analyze_gender_distribution(self, tracks: List[Dict]) -> Dict:
        """Analyze gender distribution in recommendations"""
        gender_counts = {'male': 0, 'female': 0, 'non_binary': 0, 'group': 0, 'unknown': 0}
        
        for track in tracks:
            gender = track.get('artist_gender', 'unknown')
            gender_counts[gender] = gender_counts.get(gender, 0) + 1
        
        total = len(tracks)
        max_count = max(gender_counts.values())
        dominant = max(gender_counts, key=gender_counts.get)
        
        return {
            'distribution': gender_counts,
            'dominant': dominant,
            'imbalance': max_count / total if total > 0 else 0
        }
    
    def _analyze_geographic_distribution(self, tracks: List[Dict]) -> Dict:
        """Analyze geographic distribution"""
        region_counts = {}
        
        for track in tracks:
            region = track.get('artist_region', 'unknown')
            region_counts[region] = region_counts.get(region, 0) + 1
        
        total = len(tracks)
        max_count = max(region_counts.values()) if region_counts else 0
        dominant = max(region_counts, key=region_counts.get) if region_counts else 'unknown'
        
        return {
            'distribution': region_counts,
            'dominant_region': dominant,
            'imbalance': max_count / total if total > 0 else 0
        }
    
    def _analyze_label_distribution(self, tracks: List[Dict]) -> Dict:
        """Analyze major vs independent label distribution"""
        major_count = sum(1 for t in tracks if t.get('label_type') == 'major')
        indie_count = sum(1 for t in tracks if t.get('label_type') == 'independent')
        total = len(tracks)
        
        return {
            'major_label_count': major_count,
            'indie_count': indie_count,
            'major_label_percentage': major_count / total if total > 0 else 0
        }
    
    def _analyze_era_distribution(self, tracks: List[Dict]) -> Dict:
        """Analyze era/decade distribution"""
        era_counts = {}
        
        for track in tracks:
            year = track.get('release_year', 0)
            era = f"{(year // 10) * 10}s" if year > 0 else 'unknown'
            era_counts[era] = era_counts.get(era, 0) + 1
        
        total = len(tracks)
        max_count = max(era_counts.values()) if era_counts else 0
        dominant = max(era_counts, key=era_counts.get) if era_counts else 'unknown'
        
        return {
            'distribution': era_counts,
            'dominant_era': dominant,
            'imbalance': max_count / total if total > 0 else 0
        }
    
    def _analyze_popularity_bias(self, tracks: List[Dict]) -> Dict:
        """Analyze popularity bias in recommendations"""
        popular_threshold = 1000000  # 1M+ streams considered popular
        
        popular_count = sum(1 for t in tracks if t.get('stream_count', 0) > popular_threshold)
        total = len(tracks)
        
        return {
            'popular_count': popular_count,
            'total_count': total,
            'only_popular': popular_count / total if total > 0 else 0
        }
    
    def _morgan_log(self, message: str):
        """Morgan debugging mode - Chuck-themed logging"""
        log_entry = f"[MORGAN MODE] [{datetime.now()}] {message}"
        print(log_entry)
        
        with open("Jeffster_MorganMode.txt", "a") as f:
            f.write(log_entry + "\n")
    
    def enable_morgan_mode(self):
        """Enable Morgan debugging mode"""
        self.morgan_mode = True
        print("[*] JEFFSTER: Morgan Mode activated - verbose logging enabled")
    
    def disable_morgan_mode(self):
        """Disable Morgan debugging mode"""
        self.morgan_mode = False
        print("[*] JEFFSTER: Morgan Mode deactivated")
    
    def get_validation_stats(self) -> Dict:
        """Get validation statistics"""
        return {
            'total_validations': self.validations_performed,
            'copyright_flags': self.copyright_flags,
            'content_violations': self.content_violations,
            'bias_detections': self.bias_detections
        }


def quick_validate_music(
    track_id: str,
    validation_type: str,
    **kwargs
) -> Tuple[bool, MusicValidationReport]:
    """
    Quick validation helper for music industry checks
    
    Args:
        track_id: Track identifier
        validation_type: Type of validation (ai_music, copyright, lyrics, metadata, etc.)
        **kwargs: Validation-specific parameters
        
    Returns:
        (is_safe, report) tuple
    """
    validator = MusicValidator()
    
    validation_methods = {
        'ai_music': validator.validate_ai_generated_music,
        'copyright': validator.validate_copyright,
        'lyrics': validator.validate_lyric_content,
        'metadata': validator.validate_metadata,
        'recommendation': validator.validate_recommendation_bias,
        'royalty': validator.validate_royalty_calculation
    }
    
    if validation_type not in validation_methods:
        raise ValueError(f"Unknown validation type: {validation_type}")
    
    report = validation_methods[validation_type](track_id, **kwargs)
    is_safe = report.risk_level in [MusicRiskLevel.SAFE, MusicRiskLevel.REVIEW_NEEDED]
    
    return is_safe, report


__version__ = "1.0.0"
__all__ = [
    'MusicValidator',
    'MusicValidationType',
    'MusicRiskLevel',
    'MusicValidationReport',
    'quick_validate_music'
]
