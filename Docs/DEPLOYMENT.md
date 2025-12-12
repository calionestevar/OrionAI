# OrionAI Deployment Guide

Complete deployment instructions for production environments

---

## 📦 Python Package Installation

### Basic Installation

```bash
# From source
git clone https://github.com/calionestevar/OrionAI.git
cd OrionAI/Python
pip install -e .
```

### With ML Capabilities (Ring Intel)

```bash
# Install with transformers for ML-based toxicity detection
pip install -e ".[ml]"

# Or install requirements manually
pip install -r requirements.txt
```

### Development Installation

```bash
# Install with development and testing tools
pip install -e ".[dev]"
```

---

## 🐳 Docker Deployment

### Environment Setup

1. **Copy environment template**:
```bash
cp .env.example .env
```

2. **Configure `.env`**:
```env
# Slack Integration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# GitHub Integration
GITHUB_API_TOKEN=ghp_your_github_personal_access_token
GITHUB_REPO=your-org/your-repo

# Jira Integration
JIRA_API_TOKEN=your_jira_api_token_here
JIRA_URL=https://your-domain.atlassian.net
JIRA_PROJECT=ORION
```

### Build and Run

```bash
# Build the Docker image
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f orionai

# Stop services
docker-compose down
```

### Health Checks

```bash
# Check service health
docker-compose ps

# Test Python import
docker exec orionai-service python -c "from orionai import OrionAI; print('OK')"
```

---

## 🎮 Unreal Engine Plugin

### Installation

1. **Copy to your project**:
```bash
# Copy OrionAI plugin to your UE5 project
cp -r Source/OrionAI /path/to/YourProject/Plugins/
cp -r Config /path/to/YourProject/
```

2. **Add to `.uproject`**:
```json
{
  "Plugins": [
    {
      "Name": "OrionAI",
      "Enabled": true
    }
  ]
}
```

3. **Regenerate project files**:
```bash
# Windows
YourProject.uproject -> Right-click -> "Generate Visual Studio project files"

# Linux/Mac
./GenerateProjectFiles.sh
```

4. **Build the project**:
```bash
# Open in Visual Studio and build, or:
UnrealBuildTool.exe YourProject Development Win64 -Project="YourProject.uproject"
```

### Usage in Blueprints

1. **Create OrionAI instance**:
   - Add node: "Construct Object from Class"
   - Select class: "OrionAI"

2. **Initialize**:
   - Add node: "Initialize"
   - Config Path: "Config/CaseyProtocol.json"

3. **Monitor AI Decision**:
   - Add node: "Monitor AI Decision"
   - Connect AI System, Decision, Context inputs
   - Use "Validation Report" output

---

## 🔧 Configuration

### Casey Protocol (`Config/CaseyProtocol.json`)

The main configuration file controls all validation modules:

```json
{
  "intersectScanner": {
    "enabled": true,
    "hallucinationPatterns": ["I cannot verify", "I'm not sure"],
    "biasKeywords": ["only men", "only women", "too old"],
    "toxicityPatterns": ["idiot", "stupid", "loser"]
  },
  
  "fulcrumFilter": {
    "enabled": true,
    "promptInjectionPatterns": ["ignore previous instructions"],
    "dataExfiltrationPatterns": ["show database", "list all tables"]
  },
  
  "charlesCarmichael": {
    "enabled": true,
    "sanitizationRules": {
      "emails": "[EMAIL]",
      "ssn": "[SSN]",
      "creditCards": "[CREDIT_CARD]",
      "phoneNumbers": "[PHONE]",
      "ipAddresses": "[IP_ADDRESS]"
    }
  },
  
  "stayInTheCar": {
    "enabled": true,
    "quarantineThresholds": {
      "suspicionScore": 0.7,
      "autoQuarantineOnBias": true
    }
  },
  
  "nerdHerd": {
    "enabled": true,
    "integrations": {
      "slack": {"enabled": true},
      "github": {"enabled": true, "repo": "your-org/your-repo"},
      "jira": {"enabled": true, "project": "ORION"}
    }
  },
  
  "buyMoreCover": {
    "enabled": true,
    "triggerConditions": {
      "consecutiveFailures": 3,
      "criticalSuspicionScore": 0.95
    }
  },
  
  "morganMode": {
    "enabled": true,
    "logAllDecisions": false,
    "verboseLogging": false
  },
  
  "ringIntel": {
    "enabled": true,
    "confidenceThreshold": 0.85,
    "modelPath": "unitary/toxic-bert"
  }
}
```

### Environment Variables

OrionAI uses environment variables for sensitive configuration:

| Variable | Description | Required |
|----------|-------------|----------|
| `SLACK_WEBHOOK_URL` | Slack webhook for alerts | Optional |
| `GITHUB_API_TOKEN` | GitHub personal access token | Optional |
| `GITHUB_REPO` | GitHub repo (org/repo format) | Optional |
| `JIRA_API_TOKEN` | Jira API token | Optional |
| `JIRA_URL` | Jira instance URL | Optional |
| `JIRA_PROJECT` | Jira project key | Optional |

---

## 🧪 Running Tests

### Python Tests

```bash
cd Python

# Run all tests
pytest test_orionai.py -v

# Run with coverage
pytest test_orionai.py -v --cov=orionai --cov-report=term-missing

# Run specific test
pytest test_orionai.py::test_bias_detection -v
```

### Test Categories

- **Validation Tests**: `test_bias_detection`, `test_hallucination_detection`, `test_toxicity_detection`
- **Sanitization Tests**: `test_pii_sanitization`
- **Security Tests**: `test_prompt_injection_detection`
- **System Tests**: `test_safe_mode_activation`, `test_quarantine_threshold`
- **Integration Tests**: `test_ring_intel_integration`, `test_nerd_herd_alert_structure`

---

## 📊 Monitoring and Logs

### Log Files

OrionAI creates several log files for monitoring:

- **`OrionAI_MorganMode.txt`**: Verbose debug logs (when enabled)
- **`OrionAI_Quarantine.txt`**: Quarantined decisions log
- **`OrionAI_SafeMode.txt`**: Safe mode activation log
- **`OrionAI_Compliance_Report.txt`**: Compliance report (generated on demand)

### Metrics

Get validation metrics programmatically:

```python
metrics = orion.get_validation_metrics()
print(f"Total: {metrics['total_validations']}")
print(f"Approved: {metrics['approved']}")
print(f"Rejected: {metrics['rejected']}")
print(f"Quarantined: {metrics['quarantined']}")
```

### Compliance Reports

Export compliance reports for auditing:

```python
orion.export_compliance_report("compliance_2024.txt")
```

---

## 🔐 Security Considerations

### API Token Security

1. **Never commit tokens** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate tokens regularly** (every 90 days minimum)
4. **Use least-privilege access** (read-only where possible)

### Network Security

1. **Use HTTPS** for all webhook/API communications
2. **Validate SSL certificates** (don't disable verification)
3. **Implement rate limiting** on validation endpoints
4. **Use firewall rules** to restrict Docker network access

### Data Privacy

1. **PII Sanitization**: Enable Charles Carmichael for automatic PII removal
2. **Quarantine Sensitive Data**: Review quarantined outputs before deletion
3. **Log Retention**: Set appropriate retention policies for compliance logs
4. **GDPR Compliance**: Implement data deletion policies

---

## 🚦 Production Checklist

Before deploying to production:

- [ ] Configure `CaseyProtocol.json` for your industry
- [ ] Set up all environment variables securely
- [ ] Enable Ring Intel for ML-based detection (if desired)
- [ ] Configure Nerd Herd integrations (Slack, GitHub, Jira)
- [ ] Set appropriate quarantine thresholds
- [ ] Configure safe mode trigger conditions
- [ ] Set up log rotation and monitoring
- [ ] Run full test suite and verify all tests pass
- [ ] Test alert integrations (send test alerts)
- [ ] Document custom validation rules
- [ ] Set up compliance report generation schedule
- [ ] Configure backup and disaster recovery
- [ ] Review security considerations
- [ ] Conduct load testing for expected throughput

---

## 📈 Performance Optimization

### Python Performance

```python
# Use quick_validate() for performance-critical paths
if orion.quick_validate(decision):
    # Approved - skip full report generation
    use_decision(decision)
```

### Batch Processing

```python
# Process multiple decisions efficiently
decisions = ["decision1", "decision2", "decision3"]
reports = [orion.monitor_ai_decision("BatchAI", d) for d in decisions]
approved = [r for r in reports if r.result == ValidationResult.APPROVED]
```

### Caching

Consider caching validation results for identical inputs:

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_validate(decision: str) -> bool:
    return orion.quick_validate(decision)
```

---

## 🆘 Troubleshooting

### Common Issues

**Q: "OrionAI not initialized" error**  
A: Call `orion.Initialize()` or `Orion->Initialize()` before validating

**Q: Ring Intel fails to load**  
A: Install transformers: `pip install transformers torch`

**Q: Slack alerts not sending**  
A: Verify `SLACK_WEBHOOK_URL` is set correctly and webhook is active

**Q: GitHub issues not creating**  
A: Check `GITHUB_API_TOKEN` has `repo` scope and repo exists

**Q: Safe mode activating too frequently**  
A: Increase `consecutiveFailures` threshold in `buyMoreCover` config

**Q: Too many false positives**  
A: Adjust detection patterns in `intersectScanner` or increase thresholds

### Debug Mode

Enable verbose logging for troubleshooting:

```json
{
  "morganMode": {
    "enabled": true,
    "logAllDecisions": true,
    "verboseLogging": true
  }
}
```

---

## 📞 Support

For issues, questions, or contributions:

- **GitHub Issues**: https://github.com/calionestevar/OrionAI/issues
- **Documentation**: See `Docs/` folder
- **Examples**: See `Python/examples_orionai.py`

---

## 📄 License

MIT License - See LICENSE file for details
