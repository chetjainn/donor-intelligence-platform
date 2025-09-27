from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='../static', template_folder='../templates')
CORS(app)

# Simple in-memory data store for demo
contacts = []
tasks = []
campaigns = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/contacts', methods=['GET', 'POST'])
def handle_contacts():
    if request.method == 'POST':
        contact = request.json
        contact['id'] = len(contacts) + 1
        contact['created_at'] = datetime.now().isoformat()
        contacts.append(contact)
        return jsonify(contact), 201
    return jsonify(contacts)

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        task = request.json
        task['id'] = len(tasks) + 1
        task['created_at'] = datetime.now().isoformat()
        tasks.append(task)
        return jsonify(task), 201
    return jsonify(tasks)

@app.route('/api/analytics/dashboard')
def analytics_dashboard():
    return jsonify({
        'total_donations': 0,
        'total_donors': len(contacts),
        'average_donation': 0,
        'retention_rate': 0,
        'donation_trends': [],
        'donor_segments': []
    })

@app.route('/api/campaigns', methods=['GET', 'POST'])
def handle_campaigns():
    if request.method == 'POST':
        campaign = request.json
        campaign['id'] = len(campaigns) + 1
        campaign['created_at'] = datetime.now().isoformat()
        campaigns.append(campaign)
        return jsonify(campaign), 201
    return jsonify(campaigns)

@app.route('/api/grants')
def get_grants():
    return jsonify([])

@app.route('/api/events')
def get_events():
    return jsonify([])

@app.route('/api/wealth-screening')
def get_wealth_screening():
    return jsonify([])

@app.route('/api/reports')
def get_reports():
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
