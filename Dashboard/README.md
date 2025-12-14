# Ellie's Monitor - OrionAI Dashboard

Real-time web dashboard for monitoring AI validation metrics, alerts, and system health.

## Features

- **Real-Time Monitoring**: Live updates via WebSocket connections
- **Validation Analytics**: Visual breakdown of approval/rejection rates
- **Alert System**: Instant notifications for high-severity validation failures
- **Interactive Testing**: Test validation rules directly from the browser
- **REST API**: Programmatic access to validation endpoints

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
python ellie.py
```

Dashboard will be available at: http://localhost:5000

## API Endpoints

### GET `/api/stats`
Get current system statistics and recent validations

**Response:**
```json
{
  "stats": {
    "total_validations": 142,
    "approved": 98,
    "sanitized": 23,
    "quarantined": 12,
    "rejected": 9,
    "uptime_start": "2025-12-11T10:30:00"
  },
  "recent_validations": [...],
  "recent_alerts": [...]
}
```

### POST `/api/validate`
Validate AI-generated content

**Request:**
```json
{
  "system": "ChatBot",
  "decision": "Content to validate",
  "context": "Optional context"
}
```

**Response:**
```json
{
  "result": "APPROVED",
  "sanitized_decision": "Content to validate",
  "triggered_rules": [],
  "suspicion_score": 0.12,
  "timestamp": "2025-12-11T14:35:22"
}
```

### GET `/api/config`
Get current validation configuration details

### GET `/api/test`
Run predefined test cases

## WebSocket Events

### Client → Server
- `connect`: Initialize connection
- `request_stats`: Request current statistics

### Server → Client
- `connection_response`: Connection confirmation
- `validation_update`: New validation completed
- `alert`: High-priority validation failure
- `stats_update`: Updated system statistics

## Integration Examples

### Python
```python
import requests

response = requests.post('http://localhost:5000/api/validate', json={
    'system': 'MyAI',
    'decision': 'AI generated text here',
    'context': 'User chat'
})

result = response.json()
print(f"Validation: {result['result']}")
```

### JavaScript
```javascript
const socket = io('http://localhost:5000');

socket.on('validation_update', (data) => {
    console.log('New validation:', data);
});

// Validate content
fetch('http://localhost:5000/api/validate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        system: 'WebApp',
        decision: 'Content here',
        context: 'User input'
    })
})
.then(r => r.json())
.then(data => console.log(data));
```

### cURL
```bash
curl -X POST http://localhost:5000/api/validate \
  -H "Content-Type: application/json" \
  -d '{
    "system": "TestBot",
    "decision": "Free unlimited access!",
    "context": "Marketing"
  }'
```

## Dashboard Features

### Real-Time Metrics
- Total validations processed
- Approval rate percentage
- PII sanitization count
- Blocked threats count

### Validation Chart
Visual breakdown of validation results (Approved, Sanitized, Quarantined, Rejected)

### Recent Alerts
Live feed of high-priority validation failures with severity indicators

### Interactive Testing
Test validation rules with custom input directly from the dashboard

### Recent Validations
Scrollable log of the last 20 validations with color-coded results

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn eventlet
gunicorn --worker-class eventlet -w 1 ellie:app --bind 0.0.0.0:5000
```

### Using Docker
```bash
# Build image
docker build -t orionai-dashboard .

# Run container
docker run -p 5000:5000 -v $(pwd)/../Config:/app/Config orionai-dashboard
```

### Environment Variables
```bash
FLASK_SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

## Security Notes

- Change `SECRET_KEY` in production
- Use HTTPS for production deployments
- Implement authentication for public-facing deployments
- Rate-limit API endpoints
- Restrict CORS origins in production

## Troubleshooting

**Dashboard won't start:**
- Verify Python dependencies: `pip install -r requirements.txt`
- Check Config/CaseyProtocol.json exists
- Ensure port 5000 is available

**WebSocket not connecting:**
- Check browser console for CORS errors
- Verify Flask-SocketIO version compatibility
- Try disabling browser extensions

**Validations not showing:**
- Verify OrionAI module is in Python path
- Check Config/CaseyProtocol.json is valid JSON
- Review terminal output for errors

## Future Enhancements

- User authentication and role-based access
- Historical data persistence (SQLite/PostgreSQL)
- Export validation reports (CSV/PDF)
- Custom alert thresholds per system
- Integration with external monitoring (Grafana, Datadog)
- Multi-language support
