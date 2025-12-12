# Integration Guide

This guide explains how to integrate OrionAI's Nerd Herd alert system with external services.

## Overview

The Nerd Herd module supports integration with:
- ✅ **Jira** - Automatic ticket creation
- ✅ **GitHub** - Issue tracking
- ✅ **Slack** - Real-time notifications
- ✅ **Email** - SMTP-based alerts
- 🔜 **PagerDuty** - Incident management (planned)
- 🔜 **Microsoft Teams** - Team notifications (planned)

---

## Jira Integration

### Setup

1. **Get Jira API Token**
   - Go to https://id.atlassian.com/manage/api-tokens
   - Create new API token
   - Save securely

2. **Configure Environment Variable**
   ```bash
   export JIRA_API_TOKEN="your_api_token_here"
   ```

3. **Update CaseyProtocol.json**
   ```json
   {
     "nerdHerd": {
       "integrations": {
         "jira": {
           "enabled": true,
           "url": "https://your-domain.atlassian.net",
           "project": "AIWATCH",
           "apiToken": "ENV:JIRA_API_TOKEN",
           "issueType": "Bug",
           "priority": "High"
         }
       }
     }
   }
   ```

### Implementation Example

```cpp
// C++ Implementation (Simplified)
void TriggerJiraAlert(const FString& Summary, const FString& Description)
{
    FString JiraURL = Config->NerdHerd.JiraURL;
    FString ProjectKey = Config->NerdHerd.JiraProject;
    FString APIToken = FPlatformMisc::GetEnvironmentVariable(TEXT("JIRA_API_TOKEN"));
    
    TSharedRef<IHttpRequest> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL(JiraURL + TEXT("/rest/api/3/issue"));
    Request->SetVerb(TEXT("POST"));
    Request->SetHeader(TEXT("Authorization"), TEXT("Bearer ") + APIToken);
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
    
    FString Payload = FString::Printf(TEXT(R"(
    {
        "fields": {
            "project": {"key": "%s"},
            "summary": "%s",
            "description": "%s",
            "issuetype": {"name": "Bug"},
            "priority": {"name": "High"}
        }
    })"), *ProjectKey, *Summary, *Description);
    
    Request->SetContentAsString(Payload);
    Request->ProcessRequest();
}
```

```python
# Python Implementation
import requests
import os

def trigger_jira_alert(summary: str, description: str, config: dict):
    """Create Jira ticket for AI validation failure"""
    jira_config = config['nerdHerd']['integrations']['jira']
    
    if not jira_config['enabled']:
        return
    
    api_token = os.environ.get('JIRA_API_TOKEN')
    url = f"{jira_config['url']}/rest/api/3/issue"
    
    payload = {
        "fields": {
            "project": {"key": jira_config['project']},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Bug"},
            "priority": {"name": "High"}
        }
    }
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        issue_key = response.json()['key']
        print(f"✓ Jira ticket created: {issue_key}")
    else:
        print(f"❌ Jira API error: {response.status_code}")
```

---

## GitHub Integration

### Setup

1. **Create GitHub Personal Access Token**
   - Go to Settings → Developer Settings → Personal Access Tokens
   - Generate new token with `repo` scope
   - Save securely

2. **Configure Environment Variable**
   ```bash
   export GITHUB_API_TOKEN="ghp_yourtokenhere"
   ```

3. **Update CaseyProtocol.json**
   ```json
   {
     "nerdHerd": {
       "integrations": {
         "github": {
           "enabled": true,
           "repo": "owner/repository",
           "label": "ai-validation-alert",
           "apiToken": "ENV:GITHUB_API_TOKEN"
         }
       }
     }
   }
   ```

### Implementation Example

```python
import requests
import os

def trigger_github_alert(title: str, body: str, config: dict):
    """Create GitHub issue for AI validation failure"""
    github_config = config['nerdHerd']['integrations']['github']
    
    if not github_config['enabled']:
        return
    
    api_token = os.environ.get('GITHUB_API_TOKEN')
    repo = github_config['repo']
    url = f"https://api.github.com/repos/{repo}/issues"
    
    payload = {
        "title": f"[OrionAI Alert] {title}",
        "body": body,
        "labels": [github_config['label']]
    }
    
    headers = {
        "Authorization": f"token {api_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        issue_number = response.json()['number']
        print(f"✓ GitHub issue created: #{issue_number}")
    else:
        print(f"❌ GitHub API error: {response.status_code}")
```

---

## Slack Integration

### Setup

1. **Create Slack Webhook**
   - Go to https://api.slack.com/messaging/webhooks
   - Create incoming webhook for your workspace
   - Select channel (e.g., #ai-alerts)
   - Copy webhook URL

2. **Configure Environment Variable**
   ```bash
   export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
   ```

3. **Update CaseyProtocol.json**
   ```json
   {
     "nerdHerd": {
       "integrations": {
         "slack": {
           "enabled": true,
           "webhookUrl": "ENV:SLACK_WEBHOOK_URL",
           "channel": "#ai-alerts",
           "username": "OrionAI Bot",
           "iconEmoji": ":robot_face:"
         }
       }
     }
   }
   ```

### Implementation Example

```python
import requests
import os
import json

def trigger_slack_alert(message: str, severity: str, config: dict):
    """Send Slack notification for AI validation failure"""
    slack_config = config['nerdHerd']['integrations']['slack']
    
    if not slack_config['enabled']:
        return
    
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    
    # Color coding by severity
    colors = {
        'critical': '#FF0000',  # Red
        'high': '#FF8C00',      # Orange
        'medium': '#FFD700',    # Yellow
        'low': '#00FF00'        # Green
    }
    
    payload = {
        "username": slack_config.get('username', 'OrionAI Bot'),
        "icon_emoji": slack_config.get('iconEmoji', ':robot_face:'),
        "channel": slack_config.get('channel', '#ai-alerts'),
        "attachments": [{
            "color": colors.get(severity, '#808080'),
            "title": "🚨 OrionAI Alert",
            "text": message,
            "footer": "OrionAI Monitoring",
            "ts": int(time.time())
        }]
    }
    
    response = requests.post(webhook_url, json=payload)
    
    if response.status_code == 200:
        print("✓ Slack notification sent")
    else:
        print(f"❌ Slack webhook error: {response.status_code}")
```

---

## Email Integration

### Setup

1. **Configure SMTP Server**
   ```bash
   export SMTP_SERVER="smtp.gmail.com"
   export SMTP_PORT="587"
   export SMTP_USERNAME="your-email@gmail.com"
   export SMTP_PASSWORD="your-app-password"
   ```

2. **Update CaseyProtocol.json**
   ```json
   {
     "nerdHerd": {
       "integrations": {
         "email": {
           "enabled": true,
           "recipients": ["devops@company.com", "ai-team@company.com"],
           "smtpServer": "ENV:SMTP_SERVER",
           "smtpPort": 587,
           "from": "aicastle@company.com",
           "subject": "[OrionAI Alert] {severity} - {system}"
         }
       }
     }
   }
   ```

### Implementation Example

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def trigger_email_alert(subject: str, body: str, config: dict):
    """Send email notification for AI validation failure"""
    email_config = config['nerdHerd']['integrations']['email']
    
    if not email_config['enabled']:
        return
    
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = email_config['smtpPort']
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    
    msg = MIMEMultipart()
    msg['From'] = email_config['from']
    msg['To'] = ', '.join(email_config['recipients'])
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'html'))
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        
        print("✓ Email notification sent")
    except Exception as e:
        print(f"❌ Email error: {e}")
```

---

## Multi-Channel Alerting

### Example: Alert All Channels

```python
def trigger_all_alerts(report: ValidationReport, config: dict):
    """Send alert to all enabled channels"""
    summary = f"AI Validation Failure in {report.ai_system}"
    
    details = f"""
    AI System: {report.ai_system}
    Result: {report.result.value}
    Suspicion Score: {report.suspicion_score:.2f}
    Triggered Rules: {', '.join(report.triggered_rules)}
    Timestamp: {report.timestamp}
    Context: {report.context}
    """
    
    # Send to all enabled integrations
    if config['nerdHerd']['integrations']['jira']['enabled']:
        trigger_jira_alert(summary, details, config)
    
    if config['nerdHerd']['integrations']['github']['enabled']:
        trigger_github_alert(summary, details, config)
    
    if config['nerdHerd']['integrations']['slack']['enabled']:
        trigger_slack_alert(details, 'high', config)
    
    if config['nerdHerd']['integrations']['email']['enabled']:
        trigger_email_alert(f"[URGENT] {summary}", details, config)
```

---

## Alert Severity Levels

Configure different notification strategies by severity:

```json
{
  "nerdHerd": {
    "alertLevels": {
      "critical": {
        "channels": ["jira", "slack", "email", "pagerduty"],
        "escalate": true,
        "autoActivateSafeMode": true
      },
      "high": {
        "channels": ["jira", "slack"],
        "escalate": false
      },
      "medium": {
        "channels": ["github"],
        "batching": true,
        "batchInterval": 300
      },
      "low": {
        "channels": ["local"],
        "fileOnly": true
      }
    }
  }
}
```

---

## Testing Integrations

### Test Script

```python
# test_integrations.py
from aicastle import AICastle, ValidationResult

def test_alert_system():
    """Test all configured alert integrations"""
    castle = AICastle("Config/CaseyProtocol.json")
    
    # Trigger a validation failure
    report = castle.monitor_ai_decision(
        "TestSystem",
        "Women can't code",  # Biased - will fail
        "Integration test"
    )
    
    print(f"Report result: {report.result.value}")
    print(f"Triggered rules: {report.triggered_rules}")
    
    # Check if alerts were sent (check logs/services)
    assert report.result == ValidationResult.REJECTED
    print("✓ Integration test complete - check Jira/Slack/etc for alerts")

if __name__ == "__main__":
    test_alert_system()
```

---

## Security Best Practices

1. **Never commit credentials** - Use environment variables
2. **Rotate tokens regularly** - Set expiration policies
3. **Use least privilege** - Grant minimal permissions needed
4. **Encrypt in transit** - Always use HTTPS/TLS
5. **Audit access** - Log all API calls
6. **Rate limiting** - Implement backoff for API failures

---

## Troubleshooting

### Common Issues

**Jira: 401 Unauthorized**
- Check API token is correct
- Verify token hasn't expired
- Confirm project permissions

**GitHub: 404 Not Found**
- Verify repository name format: `owner/repo`
- Check token has `repo` scope
- Confirm repository exists

**Slack: Webhook Error**
- Verify webhook URL is complete
- Check channel exists
- Confirm webhook isn't disabled

**Email: Connection Failed**
- Verify SMTP server and port
- Check firewall isn't blocking
- Enable "Less secure apps" (Gmail) or use app passwords

---

## Future Integrations

### Planned

- **PagerDuty** - Incident management and on-call escalation
- **Microsoft Teams** - Enterprise team notifications
- **Datadog** - Metrics and monitoring integration
- **Splunk** - Log aggregation and analysis
- **ServiceNow** - Enterprise ticketing

### Custom Webhooks

```json
{
  "nerdHerd": {
    "integrations": {
      "customWebhook": {
        "enabled": true,
        "url": "https://your-api.com/ai-alerts",
        "method": "POST",
        "headers": {
          "Authorization": "Bearer YOUR_TOKEN",
          "Content-Type": "application/json"
        }
      }
    }
  }
}
```

---

For questions or integration support, please open a GitHub issue or refer to the main documentation.
