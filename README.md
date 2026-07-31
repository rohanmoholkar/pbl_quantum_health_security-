# Quantum-Secured Digital Health Identity System (PBL-2)

This repository contains the simulation models and academic drafts for the PBL-2 Research & Modeling phase of the Quantum-Secured Digital Health Identity System project.

## Overview

These modules model different aspects of the quantum-secured health system:

1. **QKD Feasibility & Network Planning** (`simulations/qkd_model.py`) - Quantum Layer
2. **AI Anomaly Detection Engine** (`simulations/ai_defense.py`) - Intelligence Layer  
3. **Post-Quantum Cryptography Comparison** (`simulations/pqc_compare.py`) - Cryptographic Analysis

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
python simulations/ai_defense.py
```

**Output**: Scatter plot with blue points (normal traffic) and red points (detected attacks).

### Module 3: PQC Comparison

Compares classical (RSA, ECC) vs quantum-resistant (Kyber, Dilithium) algorithms:

```bash
python simulations/pqc_compare.py
```

**Output**: Dual-axis bar chart showing speed vs security strength comparison.

## Report Integration

The academic drafting uses the IEEE LaTeX template, located in `ieee_paper_latex/`. 

To compile the paper:
1. Ensure the generated simulation graphs are inside `ieee_paper_latex/figures/`
2. Compile `ieee_paper_latex/main.tex` using `pdflatex` or Overleaf.

## Author

**Rohan Sanjeev Moholkar**  
Department of IT, Manipal University Jaipur  
PBL-2 Project: Quantum-Secured Digital Health Identity System for India

## License

This project is part of academic coursework for PBL-2 at Manipal University Jaipur.