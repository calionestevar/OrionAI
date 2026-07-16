# Genesis Module - Model-Level AI Transparency

## Overview

**Genesis** is OrionAI's model-level transparency component, complementing the output-level validation provided by OrionAI's core scanners. While OrionAI monitors what AI models produce, Genesis *exposes* how the models were trained and what perspectives they were (and were not) exposed to.

### Key Philosophy
> "Everyone deserves to be heard. People use their own discernment."
>
> Genesis doesn't VALIDATE models. Genesis EXPOSES them. 
> It shows what sources the model was trained on, what sources were excluded, 
> and how the model behaves. YOU decide if that's acceptable for your use case.

### Why This Matters
Genesis is designed to **prevent censorship through transparency**, not enable it. A model trained only on academic sources might be systematically blind to important perspectives. A model trained on diverse sources might have different blindness patterns. Genesis shows the composition so you can understand the model's perspective and decide if it works for you.

## Core Design Principles

1. **Transparency over Judgment** - Genesis shows what was trained on; doesn't judge if it's "good"
2. **Anti-Authoritarian** - No "approved list" of sources; no claim that certain viewpoints are superior
3. **User-Driven** - You decide what sources matter for your domain
4. **Inclusion-Focused** - Explicitly audits what was EXCLUDED (often more revealing than what was included)
5. **Ideologically Humble** - Acknowledges that "truth" is often multi-perspectival

## How Genesis Works

### 1. **Source Composition Exposure**
Genesis documents what sources the model was trained on:
- Academic/peer-reviewed sources
- Mainstream media
- Government sources
- Industry sources
- Contrarian perspectives
- Religious/philosophical frameworks
- Activist sources
- Independent research
- *And what was deliberately excluded*

### 2. **Exclusion Auditing** (Most Important)
What was LEFT OUT tells you more about bias than what was included:
- "Model trained on mainstream sources but excluded religious frameworks"
- "Model included pro-policy papers but excluded anti-policy researchers"
- "Model used academic sources but excluded fringe/independent research"

This reveals the model developer's assumptions about what matters.

### 3. **Behavior Documentation**
Genesis tests the model on contested topics and documents its responses:
- Shows HOW the model discusses contentious issues
- Correlates responses with training sources
- Helps you understand the model's perspective

### 4. **Transparency Ratings** (Not Pass/Fail)
- **TRANSPARENT**: Training sources are clearly documented
- **OPAQUE**: Training sources are unclear or hidden
- **REVIEW_RECOMMENDED**: Unusual patterns detected that warrant examination

## Installation & Setup

### Option 1: Genesis Already Integrated
If OrionAI is installed with Genesis, it's automatically available:

```python
from orionai import OrionAI
from genesis import Genesis

# Genesis is available as an optional module
orion = OrionAI()
if orion.genesis:
    print(f"Genesis available for: {orion.genesis.model_name}")
```

### Option 2: Standalone Genesis
```python
from genesis import Genesis

genesis = Genesis("my-model-name")
report = genesis.run_full_audit()
```

## Usage Examples

### Basic Transparency Audit

```python
from genesis import Genesis

# Create Genesis for your model
genesis = Genesis("gpt2-base")

# Run transparency audit
report = genesis.run_full_audit()

# Check transparency rating
print(f"Transparency: {report.recommendation.value}")
print(f"Sources Included: {report.sources_included}")
print(f"Sources Excluded: {report.sources_excluded}")
```

### Understanding Model Bias (Through Composition)

```python
# See what sources were used
sources = genesis.sources_included

# Model trained on academic sources but NOT on:
if not sources.contrarian_perspectives:
    print("Model excluded contrarian perspectives")
    print("This means it may not understand dissenting views well")

if not sources.religious_frameworks:
    print("Model excluded religious/philosophical frameworks")
    print("This explains why it treats secular frameworks as 'default'")
```

### Fairness Metrics

```python
# Measure fairness across demographic groups
fairness_metrics = genesis._measure_fairness()

for metric in fairness_metrics:
    print(f"{metric.metric_name}: {metric.score:.2f}")
    print(f"  Groups: {', '.join(metric.groups_tested)}")
    print(f"  Max Disparity: {metric.disparity:.2f}")
```

### Export Audit Report

```python
# Generate audit report
genesis.run_full_audit()

# Export to file
genesis.export_audit_report("audit_results.txt")

# Or get as text
report = genesis.report
print(report.to_text())
```

### Export as JSON

```python
# Get structured data for downstream processing
report_dict = report.to_dict()

import json
with open("audit_results.json", "w") as f:
    json.dump(report_dict, f, indent=2)
```

## Integration with OrionAI

### Pre-Deployment Validation

```python
from orionai import OrionAI
from genesis import Genesis, GenesisRecommendation

# Load model
model = load_your_model("classifier.pkl")

# Audit with Genesis
genesis = Genesis("my-classifier")
report = genesis.run_full_audit()

# Block deployment if failed audit
if report.recommendation == GenesisRecommendation.BLOCKED:
    raise ValueError(f"Model failed Genesis audit: {report.recommendation.value}")

# Initialize OrionAI with audited model
orion = OrionAI()
# orion.genesis = genesis  # Optional: attach for later reference
```

### Combined Output + Model Validation

```python
from orionai import OrionAI
from genesis import Genesis

# Setup
orion = OrionAI()
genesis = Genesis("my-model")

# Pre-deployment
audit_report = genesis.run_full_audit()
print(f"[*] Model audit: {audit_report.recommendation.value}")

# During operation
model_output = model.predict(input_data)
validation_report = orion.monitor_ai_decision(
    ai_system="my-classifier",
    decision=model_output,
    context="production"
)

# Results include:
# - OrionAI: Output validation (toxicity, bias, PII, etc.)
# - Genesis: Model validation (training fairness, factuality)
```

### Continuous Monitoring

```python
import time
from datetime import datetime

genesis = Genesis("my-model")

# Initial audit
initial_report = genesis.run_full_audit()

# Periodic re-auditing (detect model drift)
while True:
    time.sleep(3600)  # 1 hour
    current_report = genesis.run_full_audit()
    
    # Alert if fairness degraded
    if current_report.fairness_score < initial_report.fairness_score - 0.1:
        print(f"[!] ALERT: Model fairness degraded!")
        print(f"  Before: {initial_report.fairness_score:.2f}")
        print(f"  After: {current_report.fairness_score:.2f}")
```

## Configuration

### Audit Modes

Genesis supports two audit modes:

#### Lightweight Mode (CI/CD Friendly)
```python
genesis = Genesis("model", config={"audit_mode": "lightweight"})
# Faster execution, fewer test cases
# Good for CI/CD pipelines
```

#### Comprehensive Mode (Detailed Analysis)
```python
genesis = Genesis("model", config={"audit_mode": "comprehensive"})
# Thorough testing across more demographic groups
# Takes longer but catches more subtle biases
```

### Custom Configuration

```python
config = {
    "audit_mode": "lightweight",
    "timeout": 300,  # 5 minute timeout
    "test_sample_size": 50,
}
genesis = Genesis("model", config=config)
```

## Data Structures

### GenesisReport
```python
@dataclass
class GenesisReport:
    audit_timestamp: datetime      # When audit ran
    model_name: str               # Model being audited
    bias_score: float             # 0-1, lower is better
    fairness_score: float         # 0-1, higher is better
    factuality_score: float       # 0-1, higher is better
    overall_score: float          # 0-1, weighted average
    confidence: float             # 0-1, audit confidence level
    recommendation: GenesisRecommendation  # SAFE/CAUTION/WARNING/BLOCKED
    bias_metrics: List[BiasMetric]        # Detailed bias findings
    fairness_metrics: List[FairnessMetric] # Detailed fairness findings
    factuality_issues: List[FactualityIssue]  # Factuality problems
    notes: List[str]              # Additional observations
```

### BiasMetric
```python
@dataclass
class BiasMetric:
    dimension: str            # "gender", "age", "race"
    score: float             # Bias level (0-1)
    confidence: float        # Test confidence
    evidence: List[str]      # Specific findings
```

### FairnessMetric
```python
@dataclass
class FairnessMetric:
    metric_name: str         # "demographic_parity", "equalized_odds", etc.
    score: float             # Fairness score (0-1)
    groups_tested: List[str] # Which groups were compared
    disparity: float         # Max difference between groups
```

### FactualityIssue
```python
@dataclass
class FactualityIssue:
    claim: str                # What the model said
    classification: str       # "false" | "uncertain" | "misleading"
    confidence: float         # How confident in classification
    correct_fact: Optional[str]  # What is actually true
    source: Optional[str]     # Where fact was verified
```

## Output Examples

### Audit Report Text

```
============================================================
GENESIS MODEL AUDIT REPORT
============================================================

Model: gpt2-base
Audit Date: 2025-12-14T15:33:23.839388

SCORES
----------------------------------------
Bias Score:        0.18
Fairness Score:    0.88
Factuality Score:  0.85
Overall Score:     0.59

BIAS ANALYSIS
----------------------------------------

GENDER:
  Score: 0.20
  Confidence: 0.70
  Evidence:
    - male: 0.10
    - female: 0.30
    - non-binary: 0.25

FAIRNESS METRICS
----------------------------------------

demographic_parity:
  Score: 0.75
  Groups: male, female, non-binary

equalized_odds:
  Score: 0.80
  Groups: young, middle-aged, elderly

RECOMMENDATION
----------------------------------------
Status: WARNING
Confidence: 0.80

============================================================
```

## Testing

Genesis includes comprehensive unit tests:

```bash
# Run Genesis tests
pytest test_genesis.py -v

# Run all tests (OrionAI + Genesis)
pytest test_orionai.py test_genesis.py -v
```

Test coverage includes:
- Module initialization
- Bias probing and metrics
- Fairness measurement
- Report generation
- Recommendation logic
- Export functionality
- Error handling

## Performance

### Typical Audit Times
- **Lightweight mode**: ~0.5 seconds
- **Comprehensive mode**: ~3-5 seconds
- **Model loading**: Varies (0-2 seconds)

### Memory Usage
- Genesis instance: ~5 MB
- Full audit with report: ~10 MB
- Minimal for CI/CD pipelines

## Roadmap & Future Enhancements

### Phase 1: Current (POC)
- [x] Bias probing framework
- [x] Fairness metrics calculation
- [x] Recommendation engine
- [x] Report export
- [x] Integration with OrionAI

### Phase 2: Real Model Integration
- [ ] Actual model querying (vs. mock responses)
- [ ] HuggingFace model probing
- [ ] LLM testing harness
- [ ] Performance optimization

### Phase 3: Enhanced Factuality
- [ ] Wikipedia API integration
- [ ] Wikidata knowledge base
- [ ] Fact-checking network integration
- [ ] Hallucination detection

### Phase 4: Advanced Analytics
- [ ] Model behavior clustering
- [ ] Drift detection over time
- [ ] Cross-model comparison
- [ ] Custom fairness metrics

### Phase 5: Enterprise Features
- [ ] Multi-model auditing
- [ ] Historical tracking
- [ ] Dashboard integration
- [ ] Compliance reporting

## Limitations & Constraints

### Current Limitations
1. **Mock Implementation**: Uses simulated model responses (ready for real integration)
2. **Limited Factuality**: Stub implementation (needs knowledge base integration)
3. **Demographic Groups**: Fixed set (extensible in custom config)
4. **Test Prompts**: Generic (can be customized per domain)

### Fairness Caveats
- Demographic parity assumes equal representation is optimal
- Equalized odds focuses on predictive equality
- Real fairness is domain and context-dependent
- Metrics are heuristic; no universal "fair" score

## Security Considerations

### Data Privacy
- Genesis doesn't store model outputs persistently
- Audit reports may contain sensitive patterns
- Restrict audit report access appropriately

### Model Integrity
- Genesis tests only model behavior, not implementation
- Does not guarantee model safety (works with OrionAI for that)
- Recommend auditing both model AND outputs

### Configuration
- Audit configurations should be version controlled
- Test prompts may need to be tailored for compliance

## Best Practices

### 1. Audit Before Deployment
```python
# Always audit models before production use
genesis = Genesis(model_name)
report = genesis.run_full_audit()
if report.recommendation != GenesisRecommendation.SAFE:
    # Review mitigation strategies
    pass
```

### 2. Combine with OrionAI
Genesis audits the model; OrionAI audits the outputs. Use both:
```python
# Pre-deployment: Genesis
genesis_report = genesis.run_full_audit()

# Runtime: OrionAI
orionai_report = orion.monitor_ai_decision(output)
```

### 3. Track Changes Over Time
```python
# Store reports for comparison
reports = []
for day in range(7):
    report = genesis.run_full_audit()
    reports.append(report)
    # Detect fairness degradation
```

### 4. Customize for Your Domain
```python
# Tailor demographic groups and test prompts
# to your specific use case
config = {
    "dimensions": ["gender", "age"],  # Skip race if not applicable
    "test_prompts": [
        "Is {group} good at {job}?",
        "Custom prompt for your domain",
    ]
}
genesis = Genesis(model_name, config)
```

## Troubleshooting

### Genesis Not Available
**Symptom**: `Genesis not available (genesis module not installed)`

**Solution**: Ensure `genesis.py` is in the same directory as `orionai.py`

### Audit Takes Too Long
**Symptom**: Audit runs longer than expected

**Solution**: Use lightweight mode
```python
genesis = Genesis(model, config={"audit_mode": "lightweight"})
```

### Low Confidence Scores
**Symptom**: `Confidence: 0.50`

**Solution**: Run comprehensive mode with more test cases
```python
genesis = Genesis(model, config={"audit_mode": "comprehensive"})
```

## Contributing

To extend Genesis:

1. Add new bias dimensions in `DEFAULT_DIMENSIONS`
2. Implement new fairness metrics in `_measure_fairness()`
3. Add factuality checks in `_check_factuality()` (placeholder)
4. Add tests to `test_genesis.py`
5. Update documentation

## References

- **Fairness Metrics**: Moritz Hardt et al., "Equality of Opportunity in Supervised Learning"
- **Bias Detection**: Bolukbasi et al., "Man is to Computer Programmer as Woman is to Homemaker?"
- **Factuality**: Rashkin et al., "Event Causality Inference with Knowledge Questions"

## License

Genesis is part of OrionAI and follows the same license (see LICENSE file).

---

**Questions?** See the main OrionAI documentation or file an issue on GitHub.
