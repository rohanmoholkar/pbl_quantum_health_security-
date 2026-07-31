import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import time

from sklearn.datasets import fetch_kddcup99
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import roc_curve, auc, classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler

print("Fetching KDD Cup 99 dataset (494k samples)...")
start_time = time.time()
kdd = fetch_kddcup99(percent10=True)

X = kdd.data
y = kdd.target

# Convert labels
y = np.array([label.decode('utf-8') for label in y])
y_binary = np.where(y == 'normal.', 0, 1)

print(f"Dataset loaded in {time.time() - start_time:.2f} seconds. Total samples: {X.shape[0]}")

# Extract numerical features for rapid training
X_numeric = []
for row in X:
    num_row = []
    for val in row:
        if isinstance(val, (int, float)):
            num_row.append(val)
    X_numeric.append(num_row)

X_numeric = np.array(X_numeric, dtype=float)

# Scale data for MLP Neural Network
print("Scaling features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_numeric)

# To ensure the script completes in a reasonable time for research iteration,
# we use a large stratified sample of 100,000 records for the deep learning training.
# (Training an MLP on 500k rows can take hours on standard hardware).
SAMPLE_SIZE = 100000
if X_scaled.shape[0] > SAMPLE_SIZE:
    X_sample, _, y_sample, _ = train_test_split(X_scaled, y_binary, train_size=SAMPLE_SIZE, stratify=y_binary, random_state=42)
else:
    X_sample, y_sample = X_scaled, y_binary

X_train, X_test, y_train, y_test = train_test_split(X_sample, y_sample, test_size=0.2, random_state=42, stratify=y_sample)

print(f"Training Data: {X_train.shape[0]} samples")
print(f"Testing Data: {X_test.shape[0]} samples")

# Define Models
models = {
    'Random Forest (Ensemble)': RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1),
    'MLP Neural Net (Deep Learning)': MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=200, alpha=0.001, random_state=42, early_stopping=True)
}

fig_dir = 'ieee_paper_latex/figures'
os.makedirs(fig_dir, exist_ok=True)

# 1. Comparative ROC Curve
print("\n--- Training Models for ROC Comparison ---")
plt.figure(figsize=(10, 8))
colors = ['darkorange', 'blue']

for (name, model), color in zip(models.items(), colors):
    print(f"Training {name}...")
    t0 = time.time()
    model.fit(X_train, y_train)
    t1 = time.time()
    print(f"{name} trained in {t1 - t0:.2f} seconds.")
    
    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred = model.predict(X_test)
    
    print(f"\nClassification Report for {name}:")
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Attack']))
    
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, color=color, lw=2, label=f'{name} (AUC = {roc_auc:.4f})')

plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([-0.01, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('Comparative ROC Curve: Deep Learning vs Ensemble', fontsize=14)
plt.legend(loc="lower right", fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'ai_roc_comparison.png'), dpi=300)
plt.close()

# 2. Learning Curve Analysis
print("\n--- Generating Learning Curves ---")
train_sizes = np.linspace(0.1, 1.0, 5)

plt.figure(figsize=(12, 6))
for i, (name, model) in enumerate(models.items(), 1):
    print(f"Calculating learning curve for {name}...")
    plt.subplot(1, 2, i)
    train_sizes_abs, train_scores, test_scores = learning_curve(
        model, X_sample, y_sample, cv=3, n_jobs=-1, train_sizes=train_sizes, scoring='accuracy'
    )
    
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    
    plt.plot(train_sizes_abs, train_mean, 'o-', color="r", label="Training score")
    plt.plot(train_sizes_abs, test_mean, 'o-', color="g", label="Cross-validation score")
    plt.fill_between(train_sizes_abs, train_mean - train_std, train_mean + train_std, alpha=0.1, color="r")
    plt.fill_between(train_sizes_abs, test_mean - test_std, test_mean + test_std, alpha=0.1, color="g")
    
    plt.title(f'Learning Curve: {name}')
    plt.xlabel('Training Examples')
    plt.ylabel('Accuracy Score')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'ai_learning_curve.png'), dpi=300)
plt.close()

print(f"\nSUCCESS: Advanced ML plots saved to {fig_dir}")
