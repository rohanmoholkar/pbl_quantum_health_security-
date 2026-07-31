import os
import time
import random
import numpy as np
import joblib

# ANSI Color Codes for stylized terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("==========================================================")
    print("   QUANTUM-SECURED HEALTH API: AI INTRUSION DETECTION     ")
    print("==========================================================")
    print(f"{Colors.ENDC}")

def load_ai_brain():
    model_path = os.path.join('models', 'rf_intrusion_model.pkl')
    scaler_path = os.path.join('models', 'scaler.pkl')
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        print(f"{Colors.FAIL}[ERROR] AI Brain not found! Please run 'python3 simulations/advanced_ai_intrusion_detection.py' first.{Colors.ENDC}")
        exit(1)
        
    print(f"{Colors.CYAN}[SYSTEM] Booting AI Core...{Colors.ENDC}")
    time.sleep(0.5)
    print(f"{Colors.CYAN}[SYSTEM] Loading Random Forest ensemble weights from {model_path}...{Colors.ENDC}")
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    time.sleep(0.5)
    print(f"{Colors.GREEN}[SUCCESS] AI Defense Engine Online. Standing by for API traffic.{Colors.ENDC}\n")
    return model, scaler

def simulate_traffic(model, scaler):
    n_features = model.n_features_in_
    
    print(f"{Colors.BOLD}Instructions: Press [ENTER] to simulate incoming network traffic. Type 'q' to quit.{Colors.ENDC}\n")
    
    packet_id = 1000
    while True:
        user_input = input(f"{Colors.CYAN}Simulate Packet [{packet_id}] (Press Enter): {Colors.ENDC}")
        if user_input.lower() == 'q':
            print("Shutting down AI Defense Engine...")
            break
            
        print(f"  {Colors.BLUE}[LOG] Receiving TCP packet on Health API port 443...{Colors.ENDC}")
        time.sleep(0.3)
        
        # We simulate a feature vector.
        # To make the demo interesting, we randomly decide if this is an attack or normal traffic.
        is_attack_sim = random.random() > 0.6 
        
        if is_attack_sim:
            # Simulate anomalous traffic (e.g., extremely high connection counts, weird protocol flags)
            raw_features = np.random.uniform(high=10000.0, size=(1, n_features))
        else:
            # Simulate normal traffic (low connection counts, standard payload sizes)
            raw_features = np.random.uniform(low=0.0, high=10.0, size=(1, n_features))
            
        # The scaler transforms it to the distribution the model expects
        scaled_features = scaler.transform(raw_features)
        
        print(f"  {Colors.BLUE}[LOG] Extracting {n_features} numerical telemetry features...{Colors.ENDC}")
        time.sleep(0.4)
        print(f"  {Colors.BLUE}[LOG] Passing through Random Forest Deep Inspection...{Colors.ENDC}")
        time.sleep(0.5)
        
        prediction = model.predict(scaled_features)[0]
        confidence = np.max(model.predict_proba(scaled_features)[0]) * 100
        
        if prediction == 1:
            print(f"  {Colors.FAIL}{Colors.BOLD}[CRITICAL ALERT] Malicious Intrusion Detected! (Confidence: {confidence:.1f}%){Colors.ENDC}")
            print(f"  {Colors.WARNING}>> Action: Connection dropped. IP Address blacklisted.{Colors.ENDC}\n")
        else:
            print(f"  {Colors.GREEN}{Colors.BOLD}[SAFE] Normal EHR API Request. (Confidence: {confidence:.1f}%){Colors.ENDC}")
            print(f"  {Colors.GREEN}>> Action: Traffic allowed. Routing to secure backend.{Colors.ENDC}\n")
            
        packet_id += 1

if __name__ == "__main__":
    print_header()
    model, scaler = load_ai_brain()
    simulate_traffic(model, scaler)
