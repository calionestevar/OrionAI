# Security Policy

## Supported Versions

OrionAI is currently in active development. Security updates are provided for:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in OrionAI, please report it privately:

1. **Email**: calionestevar@protonmail.com
2. **Subject**: `[SECURITY] OrionAI Vulnerability Report`
3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### What to expect

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Fix Timeline**: Critical issues within 2 weeks, others within 30 days
- **Disclosure**: Coordinated disclosure after fix is released

## Security Best Practices

When using OrionAI in production:

### Configuration Security
- **Never commit secrets** to version control
- Use environment variables for API tokens (Slack, GitHub, Jira)
- Rotate API tokens regularly
- Restrict file permissions on `CaseyProtocol.json`

### API Integration Security
- **Validate SSL certificates** for webhook endpoints
- Use HTTPS for all external integrations
- Implement rate limiting on validation endpoints
- Sanitize all inputs before logging

### Dashboard Security
- Change default Flask `SECRET_KEY` in production
- Enable authentication for public deployments
- Use HTTPS/TLS for production deployments
- Implement CORS restrictions
- Regular dependency updates: `pip install --upgrade -r requirements.txt`

### Docker Security
- Don't run containers as root
- Use specific image tags, not `latest`
- Scan images regularly: `docker scan orionai:latest`
- Limit container resources in docker-compose.yml

### PII Handling
- OrionAI sanitizes PII but **does not encrypt** it
- Implement encryption at rest for quarantine files
- Configure log rotation to prevent PII accumulation
- Comply with GDPR/HIPAA requirements for your jurisdiction

## Known Security Considerations

### Regular Expression Denial of Service (ReDoS)
- OrionAI uses regex patterns for validation
- Complex patterns on large inputs may cause delays
- Implement timeout limits for validation calls
- Monitor CPU usage on high-traffic deployments

### Input Validation
- OrionAI validates AI output, not user input
- Combine with input sanitization libraries
- Don't rely solely on OrionAI for XSS/SQL injection prevention

### ML Model Security (Ring Intel)
- Hugging Face models downloaded from public sources
- Verify model checksums before production use
- Keep transformers library updated
- Monitor model performance for drift/poisoning

## Dependency Security

OrionAI relies on:
- Python 3.7+ standard library
- Optional: transformers, torch (Ring Intel)
- Optional: flask, flask-socketio (Dashboard)

Run security audits:
```bash
pip install safety
safety check --file Python/requirements.txt
```

## Compliance

OrionAI is designed to help with:
- **GDPR** - PII detection and removal
- **HIPAA** - Healthcare data protection patterns
- **SOX** - Financial compliance validation
- **COPPA** - Education sector safety

**Note**: OrionAI is a validation tool, not a complete compliance solution. Consult legal counsel for regulatory requirements.

## Updates

Security updates are published via:
- GitHub Security Advisories
- Release notes with `[SECURITY]` prefix
- Email to registered users (if applicable)

Subscribe to releases: https://github.com/calionestevar/OrionAI/releases

---

**Last Updated**: December 11, 2025
