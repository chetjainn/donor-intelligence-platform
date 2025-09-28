from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__, template_folder='../templates')
CORS(app)

# Global data storage
data_store = {
    'contacts': [],
    'tasks': [],
    'campaigns': [],
    'grants': [],
    'events': [],
    'wealth_screenings': []
}

def get_sample_data():
    """Initialize and return sample data"""
    
    # Sample contacts
    contacts = [
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
    
    # Sample tasks
    tasks = [
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
    
    # Sample campaigns
    campaigns = [
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
    
    # Sample grants
    grants = [
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
    
    # Sample events
    events = [
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
    
    # Sample wealth screenings
    wealth_screenings = [
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
    
    return {
        'contacts': contacts,
        'tasks': tasks,
        'campaigns': campaigns,
        'grants': grants,
        'events': events,
        'wealth_screenings': wealth_screenings
    }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return jsonify({'message': 'Flask app is working!', 'timestamp': datetime.now().isoformat()})

# Dashboard endpoint
@app.route('/api/dashboard')
def get_dashboard():
    data = get_sample_data()
    contacts = data['contacts']
    campaigns = data['campaigns']
    tasks = data['tasks']
    grants = data['grants']
    events = data['events']
    
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

# Contacts
@app.route('/api/contacts', methods=['GET', 'POST'])
def handle_contacts():
    data = get_sample_data()
    if request.method == 'GET':
        return jsonify(data['contacts'])
    
    elif request.method == 'POST':
        req_data = request.get_json()
        new_contact = {
            'id': len(data['contacts']) + 1,
            'name': req_data.get('name'),
            'email': req_data.get('email'),
            'type': req_data.get('type'),
            'phone': req_data.get('phone', ''),
            'total_donated': 0.00,
            'last_donation': None,
            'engagement_score': random.randint(50, 100),
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        return jsonify(new_contact), 201

# Tasks
@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    data = get_sample_data()
    if request.method == 'GET':
        return jsonify(data['tasks'])
    
    elif request.method == 'POST':
        req_data = request.get_json()
        new_task = {
            'id': len(data['tasks']) + 1,
            'title': req_data.get('title'),
            'description': req_data.get('description', ''),
            'priority': req_data.get('priority', 'medium'),
            'status': 'pending',
            'contact_id': req_data.get('contact_id'),
            'due_date': req_data.get('due_date'),
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        return jsonify(new_task), 201

# Campaigns
@app.route('/api/campaigns', methods=['GET', 'POST'])
def handle_campaigns():
    data = get_sample_data()
    if request.method == 'GET':
        return jsonify(data['campaigns'])
    
    elif request.method == 'POST':
        req_data = request.get_json()
        new_campaign = {
            'id': len(data['campaigns']) + 1,
            'name': req_data.get('name'),
            'type': req_data.get('type', 'newsletter'),
            'status': 'draft',
            'subject': req_data.get('subject'),
            'sent_count': 0,
            'open_rate': 0,
            'click_rate': 0,
            'revenue': 0.00,
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        return jsonify(new_campaign), 201

# Grants
@app.route('/api/grants', methods=['GET', 'POST'])
def handle_grants():
    data = get_sample_data()
    if request.method == 'GET':
        return jsonify(data['grants'])
    
    elif request.method == 'POST':
        req_data = request.get_json()
        new_grant = {
            'id': len(data['grants']) + 1,
            'foundation': req_data.get('foundation'),
            'amount': req_data.get('amount'),
            'status': 'research',
            'deadline': req_data.get('deadline'),
            'probability': req_data.get('probability', 50),
            'program': req_data.get('program'),
            'contact_person': req_data.get('contact_person'),
            'notes': req_data.get('notes', ''),
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        return jsonify(new_grant), 201

# Events
@app.route('/api/events', methods=['GET', 'POST'])
def handle_events():
    data = get_sample_data()
    if request.method == 'GET':
        return jsonify(data['events'])
    
    elif request.method == 'POST':
        req_data = request.get_json()
        new_event = {
            'id': len(data['events']) + 1,
            'name': req_data.get('name'),
            'date': req_data.get('date'),
            'time': req_data.get('time'),
            'venue': req_data.get('venue'),
            'capacity': req_data.get('capacity', 100),
            'registered': 0,
            'ticket_price': req_data.get('ticket_price', 0.00),
            'revenue_goal': req_data.get('revenue_goal', 0.00),
            'current_revenue': 0.00,
            'status': 'planning',
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        return jsonify(new_event), 201

# Wealth Screenings
@app.route('/api/wealth-screenings', methods=['GET', 'POST'])
def handle_wealth_screenings():
    data = get_sample_data()
    if request.method == 'GET':
        return jsonify(data['wealth_screenings'])
    
    elif request.method == 'POST':
        req_data = request.get_json()
        new_screening = {
            'id': len(data['wealth_screenings']) + 1,
            'contact_id': req_data.get('contact_id'),
            'contact_name': req_data.get('contact_name'),
            'estimated_capacity': req_data.get('estimated_capacity'),
            'confidence_level': req_data.get('confidence_level', 'medium'),
            'wealth_indicators': req_data.get('wealth_indicators', []),
            'giving_history': req_data.get('giving_history', ''),
            'interests': req_data.get('interests', []),
            'recommended_ask': req_data.get('recommended_ask'),
            'next_steps': req_data.get('next_steps', ''),
            'screened_date': datetime.now().strftime('%Y-%m-%d')
        }
        return jsonify(new_screening), 201

# Analytics Dashboard
@app.route('/api/analytics/dashboard')
def get_dashboard_analytics():
    data = get_sample_data()
    contacts = data['contacts']
    campaigns = data['campaigns']
    tasks = data['tasks']
    grants = data['grants']
    events = data['events']
    
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

# AI Features
@app.route('/api/ai/prioritize-tasks')
def ai_prioritize_tasks():
    data = get_sample_data()
    tasks = data['tasks']
    
    # AI-powered task prioritization
    prioritized_tasks = sorted(tasks, key=lambda x: (
        {'high': 3, 'medium': 2, 'low': 1}[x['priority']], 
        x['created_at']
    ), reverse=True)
    
    return jsonify({
        'prioritized_tasks': prioritized_tasks[:5],
        'ai_insights': [
            'Focus on high-value donor follow-ups first',
            'Grant deadlines approaching - prioritize applications',
            'Schedule prospect meetings for maximum impact'
        ]
    })

@app.route('/api/ai/draft-email', methods=['POST'])
def ai_draft_email():
    req_data = request.get_json()
    contact_name = req_data.get('contact_name', 'Valued Supporter')
    email_type = req_data.get('type', 'thank_you')
    
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
        ]
    })

# Settings
@app.route('/api/settings')
def get_settings():
    return jsonify({
        'organization_name': 'Sample Nonprofit Organization',
        'email_signature': 'Best regards,\nFundraising Team',
        'default_currency': 'USD',
        'email_notifications': True,
        'ai_features_enabled': True
    })

@app.route('/api/settings', methods=['POST'])
def update_settings():
    req_data = request.get_json()
    return jsonify({
        'message': 'Settings updated successfully',
        'settings': req_data
    })

# Bulk upload
@app.route('/api/bulk-upload', methods=['POST'])
def bulk_upload():
    return jsonify({'message': 'Bulk upload feature coming soon!', 'status': 'success'})

# Export for Vercel
app.config['DEBUG'] = False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
