import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_kddcup99
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc, accuracy_score
import os

print("Fetching KDD Cup 99 dataset (10% subset)...")
# Download dataset (approx 18MB, cached locally)
kdd = fetch_kddcup99(percent10=True)

X = kdd.data
y = kdd.target

# Convert byte strings to strings for labels
y = np.array([label.decode('utf-8') for label in y])

# Make binary classification: 'normal.' vs everything else (attacks)
y_binary = np.where(y == 'normal.', 0, 1)

print(f"Dataset loaded. Total samples: {X.shape[0]}")
print(f"Normal traffic samples: {np.sum(y_binary == 0)}")
print(f"Attack traffic samples: {np.sum(y_binary == 1)}")

# For a quick demonstration and to avoid complex categorical encoding overhead,
# we will extract only the numerical continuous features from the dataset.
# In KDD99, these are indices 0, 4, 5, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 22...
# An easier way is to just filter out strings.
X_numeric = []
for row in X:
    num_row = []
    for val in row:
        if isinstance(val, (int, float)):
            num_row.append(val)
    X_numeric.append(num_row)

X_numeric = np.array(X_numeric, dtype=float)

print("Splitting dataset into train/test sets...")
X_train, X_test, y_train, y_test = train_test_split(X_numeric, y_binary, test_size=0.2, random_state=42, stratify=y_binary)

print("Training Random Forest Classifier on network traffic data...")
clf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=10, n_jobs=-1)
clf.fit(X_train, y_train)

print("Evaluating model...")
y_pred = clf.predict(X_test)
y_prob = clf.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {acc * 100:.2f}%")

# Create figures directory if it doesn't exist
fig_dir = '../ieee_paper_latex/figures'
os.makedirs(fig_dir, exist_ok=True)

# 1. Confusion Matrix
print("Generating Confusion Matrix...")
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Normal', 'Attack'])
fig, ax = plt.subplots(figsize=(6, 6))
disp.plot(ax=ax, cmap='Blues', colorbar=False)
plt.title("AI Intrusion Detection: Confusion Matrix")
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'ai_confusion_matrix.png'), dpi=300)
plt.close()

# 2. ROC Curve
print("Generating ROC Curve...")
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([-0.01, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) - AI Defense')
plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'ai_roc_curve.png'), dpi=300)
plt.close()

print(f"Done! Plots saved to {fig_dir}")
