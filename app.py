import os
from flask import Flask, request, jsonify

# This variable MUST be named 'app' for Gunicorn to find it
app = Flask(__name__)

# --- Smart Study Sync Logic ---
def calculate_priority(deadline_days, difficulty_level):
    # Logic: Lower deadline days and higher difficulty = Higher Priority
    # priority_score = (6 - difficulty) + days
    priority_score = (6 - difficulty_level) + deadline_days
    return priority_score

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "assistant": "Smart Study Sync",
        "message": "Academic Success Assistant is ready to prioritize your tasks."
    })

@app.route('/prioritize', methods=['POST'])
def prioritize():
    # 'silent=True' prevents crashing if JSON is missing
    data = request.get_json(silent=True) or {}
    task_name = data.get('task', 'Assignment')
    
    # Robust integer conversion to prevent 'Reason: App failed to load'
    try:
        days = int(data.get('days_left', 7))
        diff = int(data.get('difficulty', 3))
    except (ValueError, TypeError):
        days = 7
        diff = 3
    
    score = calculate_priority(days, diff)
    
    return jsonify({
        "task": task_name,
        "priority_score": score,
        "recommendation": "High Priority" if score < 7 else "Normal Priority"
    })

if __name__ == "__main__":
    # This block is for local testing; Cloud Run uses Gunicorn instead
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)