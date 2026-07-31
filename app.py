from flask import Flask, jsonify
import os
import random
import numpy as np
import joblib

app = Flask(__name__, static_folder='.', static_url_path='')

print("=== Booting Full-Stack AI Defense Server (CICIDS2017) ===")

# 1. Load the CICIDS2017-trained model
MODEL_DIR = 'models'
DATA_DIR  = 'datasets/cicids2017'

model  = joblib.load(os.path.join(MODEL_DIR, 'cicids_rf_model.pkl'))
scaler = joblib.load(os.path.join(MODEL_DIR, 'cicids_scaler.pkl'))
le     = joblib.load(os.path.join(MODEL_DIR, 'cicids_label_encoder.pkl'))
print("✓ CICIDS2017 Random Forest model loaded")

# 2. Load pre-saved test samples for authentic demo
X_test = np.load(os.path.join(DATA_DIR, 'X_test_sample.npy'))
y_test = np.load(os.path.join(DATA_DIR, 'y_test_sample.npy'))
y_labels = np.load(os.path.join(DATA_DIR, 'y_test_labels.npy'), allow_pickle=True)
print(f"✓ Loaded {len(X_test):,} authentic test samples for live demo")
print("Server Ready!")

# Feature names from CICIDS2017 (for display)
DISPLAY_FEATURES = [
    "Flow Duration", "Total Fwd Packets", "Total Bwd Packets",
    "Flow Bytes/s", "Flow Packets/s"
]

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/analyze_traffic')
def analyze_traffic():
    # Sample one authentic row
    idx = random.randint(0, len(X_test) - 1)
    sample = X_test[idx]
    true_binary = int(y_test[idx])
    # Reconstruct label from the binary test split since y_labels got shuffled
    true_label  = "BENIGN" if true_binary == 0 else "ATTACK"

    # Model inference — the sample is already scaled
    prediction = int(model.predict(sample.reshape(1, -1))[0])
    proba = model.predict_proba(sample.reshape(1, -1))[0]
    confidence = float(np.max(proba) * 100)
    
    # Build telemetry for display (first 5 raw feature values)
    telemetry = {}
    for i, name in enumerate(DISPLAY_FEATURES):
        if i < len(sample):
            telemetry[name] = round(float(sample[i]), 2)

    return jsonify({
        "status": "success",
        "dataset": "CICIDS2017",
        "telemetry": telemetry,
        "true_label": true_label,
        "is_actual_attack": bool(true_binary == 1),
        "is_attack_prediction": bool(prediction == 1),
        "confidence": confidence
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
