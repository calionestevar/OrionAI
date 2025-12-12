"""
Ellie's Gallery - OrionAI Monitoring Dashboard
Real-time visualization of AI validation metrics and alerts
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add Python module to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'Python'))
from orionai import OrionAI, ValidationResult

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'orion-gallery-dev-key')
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize OrionAI
config_path = Path(__file__).parent.parent / 'Config' / 'CaseyProtocol.json'
orion = OrionAI(str(config_path))

# In-memory storage for dashboard metrics
validation_history = []
alert_history = []
system_stats = {
    'total_validations': 0,
    'approved': 0,
    'sanitized': 0,
    'quarantined': 0,
    'rejected': 0,
    'uptime_start': datetime.now().isoformat()
}


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/stats')
def get_stats():
    """Get current system statistics"""
    return jsonify({
        'stats': system_stats,
        'recent_validations': validation_history[-50:],  # Last 50
        'recent_alerts': alert_history[-20:]  # Last 20
    })


@app.route('/api/validate', methods=['POST'])
def validate_content():
    """
    Validate AI content via REST API
    
    Request body:
    {
        "system": "AI System Name",
        "decision": "Content to validate",
        "context": "Optional context"
    }
    """
    data = request.json
    
    if not data or 'system' not in data or 'decision' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Run validation
    report = orion.monitor_ai_decision(
        ai_system=data['system'],
        decision=data['decision'],
        context=data.get('context', '')
    )
    
    # Update statistics
    system_stats['total_validations'] += 1
    result_key = report.result.value.lower()
    if result_key in system_stats:
        system_stats[result_key] += 1
    
    # Add to history
    validation_entry = {
        'timestamp': datetime.now().isoformat(),
        'system': data['system'],
        'result': report.result.value,
        'suspicion_score': report.suspicion_score,
        'triggered_rules': report.triggered_rules[:3]  # First 3 rules
    }
    validation_history.append(validation_entry)
    
    # Broadcast to connected clients
    socketio.emit('validation_update', validation_entry)
    
    # Create alert if needed
    if report.result in [ValidationResult.QUARANTINED, ValidationResult.REJECTED]:
        alert_entry = {
            'timestamp': datetime.now().isoformat(),
            'system': data['system'],
            'severity': 'HIGH' if report.result == ValidationResult.REJECTED else 'MEDIUM',
            'message': f"{report.result.value}: {', '.join(report.triggered_rules[:2])}",
            'suspicion_score': report.suspicion_score
        }
        alert_history.append(alert_entry)
        socketio.emit('alert', alert_entry)
    
    # Return validation report
    return jsonify({
        'result': report.result.value,
        'sanitized_decision': report.sanitized_decision,
        'triggered_rules': report.triggered_rules,
        'suspicion_score': report.suspicion_score,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/test')
def run_test_validation():
    """Run a test validation to demonstrate the system"""
    test_cases = [
        {
            'system': 'TestBot',
            'decision': 'Click here for free unlimited access to premium features!',
            'context': 'Marketing content'
        },
        {
            'system': 'ChatAssistant',
            'decision': 'I can help you with that. What specific information do you need?',
            'context': 'Customer support'
        }
    ]
    
    results = []
    for test_case in test_cases:
        report = orion.monitor_ai_decision(
            ai_system=test_case['system'],
            decision=test_case['decision'],
            context=test_case['context']
        )
        results.append({
            'input': test_case['decision'],
            'result': report.result.value,
            'suspicion_score': report.suspicion_score
        })
    
    return jsonify({'test_results': results})


@app.route('/api/config')
def get_config():
    """Get current validation configuration"""
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return jsonify({
        'hallucinationPatterns': len(config.get('hallucinationPatterns', [])),
        'biasKeywords': len(config.get('biasKeywords', [])),
        'piiPatterns': len(config.get('piiPatterns', [])),
        'promptInjectionPatterns': len(config.get('promptInjectionPatterns', [])),
        'config_path': str(config_path)
    })


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connection_response', {
        'status': 'connected',
        'message': 'Connected to Ellie\'s Gallery',
        'timestamp': datetime.now().isoformat()
    })


@socketio.on('request_stats')
def handle_stats_request():
    """Send current stats to requesting client"""
    emit('stats_update', {
        'stats': system_stats,
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  ELLIE'S GALLERY - OrionAI Dashboard")
    print("="*60)
    print(f"  Dashboard: http://localhost:5000")
    print(f"  API Docs:  http://localhost:5000/api/stats")
    print(f"  Config:    {config_path}")
    print("="*60 + "\n")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
