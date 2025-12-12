---
name: Bug Report
about: Report a bug or issue with OrionAI
title: '[BUG] '
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Initialize OrionAI with '...'
2. Call method '....'
3. Pass content '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Actual behavior**
What actually happened.

**Code Sample**
```python
# Minimal code sample that reproduces the issue
from orionai import OrionAI

orion = OrionAI("Config/CaseyProtocol.json")
# ... your code here
```

**Environment:**
 - OS: [e.g., Windows 11, Ubuntu 22.04, macOS 14]
 - Python Version: [e.g., 3.11.5]
 - OrionAI Version: [e.g., 1.0.0]
 - Integration: [e.g., Standalone Python, Unreal Engine 5.3, Docker]

**Validation Report (if applicable)**
```json
{
  "result": "...",
  "suspicion_score": 0.0,
  "triggered_rules": []
}
```

**Additional context**
Add any other context about the problem here (screenshots, logs, etc.)

**Config Details**
- Using custom CaseyProtocol.json: [Yes/No]
- Ring Intel enabled: [Yes/No]
- Nerd Herd integrations: [e.g., Slack, GitHub, Jira]
