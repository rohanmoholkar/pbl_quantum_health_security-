# Quantum-Secured Digital Health Identity System (PBL-3)

This repository contains the simulation models and academic drafts for the PBL-3 Research & Modeling phase of the Quantum-Secured Digital Health Identity System project.

## Overview

These modules model different aspects of the quantum-secured health system:

1. **QKD Feasibility & Network Planning** (`simulations/qkd_model.py`) - Quantum Layer
2. **AI Intrusion Detection Engine** (`simulations/advanced_ai_intrusion_detection.py`) - Intelligence Layer  
   - Implements a Comparative Study of Ensemble Learning (Random Forest) vs Deep Learning (MLP Neural Network) trained on the empirical KDD Cup 1999 dataset (494k samples).
3. **Post-Quantum Cryptography Comparison** (`simulations/pqc_compare.py`) - Cryptographic Analysis
4. **Blockchain Smart Contract Simulator** (`simulations/blockchain_ehr_demo.py` & `blockchain/HealthIdentity.sol`) - Data Integrity Layer

## Installation

Install the required dependencies for the simulations:

```bash
pip install numpy matplotlib scikit-learn
```

## Usage

### Module 1: QKD Feasibility Model

Models photon loss over fiber optics and calculates Secure Key Rate (SKR):

```bash
python simulations/qkd_model.py
```

**Output**: Graph showing exponential decay of secure key rate with distance.

### Module 2: AI Defense Engine

Trains an Isolation Forest to detect cyberattacks in hospital network traffic:

```bash
python simulations/advanced_ai_intrusion_detection.py
```

**Output**: Scatter plot with blue points (normal traffic) and red points (detected attacks).

### 3. Cryptographic Analysis (PQC)

Compares execution time of classical encryption (RSA/ECC) vs NIST-standardized Post-Quantum Cryptography (Kyber/Dilithium):

```bash
python simulations/pqc_compare.py
```

**Output**: Bar chart comparing key generation speeds in milliseconds.

### 4. Blockchain Smart Contract Integration

Simulates cryptographic hashing of Electronic Health Records on a decentralized ledger, mitigating data tampering and repudiation threats. 

```bash
python simulations/blockchain_ehr_demo.py
```

**Output**: Terminal simulation of a patient registering, a doctor updating an EHR, and an attempted tampering attack failing the cryptographic integrity check.
**Contract Code**: The actual Solidity logic is located in `blockchain/HealthIdentity.sol`.

## Full-Stack Live Web Demo
We have built a gorgeous, interactive Web UI that connects directly to the Python AI backend to stream authentic telemetry data and provide live Intrusion Detection.

1. Install the backend requirements (if not already installed):
   ```bash
   python3 -m pip install flask scikit-learn
   ```
2. Start the AI Server:
   ```bash
   python3 app.py
   ```
3. Open your browser to `http://localhost:5001`.
4. Scroll down to the **Live Full-Stack AI Demo** section and click the button to sample authentic network requests from the KDD Cup testing dataset in real-time!

## Report Integration

The academic drafting uses the IEEE LaTeX template, located in `ieee_paper_latex/`. 

To compile the paper:
1. Ensure the generated simulation graphs are inside `ieee_paper_latex/figures/`
2. Compile `ieee_paper_latex/main.tex` using `pdflatex` or Overleaf.

## Author

**Rohan Sanjeev Moholkar**  
Department of IT, Manipal University Jaipur  
PBL-3 Project: Quantum-Secured Digital Health Identity System for India

## License

This project is part of academic coursework for PBL-3 at Manipal University Jaipur.