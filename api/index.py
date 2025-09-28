from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import random
import json

app = Flask(__name__, template_folder='../templates')
CORS(app)

# Sample data - defined as functions to ensure fresh data on each call
def get_contacts():
    return [
        {
            'id': 1,
            'name': 'Sarah Johnson',
            'email': 'sarah.johnson@email.com',
            'type': 'donor',
            'phone': '(555) 123-4567',
            'total_donated': 2500.00,
            'last_donation': '2024-08-15',
            'engagement_score': 85,
            'created_at': '2024-01-15'
        },
        {
            'id': 2,
            'name': 'Michael Chen',
            'email': 'michael.chen@email.com',
            'type': 'prospect',
            'phone': '(555) 234-5678',
            'total_donated': 0.00,
            'last_donation': None,
            'engagement_score': 65,
            'created_at': '2024-02-20'
        },
        {
            'id': 3,
            'name': 'Emily Rodriguez',
            'email': 'emily.rodriguez@email.com',
            'type': 'volunteer',
            'phone': '(555) 345-6789',
            'total_donated': 150.00,
            'last_donation': '2024-07-10',
            'engagement_score': 92,
            'created_at': '2024-01-08'
        },
        {
            'id': 4,
            'name': 'David Thompson',
            'email': 'david.thompson@email.com',
            'type': 'board',
            'phone': '(555) 456-7890',
            'total_donated': 5000.00,
            'last_donation': '2024-09-01',
            'engagement_score': 98,
            'created_at': '2023-12-01'
        },
        {
            'id': 5,
            'name': 'Lisa Wang',
            'email': 'lisa.wang@email.com',
            'type': 'donor',
            'phone': '(555) 567-8901',
            'total_donated': 750.00,
            'last_donation': '2024-08-28',
            'engagement_score': 78,
            'created_at': '2024-03-12'
        }
    ]

def get_tasks():
    return [
        {
            'id': 1,
            'title': 'Follow up with Sarah Johnson',
            'description': 'Thank her for recent donation and discuss upcoming gala',
            'priority': 'high',
            'status': 'pending',
            'contact_id': 1,
            'due_date': '2024-09-30',
            'created_at': '2024-09-25'
        },
        {
            'id': 2,
            'title': 'Prepare grant proposal for Education Foundation',
            'description': 'Complete application for $50,000 education grant',
            'priority': 'high',
            'status': 'in_progress',
            'contact_id': None,
            'due_date': '2024-10-15',
            'created_at': '2024-09-20'
        },
        {
            'id': 3,
            'title': 'Schedule meeting with Michael Chen',
            'description': 'Initial prospect meeting to discuss our mission',
            'priority': 'medium',
            'status': 'pending',
            'contact_id': 2,
            'due_date': '2024-10-05',
            'created_at': '2024-09-22'
        },
        {
            'id': 4,
            'title': 'Update donor database',
            'description': 'Import new contacts from recent event',
            'priority': 'low',
            'status': 'pending',
            'contact_id': None,
            'due_date': '2024-10-10',
            'created_at': '2024-09-24'
        }
    ]

def get_campaigns():
    return [
        {
            'id': 1,
            'name': 'Annual Giving Campaign 2024',
            'type': 'appeal',
            'status': 'active',
            'subject': 'Help Us Reach Our 2024 Goal',
            'sent_count': 1250,
            'open_rate': 24.5,
            'click_rate': 3.2,
            'revenue': 15750.00,
            'created_at': '2024-09-01'
        },
        {
            'id': 2,
            'name': 'Monthly Newsletter - September',
            'type': 'newsletter',
            'status': 'completed',
            'subject': 'September Updates from Our Organization',
            'sent_count': 2100,
            'open_rate': 32.1,
            'click_rate': 5.8,
            'revenue': 0.00,
            'created_at': '2024-09-15'
        },
        {
            'id': 3,
            'name': 'Gala Invitation 2024',
            'type': 'event',
            'status': 'scheduled',
            'subject': 'You\'re Invited: Annual Gala 2024',
            'sent_count': 0,
            'open_rate': 0,
            'click_rate': 0,
            'revenue': 0.00,
            'created_at': '2024-09-20'
        }
    ]

def get_grants():
    return [
        {
            'id': 1,
            'foundation': 'Education Excellence Foundation',
            'amount': 50000.00,
            'status': 'in_progress',
            'deadline': '2024-10-15',
            'probability': 75,
            'program': 'Youth Education Initiative',
            'contact_person': 'Dr. Amanda Foster',
            'notes': 'Strong alignment with our mission. Previous relationship.',
            'created_at': '2024-08-01'
        },
        {
            'id': 2,
            'foundation': 'Community Health Grant Program',
            'amount': 25000.00,
            'status': 'submitted',
            'deadline': '2024-11-30',
            'probability': 60,
            'program': 'Health & Wellness Outreach',
            'contact_person': 'Mark Stevens',
            'notes': 'New opportunity. Competitive but good fit.',
            'created_at': '2024-09-10'
        },
        {
            'id': 3,
            'foundation': 'Technology for Good Foundation',
            'amount': 75000.00,
            'status': 'research',
            'deadline': '2024-12-01',
            'probability': 40,
            'program': 'Digital Literacy Program',
            'contact_person': 'Jennifer Liu',
            'notes': 'Requires significant tech component. Exploring partnership.',
            'created_at': '2024-09-15'
        }
    ]

def get_events():
    return [
        {
            'id': 1,
            'name': 'Annual Fundraising Gala',
            'date': '2024-11-15',
            'time': '18:00',
            'venue': 'Grand Ballroom, Downtown Hotel',
            'capacity': 300,
            'registered': 127,
            'ticket_price': 150.00,
            'revenue_goal': 45000.00,
            'current_revenue': 19050.00,
            'status': 'active',
            'created_at': '2024-07-01'
        },
        {
            'id': 2,
            'name': 'Community Volunteer Day',
            'date': '2024-10-12',
            'time': '09:00',
            'venue': 'Central Park Community Center',
            'capacity': 100,
            'registered': 78,
            'ticket_price': 0.00,
            'revenue_goal': 0.00,
            'current_revenue': 0.00,
            'status': 'active',
            'created_at': '2024-08-15'
        },
        {
            'id': 3,
            'name': 'Donor Appreciation Lunch',
            'date': '2024-12-05',
            'time': '12:00',
            'venue': 'Riverside Restaurant',
            'capacity': 50,
            'registered': 12,
            'ticket_price': 0.00,
            'revenue_goal': 0.00,
            'current_revenue': 0.00,
            'status': 'planning',
            'created_at': '2024-09-01'
        }
    ]

def get_wealth_screenings():
    return [
        {
            'id': 1,
            'contact_id': 2,
            'contact_name': 'Michael Chen',
            'estimated_capacity': 10000.00,
            'confidence_level': 'medium',
            'wealth_indicators': ['Real Estate Holdings', 'Business Ownership'],
            'giving_history': 'Limited public giving history',
            'interests': ['Education', 'Technology'],
            'recommended_ask': 2500.00,
            'next_steps': 'Schedule cultivation meeting',
            'screened_date': '2024-09-20'
        },
        {
            'id': 2,
            'contact_id': 1,
            'contact_name': 'Sarah Johnson',
            'estimated_capacity': 5000.00,
            'confidence_level': 'high',
            'wealth_indicators': ['Professional Income', 'Investment Portfolio'],
            'giving_history': 'Consistent donor to similar organizations',
            'interests': ['Health', 'Education', 'Environment'],
            'recommended_ask': 3000.00,
            'next_steps': 'Invite to major donor event',
            'screened_date': '2024-09-18'
        }
    ]

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return jsonify({
        'message': 'Flask app is working!', 
        'timestamp': datetime.now().isoformat(),
        'status': 'success'
    })

# Feature 1: Today View - AI-prioritized daily tasks and workflow management
@app.route('/api/dashboard')
def get_dashboard():
    contacts = get_contacts()
    campaigns = get_campaigns()
    tasks = get_tasks()
    grants = get_grants()
    events = get_events()
    
    total_donations = sum(contact['total_donated'] for contact in contacts)
    total_donors = len([c for c in contacts if c['total_donated'] > 0])
    avg_donation = total_donations / total_donors if total_donors > 0 else 0
    
    active_campaigns = len([c for c in campaigns if c['status'] == 'active'])
    total_campaign_revenue = sum(campaign['revenue'] for campaign in campaigns)
    
    pending_tasks = len([t for t in tasks if t['status'] == 'pending'])
    high_priority_tasks = len([t for t in tasks if t['priority'] == 'high'])
    
    return jsonify({
        'total_contacts': len(contacts),
        'total_donors': total_donors,
        'total_donations': total_donations,
        'average_donation': avg_donation,
        'active_campaigns': active_campaigns,
        'campaign_revenue': total_campaign_revenue,
        'pending_tasks': pending_tasks,
        'high_priority_tasks': high_priority_tasks,
        'total_grants': len(grants),
        'grant_value': sum(grant['amount'] for grant in grants),
        'upcoming_events': len([e for e in events if e['status'] == 'active']),
        'event_registrations': sum(event['registered'] for event in events)
    })

# Feature 2: Contact Management - Complete donor and prospect database with CRUD operations
@app.route('/api/contacts', methods=['GET', 'POST'])
def handle_contacts():
    if request.method == 'GET':
        return jsonify(get_contacts())
    
    elif request.method == 'POST':
        data = request.get_json()
        contacts = get_contacts()
        new_contact = {
            'id': len(contacts) + 1,
            'name': data.get('name'),
            'email': data.get('email'),
            'type': data.get('type'),
            'phone': data.get('phone', ''),
            'total_donated': 0.00,
            'last_donation': None,
            'engagement_score': random.randint(50, 100),
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        return jsonify(new_contact), 201

# Feature 3: Task Management - Custom task creation, editing, and tracking system
@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        return jsonify(get_tasks())
    
    elif request.method == 'POST':
        data = request.get_json()
        tasks = get_tasks()
        new_task = {
            'id': len(tasks) + 1,
            'title': data.get('title'),
            'description': data.get('description', ''),
            'priority': data.get('priority', 'medium'),
            'status': 'pending',
            'contact_id': data.get('contact_id'),
            'due_date': data.get('due_date'),
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        return jsonify(new_task), 201

# Feature 4: Analytics Dashboard - Real-time donor insights and performance metrics
@app.route('/api/analytics/dashboard')
def get_dashboard_analytics():
    contacts = get_contacts()
    campaigns = get_campaigns()
    tasks = get_tasks()
    grants = get_grants()
    events = get_events()
    
    total_donations = sum(contact['total_donated'] for contact in contacts)
    total_donors = len([c for c in contacts if c['total_donated'] > 0])
    avg_donation = total_donations / total_donors if total_donors > 0 else 0
    
    active_campaigns = len([c for c in campaigns if c['status'] == 'active'])
    total_campaign_revenue = sum(campaign['revenue'] for campaign in campaigns)
    
    pending_tasks = len([t for t in tasks if t['status'] == 'pending'])
    high_priority_tasks = len([t for t in tasks if t['priority'] == 'high'])
    
    # Generate sample trend data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
    donation_trends = [1200, 1500, 1800, 2100, 1900, 2300, 2600, 2200, 2800]
    
    # Donor segments
    donor_segments = [
        {'segment': 'Major Donors', 'count': 12, 'total': 45000},
        {'segment': 'Regular Donors', 'count': 45, 'total': 18500},
        {'segment': 'New Donors', 'count': 23, 'total': 5200},
        {'segment': 'Lapsed Donors', 'count': 18, 'total': 0}
    ]
    
    return jsonify({
        'total_contacts': len(contacts),
        'total_donors': total_donors,
        'total_donations': total_donations,
        'average_donation': avg_donation,
        'active_campaigns': active_campaigns,
        'campaign_revenue': total_campaign_revenue,
        'pending_tasks': pending_tasks,
        'high_priority_tasks': high_priority_tasks,
        'total_grants': len(grants),
        'grant_value': sum(grant['amount'] for grant in grants),
        'upcoming_events': len([e for e in events if e['status'] == 'active']),
        'event_registrations': sum(event['registered'] for event in events),
        'donation_trends': donation_trends,
        'donor_segments': donor_segments,
        'retention_rate': 78.5
    })

# Feature 5: Grant Management - Complete grant pipeline tracking and deadline management
@app.route('/api/grants', methods=['GET', 'POST'])
def handle_grants():
    if request.method == 'GET':
        return jsonify(get_grants())
    
    elif request.method == 'POST':
        data = request.get_json()
        grants = get_grants()
        new_grant = {
            'id': len(grants) + 1,
            'foundation': data.get('foundation'),
            'amount': data.get('amount'),
            'status': 'research',
            'deadline': data.get('deadline'),
            'probability': data.get('probability', 50),
            'program': data.get('program'),
            'contact_person': data.get('contact_person'),
            'notes': data.get('notes', ''),
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        return jsonify(new_grant), 201

# Feature 6: Event Management - Full event coordination with volunteer and registration tracking
@app.route('/api/events', methods=['GET', 'POST'])
def handle_events():
    if request.method == 'GET':
        return jsonify(get_events())
    
    elif request.method == 'POST':
        data = request.get_json()
        events = get_events()
        new_event = {
            'id': len(events) + 1,
            'name': data.get('name'),
            'date': data.get('date'),
            'time': data.get('time'),
            'venue': data.get('venue'),
            'capacity': data.get('capacity', 100),
            'registered': 0,
            'ticket_price': data.get('ticket_price', 0.00),
            'revenue_goal': data.get('revenue_goal', 0.00),
            'current_revenue': 0.00,
            'status': 'planning',
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        return jsonify(new_event), 201

# Feature 7: Wealth Screening - AI-powered prospect research and capacity analysis
@app.route('/api/wealth-screenings', methods=['GET', 'POST'])
def handle_wealth_screenings():
    if request.method == 'GET':
        return jsonify(get_wealth_screenings())
    
    elif request.method == 'POST':
        data = request.get_json()
        screenings = get_wealth_screenings()
        new_screening = {
            'id': len(screenings) + 1,
            'contact_id': data.get('contact_id'),
            'contact_name': data.get('contact_name'),
            'estimated_capacity': data.get('estimated_capacity'),
            'confidence_level': data.get('confidence_level', 'medium'),
            'wealth_indicators': data.get('wealth_indicators', []),
            'giving_history': data.get('giving_history', ''),
            'interests': data.get('interests', []),
            'recommended_ask': data.get('recommended_ask'),
            'next_steps': data.get('next_steps', ''),
            'screened_date': datetime.now().strftime('%Y-%m-%d')
        }
        return jsonify(new_screening), 201

# Feature 8: Communication Hub - Email campaign management with performance tracking
@app.route('/api/campaigns', methods=['GET', 'POST'])
def handle_campaigns():
    if request.method == 'GET':
        return jsonify(get_campaigns())
    
    elif request.method == 'POST':
        data = request.get_json()
        campaigns = get_campaigns()
        new_campaign = {
            'id': len(campaigns) + 1,
            'name': data.get('name'),
            'type': data.get('type', 'newsletter'),
            'status': 'draft',
            'subject': data.get('subject'),
            'sent_count': 0,
            'open_rate': 0,
            'click_rate': 0,
            'revenue': 0.00,
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        return jsonify(new_campaign), 201

# Feature 9: Reporting Dashboard - Impact reporting and donor stewardship
@app.route('/api/reports')
def get_reports():
    contacts = get_contacts()
    campaigns = get_campaigns()
    grants = get_grants()
    events = get_events()
    
    # Impact metrics
    total_impact = {
        'total_raised': sum(contact['total_donated'] for contact in contacts),
        'grants_secured': sum(grant['amount'] for grant in grants if grant['status'] == 'submitted'),
        'events_hosted': len([e for e in events if e['status'] == 'completed']),
        'volunteers_engaged': sum(event['registered'] for event in events),
        'campaigns_sent': sum(campaign['sent_count'] for campaign in campaigns)
    }
    
    # Donor stewardship data
    stewardship = {
        'thank_you_letters': 45,
        'impact_reports': 12,
        'personal_visits': 8,
        'recognition_events': 3
    }
    
    return jsonify({
        'impact_metrics': total_impact,
        'stewardship_activities': stewardship,
        'report_generated': datetime.now().isoformat()
    })

# Feature 10: Bulk Upload System
@app.route('/api/bulk-upload', methods=['POST'])
def bulk_upload():
    # Simulate bulk upload processing
    data = request.get_json() or {}
    upload_type = data.get('type', 'contacts')
    
    return jsonify({
        'message': f'Bulk upload of {upload_type} initiated successfully!',
        'status': 'processing',
        'upload_id': f'upload_{random.randint(1000, 9999)}',
        'estimated_completion': '2-3 minutes'
    })

@app.route('/api/bulk-upload/status/<upload_id>')
def bulk_upload_status(upload_id):
    return jsonify({
        'upload_id': upload_id,
        'status': 'completed',
        'records_processed': random.randint(50, 200),
        'records_imported': random.randint(45, 190),
        'errors': random.randint(0, 5)
    })

# Feature 11: Settings & User Management
@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    if request.method == 'GET':
        return jsonify({
            'organization_name': 'Sample Nonprofit Organization',
            'email_signature': 'Best regards,\nFundraising Team',
            'default_currency': 'USD',
            'email_notifications': True,
            'ai_features_enabled': True,
            'user_roles': ['fundraiser', 'manager', 'admin'],
            'data_retention_days': 365,
            'backup_frequency': 'daily'
        })
    
    elif request.method == 'POST':
        data = request.get_json()
        return jsonify({
            'message': 'Settings updated successfully',
            'settings': data,
            'updated_at': datetime.now().isoformat()
        })

@app.route('/api/users')
def get_users():
    return jsonify([
        {
            'id': 1,
            'name': 'John Smith',
            'email': 'john@nonprofit.org',
            'role': 'admin',
            'last_login': '2024-09-27',
            'status': 'active'
        },
        {
            'id': 2,
            'name': 'Jane Doe',
            'email': 'jane@nonprofit.org',
            'role': 'fundraiser',
            'last_login': '2024-09-26',
            'status': 'active'
        },
        {
            'id': 3,
            'name': 'Mike Johnson',
            'email': 'mike@nonprofit.org',
            'role': 'manager',
            'last_login': '2024-09-25',
            'status': 'active'
        }
    ])

# Feature 12: Platform Admin Dashboard
@app.route('/api/admin/dashboard')
def get_admin_dashboard():
    return jsonify({
        'system_health': {
            'status': 'healthy',
            'uptime': '99.9%',
            'response_time': '120ms',
            'error_rate': '0.1%'
        },
        'usage_stats': {
            'total_users': 25,
            'active_users_today': 18,
            'api_calls_today': 1247,
            'storage_used': '2.3GB'
        },
        'recent_activities': [
            {'action': 'User login', 'user': 'jane@nonprofit.org', 'time': '10 minutes ago'},
            {'action': 'Contact added', 'user': 'john@nonprofit.org', 'time': '25 minutes ago'},
            {'action': 'Campaign sent', 'user': 'mike@nonprofit.org', 'time': '1 hour ago'}
        ]
    })

# Feature 13: AI-powered features
@app.route('/api/ai/prioritize-tasks')
def ai_prioritize_tasks():
    tasks = get_tasks()
    
    # AI-powered task prioritization
    prioritized_tasks = sorted(tasks, key=lambda x: (
        {'high': 3, 'medium': 2, 'low': 1}[x['priority']], 
        x['created_at']
    ), reverse=True)
    
    return jsonify({
        'prioritized_tasks': prioritized_tasks,
        'ai_insights': [
            'Focus on high-value donor follow-ups first',
            'Grant deadlines approaching - prioritize applications',
            'Schedule prospect meetings for maximum impact'
        ],
        'optimization_score': 87
    })

@app.route('/api/ai/draft-email', methods=['POST'])
def ai_draft_email():
    data = request.get_json()
    contact_name = data.get('contact_name', 'Valued Supporter')
    email_type = data.get('type', 'thank_you')
    
    # AI email drafting templates
    templates = {
        'thank_you': f"Dear {contact_name},\n\nThank you for your generous support of our mission. Your contribution makes a real difference in our community.\n\nWith gratitude,\nThe Team",
        'follow_up': f"Dear {contact_name},\n\nI hope this message finds you well. I wanted to follow up on our recent conversation about our upcoming initiatives.\n\nBest regards,\nThe Team",
        'appeal': f"Dear {contact_name},\n\nAs we approach the end of the year, we're reaching out to our most valued supporters like you to help us reach our fundraising goal.\n\nSincerely,\nThe Team"
    }
    
    return jsonify({
        'draft': templates.get(email_type, templates['thank_you']),
        'suggestions': [
            'Personalize with specific donation amount',
            'Add recent program impact story',
            'Include clear call-to-action'
        ],
        'confidence_score': 92
    })

@app.route('/api/ai/donor-insights/<int:contact_id>')
def ai_donor_insights(contact_id):
    contacts = get_contacts()
    contact = next((c for c in contacts if c['id'] == contact_id), None)
    
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404
    
    return jsonify({
        'contact_id': contact_id,
        'contact_name': contact['name'],
        'insights': {
            'giving_capacity': 'High - Based on engagement score and donation history',
            'best_contact_time': 'Tuesday-Thursday, 10am-2pm',
            'preferred_communication': 'Email with phone follow-up',
            'interests': ['Education', 'Health', 'Environment'],
            'next_ask_amount': contact['total_donated'] * 1.2 if contact['total_donated'] > 0 else 250
        },
        'recommendations': [
            'Schedule personal meeting within 2 weeks',
            'Send impact report highlighting education programs',
            'Invite to upcoming donor appreciation event'
        ]
    })

# Additional utility endpoints
@app.route('/api/analytics/trends')
def get_trends():
    # Generate sample trend data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
    donation_trends = [1200, 1500, 1800, 2100, 1900, 2300, 2600, 2200, 2800]
    contact_trends = [45, 52, 48, 61, 58, 67, 72, 69, 75]
    
    return jsonify({
        'months': months,
        'donations': donation_trends,
        'contacts': contact_trends
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'features_available': 13
    })

# Export for Vercel
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
