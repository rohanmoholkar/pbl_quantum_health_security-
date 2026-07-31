from flask import Flask, jsonify, send_from_directory
import os
import random
import numpy as np
import joblib
from sklearn.datasets import fetch_kddcup99

app = Flask(__name__, static_folder='.', static_url_path='')

print("=== Booting Full-Stack AI Defense Server ===")

# 1. Load the pre-trained Brain
print("Loading Random Forest Model and Scaler...")
model_path = os.path.join('models', 'rf_intrusion_model.pkl')
scaler_path = os.path.join('models', 'scaler.pkl')

if not os.path.exists(model_path):
    print("CRITICAL ERROR: AI Model not found. Run training script first.")
    exit(1)

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# 2. Load the Dataset for Authentic Sampling
print("Loading KDD Cup 99 Dataset for authentic sampling (this takes a few seconds)...")
kdd = fetch_kddcup99(percent10=True)
raw_X = kdd.data
raw_y = kdd.target

print(f"Loaded {len(raw_X)} authentic network telemetry rows.")

# Extract numerical features just like the training script
X_numeric = []
for row in raw_X:
    num_row = []
    for val in row:
        if isinstance(val, (int, float)):
            num_row.append(val)
    X_numeric.append(num_row)

X_numeric = np.array(X_numeric, dtype=float)
y = np.array([label.decode('utf-8') for label in raw_y])

print("Server Ready!")

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/analyze_traffic')
def analyze_traffic():
    # 1. Randomly sample one AUTHENTIC row from the dataset
    idx = random.randint(0, len(X_numeric) - 1)
    sample_features = X_numeric[idx]
    true_label = y[idx]
    
    # 2. Preprocess (Scale) just like in training
    scaled_features = scaler.transform(sample_features.reshape(1, -1))
    
    # 3. Model Inference (True AI prediction)
    prediction = model.predict(scaled_features)[0]
    confidence_scores = model.predict_proba(scaled_features)[0]
    confidence = np.max(confidence_scores) * 100
    
    # Format the original features for display
    # (Just grab the first 5 metrics to avoid overwhelming the UI)
    telemetry_summary = {
        "Duration": float(sample_features[0]),
        "Src_Bytes": float(sample_features[1]),
        "Dst_Bytes": float(sample_features[2]),
        "Failed_Logins": float(sample_features[4]),
        "Compromised": float(sample_features[5])
    }
    
    is_attack_prediction = bool(prediction == 1)
    is_actual_attack = (true_label != 'normal.')
    
    return jsonify({
        "status": "success",
        "telemetry": telemetry_summary,
        "true_label": true_label,
        "is_actual_attack": is_actual_attack,
        "is_attack_prediction": is_attack_prediction,
        "confidence": float(confidence)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
