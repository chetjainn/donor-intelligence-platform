from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/test-simple')
def test_simple():
    return jsonify({'message': 'Simple test works', 'status': 'ok'})

@app.route('/api/wealth-screenings-test')
def test_wealth_screenings():
    return jsonify({'message': 'Wealth screenings test works', 'status': 'ok'})

@app.route('/api/dashboard-test')
def test_dashboard():
    return jsonify({'message': 'Dashboard test works', 'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
