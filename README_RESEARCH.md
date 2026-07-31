# PBL-2 Research Models

This directory contains three Python simulation modules for the PBL-2 Research & Modeling phase of the Quantum-Secured Digital Health Identity System project.

## Overview

These modules model different aspects of the quantum-secured health system:

1. **QKD Feasibility & Network Planning** (`qkd_model.py`) - Quantum Layer
2. **AI Anomaly Detection Engine** (`ai_defense.py`) - Intelligence Layer  
3. **Post-Quantum Cryptography Comparison** (`pqc_compare.py`) - Cryptographic Analysis

## Installation

Install the required dependencies:

```bash
pip install numpy matplotlib scikit-learn
```

## Usage

### Module 1: QKD Feasibility Model

Models photon loss over fiber optics and calculates Secure Key Rate (SKR):

```bash
python qkd_model.py
```

**Output**: Graph showing exponential decay of secure key rate with distance, with max effective distance ~100km marked.

**For Report**: Include in section 5.2 (Feasibility Modeling)

### Module 2: AI Defense Engine

Trains an Isolation Forest to detect cyberattacks in hospital network traffic:

```bash
python ai_defense.py
```

**Output**: Scatter plot with blue points (normal traffic) and red points (detected attacks).

**For Report**: Include in section 5.4 (AI Anomaly Detection)

### Module 3: PQC Comparison

Compares classical (RSA, ECC) vs quantum-resistant (Kyber, Dilithium) algorithms:

```bash
python pqc_compare.py
```

**Output**: Dual-axis bar chart showing speed vs security strength comparison.

**For Report**: Include in section 5.1 (PQC Selection)

## Technical Details

### QKD Model Parameters
- **Fiber Attenuation**: 0.2 dB/km (SMF-28 standard)
- **Detector Efficiency**: 10%
- **Source Rate**: 1 GHz
- **Distance Range**: 0-150 km

### AI Model Configuration
- **Algorithm**: Isolation Forest
- **Features**: Access frequency, data volume
- **Contamination**: 10% (expected anomaly rate)
- **Training Set**: 200 normal + 20 attack samples

### PQC Metrics (NIST Round 3)
- **RSA-2048**: 160ms key gen, 112-bit security
- **ECC-256**: 200μs key gen, 128-bit security
- **Kyber-512**: 10μs key gen, 128-bit security
- **Dilithium-II**: 20μs key gen, 128-bit security

## Report Integration

1. **Run all three scripts** and capture screenshots of the generated graphs
2. **Save graphs** with descriptive names (e.g., `qkd_skr_vs_distance.png`)
3. **Include in report**:
   - QKD graph → Section 5.2
   - AI scatter plot → Section 5.4
   - PQC comparison → Section 5.1
4. **Methodology**: Mention "Simulated photon loss using Python models" and "Trained Isolation Forest algorithm for real-time threat detection"

## Website Integration

These models are showcased in the project website under the "Research" section. Visit the website to see:
- Interactive code previews
- Feature descriptions
- Expected outputs
- Usage instructions

## Author

**Rohan Sanjeev Moholkar**  
Department of IT, Manipal University Jaipur  
PBL-2 Project: Quantum-Secured Digital Health Identity System for India

## License

This project is part of academic coursework for PBL-2 at Manipal University Jaipur.
