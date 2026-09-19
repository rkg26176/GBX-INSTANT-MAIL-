from flask import Flask, request, jsonify, render_template
import os

# आपके HTML/JS फ्रंटएंड को जोड़ने के लिए
app = Flask(__name__, template_folder='.')

# इनबॉक्स डेटा स्टोर करने के लिए अस्थायी मेमोरी
inbox_storage = {}

@app.route('/')
def home():
    return "GBX Instant Mail Backend is Live!"

# जब बाहर से कोई ईमेल या मैसेज इस पर आएगा
@app.route('/webhook/receive', methods=['POST'])
def receive_message():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No JSON data provided"}), 400
        
    recipient = data.get('to')      # किस ईमेल पर मैसेज आया
    sender = data.get('from')       # किसने भेजा
    message_body = data.get('body') # पूरा मैसेज (ओटीपी या टेक्स्ट)
    
    if recipient:
        if recipient not in inbox_storage:
            inbox_storage[recipient] = []
        inbox_storage[recipient].append({
            'from': sender,
            'body': message_body
        })
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Recipient missing"}), 400

# आपके फ्रंटएंड के लिए इनबॉक्स दिखाने का एपीआई
@app.route('/api/inbox/<path:email_address>', methods=['GET'])
def get_inbox(email_address):
    messages = inbox_storage.get(email_address, [])
    return jsonify({"messages": messages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
