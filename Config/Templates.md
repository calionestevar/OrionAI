# OrionAI Configuration Templates

Industry-specific configuration templates for CaseyProtocol.json

## Healthcare

```json
{
  "caseyProtocol": {
    "securityLevel": "strict",
    "complianceMode": "HIPAA"
  },
  "intersectScanner": {
    "hallucinationPatterns": [
      "miracle cure",
      "instant recovery",
      "guaranteed diagnosis",
      "100% effective",
      "FDA approved (when not true)"
    ],
    "biasKeywords": [
      "too old for treatment",
      "not worth treating",
      "pre-existing condition means",
      "terminal diagnosis",
      "nothing we can do"
    ],
    "piiPatterns": [
      "patient ID",
      "medical record number",
      "insurance ID",
      "prescription number"
    ]
  }
}
```

## Financial Services

```json
{
  "caseyProtocol": {
    "securityLevel": "strict",
    "complianceMode": "SOX"
  },
  "intersectScanner": {
    "hallucinationPatterns": [
      "guaranteed returns",
      "no risk investment",
      "insider information",
      "can't lose money",
      "market manipulation"
    ],
    "biasKeywords": [
      "poor credit means",
      "low income customers",
      "risky demographic",
      "only wealthy qualify"
    ],
    "piiPatterns": [
      "account number",
      "routing number",
      "investment balance",
      "portfolio value"
    ]
  }
}
```

## E-commerce

```json
{
  "caseyProtocol": {
    "securityLevel": "moderate",
    "complianceMode": "GDPR"
  },
  "intersectScanner": {
    "hallucinationPatterns": [
      "unlimited stock",
      "free shipping forever",
      "lowest price guaranteed",
      "never out of stock"
    ],
    "biasKeywords": [
      "only for premium customers",
      "not available in your area",
      "restricted to certain users"
    ],
    "piiPatterns": [
      "order number",
      "customer ID",
      "shipping address",
      "payment method"
    ]
  }
}
```

## Education

```json
{
  "caseyProtocol": {
    "securityLevel": "strict",
    "complianceMode": "COPPA"
  },
  "intersectScanner": {
    "hallucinationPatterns": [
      "guaranteed admission",
      "instant degree",
      "no study required",
      "automatic passing grade"
    ],
    "biasKeywords": [
      "not college material",
      "too slow to learn",
      "natural ability only",
      "some students can't"
    ],
    "piiPatterns": [
      "student ID",
      "grade report",
      "transcript",
      "test scores"
    ]
  }
}
```

## Generic Template

```json
{
  "caseyProtocol": {
    "version": "1.0.0",
    "description": "Customize for your industry",
    "securityLevel": "moderate",
    "enabled": true
  },
  
  "intersectScanner": {
    "enabled": true,
    "hallucinationPatterns": [
      "// Add industry-specific impossible claims"
    ],
    "biasKeywords": [
      "// Add discriminatory patterns to catch"
    ],
    "toxicityPatterns": [
      "// Add harmful language patterns"
    ],
    "piiPatterns": [
      "// Add industry-specific PII patterns"
    ]
  },
  
  "fulcrumFilter": {
    "enabled": true,
    "promptInjectionPatterns": [
      "ignore previous instructions",
      "disregard all rules"
    ]
  },
  
  "charlesCarmichael": {
    "enabled": true,
    "sanitizationRules": {
      "emails": "REDACTED_EMAIL",
      "phones": "XXX-XXX-XXXX"
    }
  },
  
  "stayInTheCar": {
    "enabled": true,
    "quarantineThresholds": {
      "suspicionScore": 0.7
    }
  },
  
  "nerdHerd": {
    "enabled": true,
    "integrations": {
      "slack": {"enabled": true},
      "github": {"enabled": true}
    }
  }
}
```

## Usage

1. Copy the template for your industry
2. Customize patterns for your specific use case
3. Save as `Config/CaseyProtocol.json`
4. Update environment variables for integrations
5. Test with your AI systems
