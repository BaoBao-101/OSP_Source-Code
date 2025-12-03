from flask import Flask, jsonify
import pandas as pd
import joblib
import threading
import sys
import os

# Path to file log
sys.path.append("/opt/apache_log/")

# Import lib
from parse import monitor_logs  
from email_alert import send_email_alert

app = Flask(__name__)

# Load model và vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Path to parsed log
ACCESS_CSV = "/opt/apache_log_monitor/access_log.csv"

# API check log
@app.route('/check_logs', methods=['GET'])
def check_logs():
    if not os.path.exists(ACCESS_CSV):
        return jsonify({"error": "Log file not found!"}), 404

    df_log = pd.read_csv(ACCESS_CSV)
    
    # Check if CSV do not have data
    if df_log.empty:
        return jsonify({"message": "No log entries found."})

    X_new = vectorizer.transform(df_log['Request'])
    df_log['is_malicious'] = model.predict(X_new)

    malicious_requests = df_log[df_log['is_malicious'] == 1]

    if not malicious_requests.empty:
        alert_message = f"Detect {len(malicious_requests)} malicious request!\n\n{malicious_requests.to_string()}"
        send_email_alert("Warning: Detect Attack!", alert_message)
    
    return jsonify(malicious_requests.to_dict(orient="records"))

# Run monitor_logs in background when run app
def start_log_monitoring():
    monitor_logs()

log_thread = threading.Thread(target=start_log_monitoring, daemon=True)
log_thread.start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
