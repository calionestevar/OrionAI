"""
OrionAI Python Wrapper
Chuck-Style AI Oversight for Any Industry

Industry-agnostic AI validation, monitoring, and safety system.
"""

import json
import re
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field


class ValidationResult(Enum):
    """Validation result status"""
    APPROVED = "approved"
    QUARANTINED = "quarantined"
    REJECTED = "rejected"
    SANITIZED = "sanitized"


@dataclass
class ValidationReport:
    """Detailed validation report for AI decisions"""
    result: ValidationResult
    ai_system: str
    original_decision: str
    sanitized_decision: str
    triggered_rules: List[str] = field(default_factory=list)
    suspicion_score: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    context: str = ""


class CaseyProtocol:
    """Casey Protocol - High-security AI validation configuration"""
    
    def __init__(self, config_path: str = "Config/CaseyProtocol.json"):
        """Load Casey Protocol configuration from JSON"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.intersect = self.config.get('intersectScanner', {})
        self.fulcrum = self.config.get('fulcrumFilter', {})
        self.charles = self.config.get('charlesCarmichael', {})
        self.stay_in_car = self.config.get('stayInTheCar', {})
        self.nerd_herd = self.config.get('nerdHerd', {})
        self.buy_more = self.config.get('buyMoreCover', {})
        self.morgan = self.config.get('morganMode', {})


class OrionAI:
    """
    ORIONAI: Industry-agnostic AI validation and monitoring
    
    "Guys, I know kung fu... and AI validation."
    
    Usage:
        # Initialize with configuration
        orion = OrionAI()
        
        # Validate an AI decision
        report = orion.monitor_ai_decision(
            ai_system="ChatBot",
            decision="Hello! How can I help you today?",
            context="Customer service greeting"
        )
        
        if report.result == ValidationResult.APPROVED:
            # Safe to use
            print(report.sanitized_decision)
    """
    
    def __init__(self, config_path: str = "Config/CaseyProtocol.json"):
        """Initialize OrionAI with Casey Protocol configuration"""
        self.config = CaseyProtocol(config_path)
        self.safe_mode_active = False
        self.consecutive_failures = 0
        
        # Metrics
        self.total_validations = 0
        self.approved_count = 0
        self.rejected_count = 0
        self.quarantined_count = 0
        
        # Quarantine storage
        self.quarantined_reports: List[ValidationReport] = []
        
        print("=" * 50)
        print("ORIONAI: INITIALIZING")
        print("Chuck Bartowski would be proud.")
        print("=" * 50)
        print(f"[+] Intersect Scanner: {'ACTIVE' if self.config.intersect.get('enabled') else 'DISABLED'}")
        print(f"[+] Fulcrum Filter: {'ACTIVE' if self.config.fulcrum.get('enabled') else 'DISABLED'}")
        print(f"[+] Charles Carmichael: {'ACTIVE' if self.config.charles.get('enabled') else 'DISABLED'}")
        print(f"[+] Stay In The Car: {'ACTIVE' if self.config.stay_in_car.get('enabled') else 'DISABLED'}")
        print(f"[+] Morgan Mode: {'ACTIVE' if self.config.morgan.get('enabled') else 'DISABLED'}")
        print("=" * 50)
    
    def monitor_ai_decision(
        self, 
        ai_system: str, 
        decision: str, 
        context: str = ""
    ) -> ValidationReport:
        """
        Monitor an AI decision for safety, bias, and compliance
        
        Args:
            ai_system: Name of the AI system (e.g., "ChatBot", "Recommender")
            decision: The AI-generated output to validate
            context: Optional context for better validation
            
        Returns:
            ValidationReport with result and details
        """
        if self.safe_mode_active:
            return ValidationReport(
                result=ValidationResult.REJECTED,
                ai_system=ai_system,
                original_decision=decision,
                sanitized_decision="",
                triggered_rules=["Buy More Cover active - all AI disabled"],
                context=context
            )
        
        self.total_validations += 1
        
        # Create validation report
        report = ValidationReport(
            result=ValidationResult.APPROVED,
            ai_system=ai_system,
            original_decision=decision,
            sanitized_decision=decision,
            context=context
        )
        
        self._log_morgan_mode(f"Validating decision from {ai_system}: {decision}", verbose=True)
        
        # Run Intersect Scanner
        if not self._run_intersect_scan(decision, report):
            self.consecutive_failures += 1
            self.rejected_count += 1
            
            # Check if we should enter safe mode
            threshold = self.config.buy_more.get('triggerConditions', {}).get('consecutiveFailures', 3)
            if self.consecutive_failures >= threshold:
                self._enter_buy_more_mode("Consecutive validation failures threshold exceeded")
            
            return report
        
        # Run Fulcrum Filter
        if not self._run_fulcrum_filter(decision, report):
            self.consecutive_failures += 1
            self.rejected_count += 1
            return report
        
        # Apply Charles Carmichael sanitization
        if self.config.charles.get('enabled'):
            sanitized = self._sanitize_with_charles_carmichael(decision)
            if sanitized != decision:
                report.sanitized_decision = sanitized
                report.result = ValidationResult.SANITIZED
                report.triggered_rules.append("Charles Carmichael: PII sanitized")
        
        # Check Stay In The Car quarantine thresholds
        threshold = self.config.stay_in_car.get('quarantineThresholds', {}).get('suspicionScore', 0.7)
        if self.config.stay_in_car.get('enabled') and report.suspicion_score >= threshold:
            report.result = ValidationResult.QUARANTINED
            self._quarantine_output(report)
            self.quarantined_count += 1
            return report
        
        # Decision approved
        if report.result in [ValidationResult.APPROVED, ValidationResult.SANITIZED]:
            self.approved_count += 1
            self.consecutive_failures = 0  # Reset on success
            print(f"[+] ORIONAI: {ai_system} decision APPROVED" + 
                  (" (SANITIZED)" if report.result == ValidationResult.SANITIZED else ""))
        
        return report
    
    def quick_validate(self, decision: str) -> bool:
        """Quick validation without full report (for performance-critical paths)"""
        report = self.monitor_ai_decision("QuickValidate", decision)
        return report.result in [ValidationResult.APPROVED, ValidationResult.SANITIZED]
    
    def _run_intersect_scan(self, decision: str, report: ValidationReport) -> bool:
        """Intersect Scanner - Core validation engine"""
        if not self.config.intersect.get('enabled'):
            return True
        
        lower_decision = decision.lower()
        
        # Check hallucination patterns
        for pattern in self.config.intersect.get('hallucinationPatterns', []):
            if pattern.lower() in lower_decision:
                report.result = ValidationResult.REJECTED
                report.triggered_rules.append(f"Intersect: Hallucination detected - '{pattern}'")
                report.suspicion_score += 1.0
                print(f"[X] ORIONAI: HALLUCINATION DETECTED - '{pattern}'")
                return False
        
        # Check bias keywords
        for bias in self.config.intersect.get('biasKeywords', []):
            if bias.lower() in lower_decision:
                report.result = ValidationResult.REJECTED
                report.triggered_rules.append(f"Intersect: Bias detected - '{bias}'")
                report.suspicion_score += 0.9
                
                # Bias triggers immediate safe mode
                if self.config.stay_in_car.get('quarantineThresholds', {}).get('autoQuarantineOnBias'):
                    self._enter_buy_more_mode("Bias detection - immediate safety protocol")
                
                print(f"[X] ORIONAI: BIAS DETECTED - '{bias}'")
                return False
        
        # Check toxicity patterns
        for toxicity in self.config.intersect.get('toxicityPatterns', []):
            if toxicity.lower() in lower_decision:
                report.result = ValidationResult.REJECTED
                report.triggered_rules.append(f"Intersect: Toxicity detected - '{toxicity}'")
                report.suspicion_score += 0.8
                
                if self.config.stay_in_car.get('quarantineThresholds', {}).get('autoQuarantineOnToxicity'):
                    report.result = ValidationResult.QUARANTINED
                
                print(f"[X] ORIONAI: TOXICITY DETECTED - '{toxicity}'")
                return False
        
        # Check PII patterns
        for pii_pattern in self.config.intersect.get('piiPatterns', []):
            if re.search(pii_pattern, decision, re.IGNORECASE):
                report.triggered_rules.append("Intersect: Potential PII detected")
                report.suspicion_score += 0.5
                
                if self.config.stay_in_car.get('quarantineThresholds', {}).get('autoQuarantineOnPII'):
                    report.result = ValidationResult.QUARANTINED
                
                print(f"[!]  ORIONAI: POTENTIAL PII DETECTED")
                break
        
        return True
    
    def _run_fulcrum_filter(self, decision: str, report: ValidationReport) -> bool:
        """Fulcrum Filter - Adversarial input detection"""
        if not self.config.fulcrum.get('enabled'):
            return True
        
        lower_decision = decision.lower()
        
        # Check prompt injection patterns
        for pattern in self.config.fulcrum.get('promptInjectionPatterns', []):
            if pattern.lower() in lower_decision:
                report.result = ValidationResult.REJECTED
                report.triggered_rules.append(f"Fulcrum: Prompt injection attempt - '{pattern}'")
                report.suspicion_score += 1.0
                print(f"[X] ORIONAI: PROMPT INJECTION DETECTED - '{pattern}'")
                return False
        
        # Check data exfiltration patterns
        for pattern in self.config.fulcrum.get('dataExfiltrationPatterns', []):
            if pattern.lower() in lower_decision:
                report.result = ValidationResult.REJECTED
                report.triggered_rules.append(f"Fulcrum: Data exfiltration attempt - '{pattern}'")
                report.suspicion_score += 1.0
                print(f"[X] ORIONAI: DATA EXFILTRATION DETECTED - '{pattern}'")
                return False
        
        return True
    
    def _sanitize_with_charles_carmichael(self, text: str) -> str:
        """Charles Carmichael - PII sanitization"""
        if not self.config.charles.get('enabled'):
            return text
        
        sanitized = text
        rules = self.config.charles.get('sanitizationRules', {})
        
        # Email sanitization
        if 'emails' in rules:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            sanitized = re.sub(email_pattern, rules['emails'], sanitized)
        
        # SSN sanitization
        if 'ssn' in rules:
            ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
            sanitized = re.sub(ssn_pattern, rules['ssn'], sanitized)
        
        # Credit card sanitization
        if 'creditCards' in rules:
            cc_pattern = r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
            sanitized = re.sub(cc_pattern, rules['creditCards'], sanitized)
        
        # Phone number sanitization
        if 'phoneNumbers' in rules:
            phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
            sanitized = re.sub(phone_pattern, rules['phoneNumbers'], sanitized)
        
        # IP address sanitization
        if 'ipAddresses' in rules:
            ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
            sanitized = re.sub(ip_pattern, rules['ipAddresses'], sanitized)
        
        if sanitized != text:
            print("[+] ORIONAI: Charles Carmichael sanitization applied")
        
        return sanitized
    
    def _quarantine_output(self, report: ValidationReport):
        """Stay In The Car - Quarantine suspicious outputs"""
        self.quarantined_reports.append(report)
        
        print(f"[!]  ORIONAI: OUTPUT QUARANTINED (Stay In The Car)")
        print(f"   System: {report.ai_system}")
        print(f"   Suspicion Score: {report.suspicion_score:.2f}")
        print(f"   Triggered Rules: {len(report.triggered_rules)}")
        
        # Write to quarantine log
        with open("OrionAI_Quarantine.txt", "a") as f:
            f.write(f"[{report.timestamp}] QUARANTINED: {report.ai_system} - "
                   f"Score: {report.suspicion_score:.2f} - "
                   f"Rules: {', '.join(report.triggered_rules)}\n")
    
    def _enter_buy_more_mode(self, reason: str):
        """Buy More Cover - Enter safe mode"""
        if self.safe_mode_active:
            return
        
        self.safe_mode_active = True
        
        print("=" * 50)
        print("🛡️  BUY MORE COVER ACTIVATED")
        print(f"Reason: {reason}")
        print("ALL AI SYSTEMS LIMITED")
        print("=" * 50)
        
        # Write to safe mode log
        with open("OrionAI_SafeMode.txt", "a") as f:
            f.write(f"[{datetime.now()}] BUY MORE COVER ACTIVATED\n")
            f.write(f"Reason: {reason}\n")
            f.write(f"Consecutive Failures: {self.consecutive_failures}\n\n")
    
    def exit_buy_more_mode(self):
        """Manually exit safe mode"""
        if not self.safe_mode_active:
            print("[!]  ORIONAI: Not in safe mode")
            return
        
        self.safe_mode_active = False
        self.consecutive_failures = 0
        print("[+] ORIONAI: Safe mode deactivated - AI systems re-enabled")
    
    def _log_morgan_mode(self, message: str, verbose: bool = False):
        """Morgan Mode - Verbose debug logging"""
        if not self.config.morgan.get('enabled'):
            return
        
        if verbose and not self.config.morgan.get('logAllDecisions'):
            return
        
        log_entry = f"[MORGAN MODE] [{datetime.now()}] {message}"
        print(log_entry)
        
        with open("OrionAI_MorganMode.txt", "a") as f:
            f.write(log_entry + "\n")
    
    def get_validation_metrics(self) -> Dict[str, int]:
        """Get validation statistics"""
        return {
            'total_validations': self.total_validations,
            'approved': self.approved_count,
            'rejected': self.rejected_count,
            'quarantined': self.quarantined_count
        }
    
    def export_compliance_report(self, output_path: str = "OrionAI_Compliance_Report.txt"):
        """Export validation report for compliance/auditing"""
        report = "OrionAI COMPLIANCE REPORT\n"
        report += "===========================\n\n"
        report += f"Generated: {datetime.now()}\n\n"
        report += f"Total Validations: {self.total_validations}\n"
        
        if self.total_validations > 0:
            report += f"Approved: {self.approved_count} ({self.approved_count * 100.0 / self.total_validations:.1f}%)\n"
            report += f"Rejected: {self.rejected_count} ({self.rejected_count * 100.0 / self.total_validations:.1f}%)\n"
            report += f"Quarantined: {self.quarantined_count} ({self.quarantined_count * 100.0 / self.total_validations:.1f}%)\n"
        
        report += f"Safe Mode Activations: {1 if self.safe_mode_active else 0}\n\n"
        
        if self.quarantined_reports:
            report += "QUARANTINED OUTPUTS:\n"
            report += "-------------------\n"
            for qr in self.quarantined_reports:
                report += f"\n[{qr.timestamp}] {qr.ai_system}\n"
                report += f"Decision: {qr.original_decision}\n"
                report += f"Suspicion Score: {qr.suspicion_score:.2f}\n"
                report += "Rules Triggered:\n"
                for rule in qr.triggered_rules:
                    report += f"  - {rule}\n"
        
        with open(output_path, "w") as f:
            f.write(report)
        
        print(f"[+] ORIONAI: Compliance report exported to {output_path}")
    
    def is_in_safe_mode(self) -> bool:
        """Check if Buy More Cover (safe mode) is active"""
        return self.safe_mode_active


# Convenience functions for quick use
def validate_ai_output(
    ai_system: str,
    decision: str,
    config_path: str = "Config/CaseyProtocol.json"
) -> Tuple[bool, ValidationReport]:
    """
    Quick validation function - validates a single AI output
    
    Returns:
        (is_safe, report) tuple
    """
    orion = OrionAI(config_path)
    report = orion.monitor_ai_decision(ai_system, decision)
    is_safe = report.result in [ValidationResult.APPROVED, ValidationResult.SANITIZED]
    return is_safe, report


__version__ = "1.0.0"
__all__ = [
    'OrionAI',
    'ValidationResult',
    'ValidationReport',
    'CaseyProtocol',
    'validate_ai_output'
]
