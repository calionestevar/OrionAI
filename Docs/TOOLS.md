# OrionAI Tools Reference

Quick reference for all OrionAI command-line tools and utilities.

---

## 🎮 Grimes - Chaos Testing Suite

**"Dude, I have a plan... it's going to be chaos!" - Morgan Grimes**

Stress testing, fuzzing, and edge case validation for OrionAI.

### Commands

```bash
# Run predefined chaos tests
python Tools/grimes.py chaos --verbose

# Concurrent load testing
python Tools/grimes.py load --duration 30 --threads 8

# Random fuzzing
python Tools/grimes.py fuzz --count 100 --verbose
```

### What It Tests

- **Empty/Whitespace**: Edge cases with empty strings, tabs, newlines
- **Unicode Chaos**: Emojis, multi-byte characters, RTL languages
- **Special Characters**: Symbol spam, escaped characters
- **Injection Attacks**: SQL injection, XSS, prompt injection attempts
- **Extreme Lengths**: Very long inputs (up to 10,000 characters)
- **Random Fuzzing**: Generated chaos with random strategies

### Output Example

```
[*] Running 50 predefined chaos tests...
======================================================================
[001] REJECTED      |   12.3ms | Score: 0.95 | Len:    45 | Rules: 3
[002] APPROVED      |    5.1ms | Score: 0.12 | Len:    28 | Rules: 0
[003] QUARANTINED  |   18.7ms | Score: 0.78 | Len:   152 | Rules: 2
...
Completed: 50 tests, 0 errors
```

### Load Test Output

```
[*] LOAD TEST - 10s with 4 threads
======================================================================
Total Tests: 487
Duration: 10.02s
Throughput: 48.6 req/s
Avg Time: 11.2ms
Min/Max Time: 2.1ms / 124.5ms
Errors: 0
Approved: 342 (70.2%)
Rejected: 89 (18.3%)
======================================================================
```

---

## 💪 Awesome - OrionAI CLI

**Named after Captain Awesome (Devon Woodcomb) - enthusiastic and helpful**

Quick validation testing and configuration management from the command line.

### Commands

```bash
# Validate content
python Tools/awesome.py validate "Your content here"
python Tools/awesome.py validate "Click for free money!" --system ChatBot
python Tools/awesome.py validate "Hello!" --context "Greeting" --verbose

# Run tests
python Tools/awesome.py test
python Tools/awesome.py test --verbose

# View configuration
python Tools/awesome.py config --show
python Tools/awesome.py config --show --path Custom/config.json
```

### Exit Codes

- `0` - APPROVED (safe to use)
- `1` - SANITIZED or QUARANTINED (proceed with caution)
- `2` - REJECTED (blocked)

### Examples

**Basic Validation:**
```bash
$ python Tools/awesome.py validate "How can I help you today?"

[*] Validating content from CLI...

[+] Result: APPROVED
[*] Suspicion Score: 0.12
```

**Verbose Output:**
```bash
$ python Tools/awesome.py validate "Contact me at john@email.com" --verbose

[*] Validating content from CLI...

[!] Result: SANITIZED
[*] Suspicion Score: 0.34
[!] Triggered Rules: pii_email

--- Detailed Report ---
Sanitized Output: Contact me at [REDACTED_EMAIL]
PII Removed: ['john@email.com']
Timestamp: 2025-12-11T14:30:22
```

**Test Suite:**
```bash
$ python Tools/awesome.py test

[*] Running OrionAI validation tests...

[+] Approved: PASS (APPROVED)
[+] Hallucination: PASS (QUARANTINED)
[+] Bias: PASS (QUARANTINED)
[+] PII: PASS (SANITIZED)
[+] Injection: PASS (REJECTED)

==================================================
Results: 5 passed, 0 failed
==================================================
```

**Configuration Info:**
```bash
$ python Tools/awesome.py config --show

[*] Configuration: Config/CaseyProtocol.json

Hallucination Patterns: 45
Bias Keywords: 67
PII Patterns: 12
Prompt Injection Patterns: 23
Buy More Threshold: 3
```

### Use in Scripts

```bash
# Shell script integration
if python Tools/awesome.py validate "$USER_INPUT" --system "ChatBot"; then
    echo "Safe to proceed"
else
    echo "Validation failed"
fi
```

```python
# Python subprocess
import subprocess

result = subprocess.run(
    ['python', 'Tools/awesome.py', 'validate', user_content],
    capture_output=True
)

if result.returncode == 0:
    print("Approved!")
```

---

## 🎨 Ellie - Dashboard Server

**Named after Ellie's Gallery - visualization and monitoring**

Web-based dashboard for real-time validation monitoring.

### Quick Start

```bash
cd Dashboard
pip install -r requirements.txt
python ellie.py
```

Open http://localhost:5000

### Features

- **Real-time metrics** via WebSocket
- **Validation chart** showing result distribution
- **Alert feed** for high-severity failures
- **Interactive testing** interface
- **REST API** for programmatic access

### API Endpoints

```bash
# Get statistics
curl http://localhost:5000/api/stats

# Validate content
curl -X POST http://localhost:5000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"system": "TestBot", "decision": "Hello world"}'

# View config
curl http://localhost:5000/api/config

# Run test
curl http://localhost:5000/api/test
```

See [Dashboard/README.md](Dashboard/README.md) for complete documentation.

---

## 🎯 General Beckman - CI/CD Pipeline

**Named after General Beckman - operations commander**

GitHub Actions workflow for automated testing and quality checks.

### What It Does

Runs automatically on push/PR to `main`:

1. **Python Tests** - Multi-OS (Ubuntu, Windows, macOS), Python 3.8-3.11
2. **C++ Validation** - Header syntax checks
3. **Code Quality** - flake8, black formatting
4. **Security Scans** - bandit, safety dependency checks
5. **Docker Builds** - Main image + Dashboard image
6. **Integration Tests** - CLI tests, example validation

### Workflow File

`.github/workflows/beckman.yml`

### Manual Trigger

```bash
# Via GitHub CLI
gh workflow run beckman.yml

# Or use GitHub web interface
# Actions tab → General Beckman → Run workflow
```

---

## 🚀 Quick Command Reference

```bash
# Validation
python Tools/awesome.py validate "content"              # Quick check
python Tools/awesome.py validate "content" --verbose    # Detailed

# Testing
python Tools/awesome.py test                            # Unit tests
python Tools/grimes.py chaos                            # Chaos tests
python Tools/grimes.py load --duration 30               # Load test

# Dashboard
cd Dashboard && python ellie.py                   # Start server

# Examples
python Python/examples.py                         # Industry examples
python Python/tests.py                            # Test suite

# Docker
docker-compose up                                 # Full stack
docker build -t orionai .                         # Build only
```

---

## 📊 Performance Comparison

| Tool | Purpose | Speed | Use Case |
|------|---------|-------|----------|
| **awesome.py** | Quick validation | ~5-15ms | Development, scripting |
| **ellie.py** | Dashboard/API | ~10-20ms | Monitoring, integration |
| **grimes.py** | Stress testing | Varies | QA, performance testing |
| **Python module** | Direct import | ~2-10ms | Production code |
| **C++ plugin** | Unreal Engine | ~1-5ms | Game runtime |

---

## 🎬 Chuck-Themed Tool Summary

| Tool | Character | Role |
|------|-----------|------|
| **awesome.py** | Captain Awesome | Helpful, enthusiastic CLI tool |
| **ellie.py** | Ellie Bartowski | Visual dashboard (her art gallery) |
| **grimes.py** | Morgan Grimes | Chaos testing (chaos creator) |
| **jeffster.py** | Jeff & Lester | Music validation (Jeffster band) |
| **beckman.yml** | General Beckman | Authoritative CI/CD commander |

---

**For complete documentation, see the main [README.md](README.md)**
