# OrionAI Python Package

Industry-agnostic AI validation, monitoring, and safety system with Chuck-themed naming conventions.

## Installation

```bash
pip install aicastle
```

Or install from source:

```bash
git clone https://github.com/calionestevar/OrionAI.git
cd OrionAI/Python
pip install -e .
```

## Quick Start

```python
from aicastle import AICastle, ValidationResult

# Initialize with configuration
castle = AICastle("Config/CaseyProtocol.json")

# Validate an AI decision
report = castle.monitor_ai_decision(
    ai_system="ChatBot",
    decision="Hello! How can I help you today?",
    context="Customer service greeting"
)

# Check result
if report.result == ValidationResult.APPROVED:
    print("✓ Safe to use:", report.sanitized_decision)
elif report.result == ValidationResult.SANITIZED:
    print("⚠ PII removed:", report.sanitized_decision)
else:
    print("❌ Rejected:", report.triggered_rules)
```

## Features

### 🔍 Intersect Scanner
- Hallucination detection
- Bias keyword matching
- Toxicity filtering
- PII pattern recognition

### 🛡️ Fulcrum Filter
- Prompt injection detection
- Jailbreak attempt blocking
- Data exfiltration prevention

### 🕴️ Charles Carmichael
- Email sanitization
- SSN redaction
- Credit card masking
- Phone number anonymization
- IP address obfuscation

### 🚗 Stay In The Car
- Quarantine suspicious outputs
- Configurable suspicion scoring
- Automatic quarantine triggers

### 🛠️ Nerd Herd
- Alert system for failures
- Integration hooks (Jira, GitHub, Slack)
- Local file logging

### 🏪 Buy More Cover
- Safe mode activation
- Consecutive failure tracking
- Manual override protection

### 📊 Morgan Mode
- Verbose debug logging
- Full decision history
- Stack trace inclusion

## Industry Examples

### Gaming
```python
castle = AICastle()
report = castle.monitor_ai_decision(
    "NPCDialogue",
    "Welcome, brave adventurer!",
    "Fantasy RPG NPC greeting"
)
```

### Healthcare
```python
castle = AICastle()
report = castle.monitor_ai_decision(
    "HealthAssistant",
    "Your prescription is ready for pickup.",
    "Patient communication"
)
```

### Finance
```python
castle = AICastle()
report = castle.monitor_ai_decision(
    "InvestmentAdvisor",
    "Diversification reduces portfolio risk.",
    "Financial advice"
)
```

### E-commerce
```python
castle = AICastle()
report = castle.monitor_ai_decision(
    "RecommendationEngine",
    "Based on your history, try Product X.",
    "Product suggestions"
)
```

### Customer Service
```python
castle = AICastle()
report = castle.monitor_ai_decision(
    "ServiceBot",
    "I'm happy to help with your order!",
    "Customer support"
)
```

## Configuration

Create a `CaseyProtocol.json` configuration file:

```json
{
  "intersectScanner": {
    "enabled": true,
    "hallucinationPatterns": ["flying elephants", "free money"],
    "biasKeywords": ["women can't", "men are better"],
    "toxicityPatterns": ["kill yourself", "you're worthless"]
  },
  "stayInTheCar": {
    "enabled": true,
    "quarantineThresholds": {
      "suspicionScore": 0.7,
      "autoQuarantineOnBias": true
    }
  }
}
```

See `Config/CaseyProtocol.json` for full configuration options.

## Metrics & Reporting

```python
# Get validation metrics
metrics = castle.get_validation_metrics()
print(f"Total validations: {metrics['total_validations']}")
print(f"Approved: {metrics['approved']}")
print(f"Rejected: {metrics['rejected']}")

# Export compliance report
castle.export_compliance_report("compliance_report.txt")
```

## API Reference

### `AICastle`

Main validation class.

**Methods:**
- `monitor_ai_decision(ai_system, decision, context="")` - Full validation with report
- `quick_validate(decision)` - Fast boolean validation
- `get_validation_metrics()` - Get statistics
- `export_compliance_report(path)` - Generate audit report
- `is_in_safe_mode()` - Check if Buy More Cover is active
- `exit_buy_more_mode()` - Manually deactivate safe mode

### `ValidationReport`

Detailed validation result.

**Attributes:**
- `result` - ValidationResult enum (APPROVED, REJECTED, QUARANTINED, SANITIZED)
- `ai_system` - Name of the AI system
- `original_decision` - Original AI output
- `sanitized_decision` - PII-cleaned version
- `triggered_rules` - List of validation rules that fired
- `suspicion_score` - Numeric score (0.0 - 1.0+)
- `timestamp` - When validation occurred
- `context` - User-provided context

### `ValidationResult`

Enum for validation outcomes.

- `APPROVED` - Safe to use as-is
- `SANITIZED` - PII removed, safe to use
- `QUARANTINED` - Flagged for review
- `REJECTED` - Blocked, unsafe

## Examples

Run the included examples:

```bash
cd Python
python examples.py
```

Examples cover:
1. Gaming - NPC dialogue validation
2. Customer service - Response validation
3. Social media - Content moderation
4. Healthcare - Patient interaction
5. E-commerce - Product recommendations
6. Finance - Investment advice
7. Metrics & reporting
8. Safe mode activation

## Testing

```bash
pip install pytest pytest-cov
pytest tests/ --cov=aicastle
```

## License

MIT License - See LICENSE file

## Chuck References

All module names reference the TV series "Chuck":
- **Intersect** - The AI database in Chuck's head
- **Casey Protocol** - John Casey, strict security agent
- **Fulcrum** - Adversarial organization
- **Charles Carmichael** - Chuck's undercover alias
- **Stay In The Car** - Sarah's frequent order to Chuck
- **Nerd Herd** - Buy More's tech support team
- **Buy More** - The cover organization
- **Morgan Mode** - Morgan Grimes, Chuck's verbose best friend
- **Ring Intel** - The Ring, shadow organization
- **Orion** - Stephen Bartowski's project

## Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.

## Support

- GitHub Issues: https://github.com/calionestevar/OrionAI/issues
- Documentation: https://github.com/calionestevar/OrionAI/wiki
