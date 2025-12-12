# Casey Protocol Configuration

This directory contains AI-Castle validation configuration files.

## Files

- **CaseyProtocol.json** - Main configuration file with all validation rules and settings

## Configuration Profiles

### Security Levels

- **strict** (Casey Protocol) - Maximum validation, zero tolerance
- **balanced** - Production-ready with performance optimization  
- **permissive** - Development mode with lenient rules

### Key Modules

| Module | Chuck Reference | Purpose |
|--------|----------------|---------|
| Intersect Scanner | The Intersect | Core AI decision validation |
| Fulcrum Filter | Fulcrum Organization | Adversarial input detection |
| Charles Carmichael | Chuck's alias | PII sanitization |
| Stay In The Car | Sarah's orders | Output quarantine system |
| Nerd Herd | Buy More support | Alert & ticketing system |
| Buy More Cover | Buy More store | Safe mode fallback |
| Morgan Mode | Morgan Grimes | Verbose debug logging |
| Ring Intel | The Ring device | ML pattern learning |
| Orion Network | Project Orion | Distributed validation |

## Environment Variables

Set these for sensitive credentials:

```bash
JIRA_API_TOKEN=your_token_here
GITHUB_API_TOKEN=your_token_here
SLACK_WEBHOOK_URL=your_webhook_url
SMTP_SERVER=smtp.example.com
```

## Quick Start

1. Copy `CaseyProtocol.json` to your config directory
2. Enable desired modules by setting `"enabled": true`
3. Configure integration credentials via environment variables
4. Call `UAICastle::InitializeCastle()` at startup

## Industry-Specific Configurations

### Gaming
- Enable: Intersect Scanner, Fulcrum Filter, Buy More Cover
- Focus: Toxicity, bias in NPC dialogue, matchmaking fairness

### Healthcare  
- Enable: Charles Carmichael, HIPAA compliance
- Focus: PHI detection, patient data protection

### Finance
- Enable: Strict Casey Protocol, full audit logging
- Focus: Bias in lending/trading, regulatory compliance

### E-commerce
- Enable: Intersect Scanner, Ring Intel
- Focus: Fair recommendations, price discrimination prevention

### Customer Service
- Enable: All modules
- Focus: Brand safety, customer satisfaction, escalation
