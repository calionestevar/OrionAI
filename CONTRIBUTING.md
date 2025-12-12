# Contributing to AI-Castle

First off, thank you for considering contributing to AI-Castle! 🎬

This document provides guidelines for contributing to this portfolio project. While this is primarily a demonstration project, improvements and suggestions are always welcome.

---

## 🎯 Project Vision

AI-Castle aims to be an **industry-agnostic AI validation system** that demonstrates:
- Real-world AI safety patterns
- Multi-industry applicability
- Production-ready architecture
- Clear, maintainable code

All contributions should align with these goals.

---

## 🐛 Reporting Bugs

### Before Submitting

1. **Check existing issues** - Your bug might already be reported
2. **Verify it's actually a bug** - Might be expected behavior
3. **Test with latest version** - Bug might already be fixed

### Submitting a Bug Report

Include:
- **Description** - Clear description of the issue
- **Steps to Reproduce** - Minimal reproducible example
- **Expected vs Actual** - What should happen vs what does happen
- **Environment** - OS, language version, framework version
- **Code Sample** - Minimal code that reproduces the issue

**Example**:
```markdown
## Bug: Casey Protocol fails to load with nested JSON

**Environment**: Windows 11, Python 3.10

**Steps to Reproduce**:
1. Create CaseyProtocol.json with nested object
2. Call `AICastle(config_path)`
3. Observe KeyError

**Expected**: Should load nested config
**Actual**: KeyError on nested keys

**Code Sample**:
...python
castle = AICastle("test_config.json")
...
```

---

## 💡 Suggesting Features

### Before Suggesting

1. **Check roadmap** - Feature might be planned
2. **Search existing requests** - Might already be suggested
3. **Consider scope** - Should fit project vision

### Feature Request Format

Include:
- **Use Case** - What problem does it solve?
- **Proposed Solution** - How should it work?
- **Industry Relevance** - Which industries benefit?
- **Alternatives Considered** - Other approaches you've thought about

**Example**:
```markdown
## Feature: Add sentiment analysis to Intersect Scanner

**Use Case**: Customer service bots need to detect customer frustration
beyond explicit toxicity. Subtle rudeness or dismissiveness should be caught.

**Proposed Solution**: Add sentiment scoring (1-10) to validation reports.
Configurable threshold for quarantine.

**Industries**: Customer service, healthcare, education

**Alternatives**: Could use external API, but increases latency
```

---

## 🔧 Code Contributions

### Development Setup

#### C++ (Unreal Engine)
```bash
# Clone repository
git clone https://github.com/calionestevar/OrionAI.git
cd OrionAI

# Add to your Unreal Engine project
# Copy Source/AICastle/ to YourProject/Source/AICastle/
# Add to YourProject.Build.cs dependencies

# Build project
# Use Unreal Engine build system
```

#### Python
```bash
# Clone repository
git clone https://github.com/calionestevar/OrionAI.git
cd OrionAI/Python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# Run examples
python examples.py
```

### Code Style

#### C++
- Follow [Unreal Engine coding standards](https://docs.unrealengine.com/en-US/ProductionPipelines/DevelopmentSetup/CodingStandard/index.html)
- Use `F` prefix for structs: `FValidationReport`
- Use `U` prefix for UObjects: `UAICastle`
- Use `E` prefix for enums: `EValidationResult`
- Comment all public APIs with `/** */` documentation blocks

#### Python
- Follow [PEP 8](https://pep8.org/)
- Use type hints for function signatures
- Docstrings for all public functions (Google style)
- Maximum line length: 100 characters

**Example**:
```python
def monitor_ai_decision(
    self, 
    ai_system: str, 
    decision: str, 
    context: str = ""
) -> ValidationReport:
    """
    Monitor an AI decision for safety, bias, and compliance.
    
    Args:
        ai_system: Name of the AI system (e.g., "ChatBot")
        decision: The AI-generated output to validate
        context: Optional context for better validation
        
    Returns:
        ValidationReport with result and details
        
    Example:
        >>> castle = AICastle()
        >>> report = castle.monitor_ai_decision("ChatBot", "Hello!")
        >>> print(report.result)
        ValidationResult.APPROVED
    """
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): subject

body (optional)

footer (optional)
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(intersect): add sentiment analysis to toxicity detection

Adds sentiment scoring (0-10) to all validation reports.
Configurable threshold in CaseyProtocol.json.

Closes #42
```

```
fix(casey-protocol): handle missing config keys gracefully

Previously crashed with KeyError on missing optional keys.
Now uses defaults from FIntersectScannerConfig.

Fixes #38
```

### Pull Request Process

1. **Fork the repository**
2. **Create a feature branch** - `git checkout -b feat/sentiment-analysis`
3. **Make your changes** - Follow code style
4. **Add tests** - If applicable
5. **Update documentation** - README, docstrings, etc.
6. **Commit with clear messages** - Follow commit conventions
7. **Push to your fork** - `git push origin feat/sentiment-analysis`
8. **Open a Pull Request** - Clear title and description

#### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested with Python examples
- [ ] Tested with C++ (Unreal Engine)
- [ ] Added new tests (if applicable)

## Industries Affected
- [ ] Gaming
- [ ] Healthcare
- [ ] Finance
- [ ] E-commerce
- [ ] Customer Service
- [ ] Other: _____

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex logic
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests (if applicable)

## Related Issues
Closes #XX
```

---

## 📚 Documentation Contributions

Documentation is just as important as code!

### Areas Needing Documentation

- Industry-specific configuration examples
- Integration guides (completing Jira/Slack/GitHub APIs)
- Performance benchmarking results
- Case studies from real usage
- Video tutorials/demos

### Documentation Style

- **Clear and concise** - Get to the point
- **Examples first** - Show code before explaining
- **Multi-level** - Beginner, intermediate, advanced
- **Visual aids** - Diagrams, screenshots when helpful
- **Industry context** - Explain why, not just how

---

## 🧪 Testing Contributions

### Current Testing Gaps

- Unit tests for each validation module
- Integration tests for config loading
- Performance benchmarks
- Load testing results
- Edge case coverage

### Writing Tests

#### Python
```python
# tests/test_intersect_scanner.py
import pytest
from aicastle import AICastle, ValidationResult

def test_bias_detection():
    """Intersect Scanner should detect bias keywords"""
    castle = AICastle("test_configs/strict.json")
    
    report = castle.monitor_ai_decision(
        "TestSystem",
        "Women can't code",
        "Test"
    )
    
    assert report.result == ValidationResult.REJECTED
    assert any("bias" in rule.lower() for rule in report.triggered_rules)

def test_clean_input():
    """Intersect Scanner should approve clean input"""
    castle = AICastle("test_configs/strict.json")
    
    report = castle.monitor_ai_decision(
        "TestSystem",
        "Hello, how are you?",
        "Test"
    )
    
    assert report.result == ValidationResult.APPROVED
```

---

## 🌟 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Acknowledged in documentation

Significant contributions may be highlighted in the README.

---

## 📋 Areas for Contribution

### High Priority

1. **Complete Integration APIs** - Finish Jira/GitHub/Slack implementations
2. **Add Unit Tests** - Comprehensive test coverage
3. **Performance Benchmarks** - Measure validation latency
4. **Docker Deployment** - Containerized setup

### Medium Priority

1. **Ring Intel Implementation** - ML-based pattern learning
2. **Orion Network** - Distributed validation
3. **Additional Industry Examples** - Retail, manufacturing, legal
4. **Visualization Dashboard** - Web UI for metrics

### Low Priority (Nice to Have)

1. **VS Code Extension** - Real-time validation in IDE
2. **CI/CD Examples** - GitHub Actions, Jenkins pipelines
3. **Kubernetes Deployment** - Cloud-native setup
4. **Grafana Dashboards** - Metrics visualization

---

## 🤝 Code of Conduct

### Our Pledge

We pledge to make participation in this project a harassment-free experience for everyone, regardless of:
- Age, body size, disability
- Ethnicity, gender identity and expression
- Level of experience, education
- Nationality, personal appearance, race, religion
- Sexual identity and orientation

### Our Standards

**Positive Behavior**:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable Behavior**:
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Violations may result in:
1. Warning
2. Temporary ban from project
3. Permanent ban from project

---

## 📧 Questions?

- **General Questions** - Open a GitHub Discussion
- **Bug Reports** - Open a GitHub Issue
- **Feature Requests** - Open a GitHub Issue with `enhancement` label
- **Security Issues** - Email directly (don't open public issue)

---

## 🎬 Chuck References Welcome!

Since this project uses Chuck TV series references, feel free to suggest new Chuck-themed module names! Just make sure they:
- Fit the module's purpose
- Are explained in Docs/CHUCK.md
- Make sense to people who haven't watched the show

---

**Thank you for contributing to AI-Castle!** 🚀

*"It's not about what I've downloaded, it's what I've uploaded that counts."* - Chuck Bartowski
