# OrionAI Python Package

Industry-agnostic AI validation, monitoring, and safety system with Chuck-themed naming conventions.

**PyPI:** [`pip install orion-validate`](https://pypi.org/project/orion-validate/)  
**GitHub:** [calionestevar/ai-castle](https://github.com/calionestevar/ai-castle)

## Installation

```bash
pip install orion-validate
```

To install with optional ML features:

```bash
pip install "orion-validate[ml]"
```

Or install from source:

```bash
git clone https://github.com/calionestevar/OrionAI.git
cd OrionAI
pip install -e .
```

## Quick Start

```python
from orionai import OrionAI, ValidationResult

# Initialize with configuration
orion = OrionAI("Config/CaseyProtocol.json")  # Or default bundled config

# Validate an AI decision
report = orion.monitor_ai_decision(
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

### 🔍 Intersect Scanner (Core Validation)
- Hallucination detection
- Bias keyword matching
- Toxicity filtering
- PII pattern recognition

### 🛡️ Fulcrum Filter (Adversarial Defense)
- Prompt injection detection
- Jailbreak attempt blocking
- Data exfiltration prevention

### 🕴️ Charles Carmichael (PII Sanitization)
- Email sanitization
- SSN redaction
- Credit card masking
- Phone number anonymization
- IP address obfuscation

### 🚗 Stay In The Car (Quarantine System)
- Quarantine suspicious outputs
- Configurable suspicion scoring
- Automatic quarantine triggers

### 🛠️ Nerd Herd (Alert Integration)
- Alert system for failures
- Integration hooks (Jira, GitHub, Slack)
- Local file logging

### 🏪 Buy More Cover (Safe Mode)
- Safe mode activation
- Consecutive failure tracking
- Manual override protection

### 📊 Morgan Mode (Debug Logging)
- Verbose debug logging
- Full decision history
- Stack trace inclusion

### 🧬 Genesis (Model Transparency)
- Source composition exposure
- Exclusion auditing
- Behavior documentation
- Transparency ratings

### 🎸 Jeffster (Music Industry Validation)
- AI-generated music detection
- Copyright/sample detection
- Lyric content validation
- Metadata/rights verification

## Industry Examples

### Gaming
```python
from orionai import OrionAI
orion = OrionAI()
report = orion.monitor_ai_decision(
    "NPCDialogue",
    "Welcome, brave adventurer!",
    "Fantasy RPG NPC greeting"
)
```

### Healthcare
```python
from orionai import OrionAI
orion = OrionAI()
report = orion.monitor_ai_decision(
    "HealthAssistant",
    "Your prescription is ready for pickup.",
    "Patient communication"
)
```

### Finance
```python
from orionai import OrionAI
orion = OrionAI()
report = orion.monitor_ai_decision(
    "InvestmentAdvisor",
    "Diversification reduces portfolio risk.",
    "Financial advice"
)
```

### E-commerce
```python
from orionai import OrionAI
orion = OrionAI()
report = orion.monitor_ai_decision(
    "RecommendationEngine",
    "Based on your history, try Product X.",
    "Product suggestions"
)
```

### Customer Service
```python
from orionai import OrionAI
orion = OrionAI()
report = orion.monitor_ai_decision(
    "ServiceBot",
    "I'm happy to help with your order!",
    "Customer support"
)
```

## Genesis Module (Model Transparency)
Genesis complements output-level validation with model-level transparency:
```python
from orionai import Genesis, GenesisRecommendation

genesis = Genesis("my-model-name")
report = genesis.run_full_audit()

print(f"Transparency: {report.recommendation.value}")
print(f"Sources Included: {report.sources_included}")
print(f"Sources Excluded: {report.sources_excluded}")
```
📖 Learn More: See docs/GENESIS_README.md in GitHub repo

## Jeffster Module (Music Industry)
```python
from orionai import MusicValidator, MusicValidationType

validator = MusicValidator()

# AI music detection
is_safe, report = quick_validate_music(
    "track-123",
    "ai_music",
    audio_features={"timing_variance": 0.02, "harmonic_complexity": 0.2}
)

# Copyright check
report = validator.validate_copyright(
    "track-123",
    audio_fingerprint="abc123def456"
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
metrics = orion.get_validation_metrics()
print(f"Total validations: {metrics['total_validations']}")
print(f"Approved: {metrics['approved']}")
print(f"Rejected: {metrics['rejected']}")

# Export compliance report
orion.export_compliance_report("compliance_report.txt")
```

## API Reference

### `OrionAI`

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

### `Genesis`

Model-level transparency auditor.

**Methods:**
- `run_full_audit()` - Run comprehensive model audit
- `export_audit_report(path)` - Export to file
- `get_audit_summary()` - Get results as dict

### `MusicValidator`

Music industry validation (Jeffster).

**Methods:**
- `validate_ai_generated_music()` - AI detection
- `validate_copyright()` - Copyright/samples check
- `validate_lyric_content()` - Content appropriateness
- `validate_metadata()` - Track metadata validation
- `validate_recommendation_bias()` - Algorithm fairness
- `validate_royalty_calculation()` - Payment accuracy
- `get_validation_stats()` - Statistics

## Examples

Run the included examples:

```bash
python examples/examples.py
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

Clone the repository for access to test suites:

```bash
git clone https://github.com/calionestevar/OrionAI.git
cd OrionAI
pip install pytest pytest-cov
pytest tests/ --cov=orionai
```

### Environment Variables

Control OrionAI behavior via environment variables:

- **`ORIONAI_DISABLE_ML`** - Set to `"1"` to disable ML model loading (useful for fast CI/CD tests)
- **`ORIONAI_TOXICITY_MODEL`** - Override the default toxicity detection model

```bash
# Run tests without downloading ML models (faster)
set ORIONAI_DISABLE_ML=1
pytest test_orionai.py

# Use a specific model
ORIONAI_TOXICITY_MODEL="cardiffnlp/twitter-roberta-base-hate-latest" python your_app.py
```

### Model Fallback

Ring Intel (ML toxicity detection) includes automatic fallback support. If the primary model fails to load, it will try alternative models:

1. `facebook/roberta-hate-speech-dynabench-r4-target` (primary)
2. `cardiffnlp/twitter-roberta-base-hate-latest`
3. `distilbert-base-uncased-finetuned-sst-2-english` (sentiment fallback)

This ensures your application remains functional even if specific HuggingFace models become unavailable.

## License

MIT License - See LICENSE file

## Chuck References

All module names reference the TV series "Chuck" (2007-2012):
| Module | Reference | In Show |
|--------|-----------|---------|
| Intersect | The Intersect | AI database in Chuck's head |
| OrionAI | Project Orion | Stephen Bartowski's Intersect framework |
| Casey Protocol | John Casey | NSA agent with strict protocols |
| Fulcrum Filter | Fulcrum | Adversarial spy organization |
| Charles Carmichael | Chuck's alias | Undercover identity |
| Stay In The Car | Sarah's order | Frequent containment command |
| Nerd Herd | The Nerd Herd | Buy More tech support team |
| Buy More Cover | Buy More | Electronics store cover |
| Morgan Mode | Morgan Grimes | Verbose best friend (debug loggin) |
| Ring Intel | The Ring | Shadow organization (ML detection) |
| Awesome | Devon Woodcomb (aka Captain Awesome) | Chuck's sister's fiance/husband |
| Jeffster | Jeff & Lester | Buy More musical duo (music validation) |

**Full project documentation** (including Grimes module, Ellie's Dashboard, Beckman CI/CD) available at:
[GitHub Repository](https://github.com/calionestevar/OrionAI)

## Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.

## Support

- GitHub Issues: https://github.com/calionestevar/OrionAI/issues
- Documentation: https://github.com/calionestevar/OrionAI/blob/main/docs
