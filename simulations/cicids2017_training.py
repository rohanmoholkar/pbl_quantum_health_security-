"""
CICIDS2017 Intrusion Detection — Comparative ML Training Pipeline
=================================================================
Trains Random Forest (Ensemble) and MLP Neural Network (Deep Learning)
on the CICIDS2017 dataset (2.83M flow records, 78 features, 15 classes).

Outputs:
  - ieee_paper_latex/figures/cicids_roc_comparison.png
  - ieee_paper_latex/figures/cicids_confusion_matrix.png
  - ieee_paper_latex/figures/cicids_learning_curve.png
  - ieee_paper_latex/figures/cicids_attack_distribution.png
  - models/cicids_rf_model.pkl
  - models/cicids_scaler.pkl
  - models/cicids_label_encoder.pkl
  - datasets/cicids2017/X_test_sample.npy  (for live demo sampling)
  - datasets/cicids2017/y_test_sample.npy
"""

import os
import sys
import time
import warnings
import glob

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split, learning_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    classification_report, accuracy_score, confusion_matrix,
    roc_curve, auc, ConfusionMatrixDisplay
)

warnings.filterwarnings('ignore')

FIG_DIR   = 'ieee_paper_latex/figures'
MODEL_DIR = 'models'
DATA_DIR  = 'datasets/cicids2017'

os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# ──────────────────────────────────────────────
# 1.  LOAD & MERGE ALL CSV FILES
# ──────────────────────────────────────────────
print("=" * 60)
print("  CICIDS2017 — Full Training Pipeline")
print("=" * 60)

# Look for parquet files first (Hugging Face format), then CSV
parquet_files = sorted(glob.glob(os.path.join(DATA_DIR, 'machine_learning', '*.parquet')))
csv_files = sorted(glob.glob(os.path.join(DATA_DIR, '*.csv')))

data_files = parquet_files if parquet_files else csv_files
file_format = 'parquet' if parquet_files else 'csv'

if not data_files:
    print(f"\nERROR: No CSV or Parquet files found in {DATA_DIR}/")
    print("Please download the CICIDS2017 dataset into that folder.")
    sys.exit(1)

print(f"\nFound {len(data_files)} {file_format.upper()} files:")
for f in data_files:
    print(f"  • {os.path.basename(f)}")

dfs = []
for f in data_files:
    print(f"\nLoading {os.path.basename(f)}...")
    if file_format == 'parquet':
        df = pd.read_parquet(f)
    else:
        try:
            df = pd.read_csv(f, encoding='utf-8', low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(f, encoding='latin-1', low_memory=False)
    # Normalize column names (strip whitespace)
    df.columns = df.columns.str.strip()
    dfs.append(df)
    print(f"  → {len(df):,} rows, {len(df.columns)} columns")

data = pd.concat(dfs, ignore_index=True)
print(f"\n✓ Total merged dataset: {len(data):,} rows × {len(data.columns)} columns")

# ──────────────────────────────────────────────
# 2.  CLEAN DATA
# ──────────────────────────────────────────────
print("\n--- Data Cleaning ---")

# Identify the label column (might be 'Label' or ' Label')
label_col = None
for c in data.columns:
    if c.strip().lower() == 'label':
        label_col = c
        break

if label_col is None:
    print("ERROR: Could not find 'Label' column.")
    sys.exit(1)

print(f"Label column: '{label_col}'")
data[label_col] = data[label_col].str.strip()

# Show class distribution
print("\nClass distribution:")
class_dist = data[label_col].value_counts()
for cls, cnt in class_dist.items():
    print(f"  {cls:30s} → {cnt:>10,}")

# Drop non-numeric columns and the label
feature_cols = data.columns.drop(label_col)
# Keep only numeric columns
numeric_data = data[feature_cols].apply(pd.to_numeric, errors='coerce')

# Replace infinity with NaN, then drop NaN
numeric_data.replace([np.inf, -np.inf], np.nan, inplace=True)
nan_before = numeric_data.isna().sum().sum()
numeric_data.dropna(axis=1, how='all', inplace=True)  # Drop fully-NaN columns
numeric_data.fillna(0, inplace=True)  # Fill remaining NaN with 0

# Align labels with cleaned features
labels = data[label_col].iloc[numeric_data.index]

print(f"\n✓ Features after cleaning: {numeric_data.shape[1]}")
print(f"  NaN/Inf values replaced: {nan_before:,}")

# ──────────────────────────────────────────────
# 3.  PREPARE FEATURES & LABELS
# ──────────────────────────────────────────────
print("\n--- Feature Engineering ---")

X = numeric_data.values.astype(np.float64)
y_raw = labels.values

# Binary classification: BENIGN vs ATTACK
y_binary = np.where(y_raw == 'BENIGN', 0, 1)
print(f"  Binary: {np.sum(y_binary==0):,} benign, {np.sum(y_binary==1):,} attacks")

# Multi-class for confusion matrix
le = LabelEncoder()
y_multi = le.fit_transform(y_raw)
print(f"  Multi-class: {len(le.classes_)} unique classes")

# Use a stratified sample if dataset is very large to keep training practical
MAX_SAMPLES = 500000
if len(X) > MAX_SAMPLES:
    print(f"\n  Sampling {MAX_SAMPLES:,} records for training (stratified)...")
    X_sampled, _, y_bin_sampled, _, y_multi_sampled, _ = train_test_split(
        X, y_binary, y_multi,
        train_size=MAX_SAMPLES,
        stratify=y_binary,
        random_state=42
    )
else:
    X_sampled, y_bin_sampled, y_multi_sampled = X, y_binary, y_multi

# Scale features
print("  Scaling features with StandardScaler...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_sampled)

# Train/Test split
X_train, X_test, y_train, y_test, y_multi_train, y_multi_test = train_test_split(
    X_scaled, y_bin_sampled, y_multi_sampled,
    test_size=0.2, random_state=42, stratify=y_bin_sampled
)

print(f"\n  Training set: {X_train.shape[0]:,} samples")
print(f"  Testing set:  {X_test.shape[0]:,} samples")

# ──────────────────────────────────────────────
# 4.  TRAIN MODELS
# ──────────────────────────────────────────────
models = {
    'Random Forest (Ensemble)': RandomForestClassifier(
        n_estimators=100, max_depth=20, random_state=42, n_jobs=-1
    ),
    'MLP Neural Net (Deep Learning)': MLPClassifier(
        hidden_layer_sizes=(128, 64, 32), max_iter=300,
        alpha=0.001, random_state=42, early_stopping=True,
        validation_fraction=0.1
    )
}

results = {}

print("\n" + "=" * 60)
print("  MODEL TRAINING")
print("=" * 60)

for name, model in models.items():
    print(f"\n>>> Training {name}...")
    t0 = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - t0
    print(f"    Trained in {train_time:.1f}s")

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    acc = accuracy_score(y_test, y_pred)

    print(f"    Accuracy: {acc:.4f}")
    print(f"\n    Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['BENIGN', 'ATTACK']))

    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    results[name] = {
        'model': model, 'fpr': fpr, 'tpr': tpr,
        'auc': roc_auc, 'acc': acc, 'y_pred': y_pred,
        'time': train_time
    }

# ──────────────────────────────────────────────
# 5.  GENERATE FIGURES
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("  GENERATING FIGURES")
print("=" * 60)

# 5a. ROC Comparison
print("\n  → ROC Comparison...")
plt.figure(figsize=(10, 8))
colors = {'Random Forest (Ensemble)': '#22d3ee', 'MLP Neural Net (Deep Learning)': '#a78bfa'}
for name, r in results.items():
    plt.plot(r['fpr'], r['tpr'], color=colors[name], lw=2.5,
             label=f'{name} (AUC = {r["auc"]:.4f})')
plt.plot([0, 1], [0, 1], color='#475569', lw=1.5, linestyle='--')
plt.xlim([-0.01, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=13)
plt.ylabel('True Positive Rate', fontsize=13)
plt.title('ROC Curve: CICIDS2017 Intrusion Detection', fontsize=15)
plt.legend(loc='lower right', fontsize=12)
plt.grid(True, alpha=0.2)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'cicids_roc_comparison.png'), dpi=300)
plt.close()

# 5b. Multi-class Confusion Matrix (Random Forest)
print("  → Confusion Matrix...")
rf_model = models['Random Forest (Ensemble)']
y_multi_pred = rf_model.predict(X_test)

# For the confusion matrix, re-train a multi-class RF quickly
rf_multi = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1)
rf_multi.fit(X_train, y_multi_train)
y_multi_pred = rf_multi.predict(X_test)

# Get top classes (avoid tiny classes cluttering the matrix)
unique_test = np.unique(y_multi_test)
class_names = le.inverse_transform(unique_test)

cm = confusion_matrix(y_multi_test, y_multi_pred, labels=unique_test)

fig, ax = plt.subplots(figsize=(14, 12))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(ax=ax, cmap='Blues', values_format='d', xticks_rotation=45)
ax.set_title('Multi-Class Confusion Matrix: CICIDS2017 (Random Forest)', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'cicids_confusion_matrix.png'), dpi=300)
plt.close()

# 5c. Learning Curves
print("  → Learning Curves...")
train_sizes = np.linspace(0.1, 1.0, 5)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for i, (name, model_obj) in enumerate(models.items()):
    ax = axes[i]
    # Use a smaller sample for learning curves (speed)
    lc_size = min(50000, len(X_scaled))
    X_lc = X_scaled[:lc_size]
    y_lc = y_bin_sampled[:lc_size]

    train_sizes_abs, train_scores, test_scores = learning_curve(
        model_obj, X_lc, y_lc, cv=3, n_jobs=-1,
        train_sizes=train_sizes, scoring='accuracy'
    )
    train_mean = np.mean(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    ax.plot(train_sizes_abs, train_mean, 'o-', color='#ef4444', label='Training')
    ax.plot(train_sizes_abs, test_mean, 'o-', color='#22c55e', label='Cross-validation')
    ax.fill_between(train_sizes_abs, train_mean - train_std, train_mean + train_std, alpha=0.1, color='#ef4444')
    ax.fill_between(train_sizes_abs, test_mean - test_std, test_mean + test_std, alpha=0.1, color='#22c55e')
    ax.set_title(f'Learning Curve: {name}', fontsize=12)
    ax.set_xlabel('Training Examples')
    ax.set_ylabel('Accuracy')
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'cicids_learning_curve.png'), dpi=300)
plt.close()

# 5d. Attack Distribution
print("  → Attack Distribution...")
attack_counts = pd.Series(y_raw).value_counts()
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(
    attack_counts.index[::-1],
    attack_counts.values[::-1],
    color=['#22d3ee' if x == 'BENIGN' else '#f87171' for x in attack_counts.index[::-1]]
)
ax.set_xlabel('Number of Records', fontsize=12)
ax.set_title('CICIDS2017 — Traffic Class Distribution', fontsize=14)
ax.grid(axis='x', alpha=0.2)
for bar, val in zip(bars, attack_counts.values[::-1]):
    ax.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
            f'{val:,}', va='center', fontsize=9, color='#94a3b8')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'cicids_attack_distribution.png'), dpi=300)
plt.close()

# ──────────────────────────────────────────────
# 6.  SAVE MODELS & TEST DATA FOR LIVE DEMO
# ──────────────────────────────────────────────
print("\n--- Saving Models ---")
joblib.dump(rf_model, os.path.join(MODEL_DIR, 'cicids_rf_model.pkl'))
joblib.dump(scaler, os.path.join(MODEL_DIR, 'cicids_scaler.pkl'))
joblib.dump(le, os.path.join(MODEL_DIR, 'cicids_label_encoder.pkl'))

# Save a test sample for the live demo (100k rows to show massive scale)
demo_size = min(100000, len(X_test))
np.save(os.path.join(DATA_DIR, 'X_test_sample.npy'), X_test[:demo_size])
np.save(os.path.join(DATA_DIR, 'y_test_sample.npy'), y_test[:demo_size])
# Save raw labels for demo display
y_raw_test = y_raw[len(y_raw) - len(y_test):][:demo_size]
np.save(os.path.join(DATA_DIR, 'y_test_labels.npy'), y_raw_test)

print(f"  ✓ Models saved to {MODEL_DIR}/")
print(f"  ✓ Demo test data saved ({demo_size:,} samples)")

# ──────────────────────────────────────────────
# 7.  SUMMARY
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("  TRAINING COMPLETE — SUMMARY")
print("=" * 60)
for name, r in results.items():
    print(f"\n  {name}:")
    print(f"    Accuracy : {r['acc']:.4f}")
    print(f"    AUC      : {r['auc']:.4f}")
    print(f"    Time     : {r['time']:.1f}s")
print(f"\n  Figures saved to: {FIG_DIR}/")
print(f"  Models saved to:  {MODEL_DIR}/")
print("=" * 60)
