import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import IsolationForest

# --- DATA GENERATION ---
# 1. Generate "Normal" Hospital Traffic
# Features: [Login_Time (0-24h), Data_Volume_MB, Access_Frequency]
rng = np.random.RandomState(42)
X_normal = 0.3 * rng.randn(100, 2)
X_normal_train = np.r_[X_normal + 2, X_normal - 2] # Two clusters of normal activity

# 2. Generate "Cyberattack" Anomalies (Outliers)
# Random scattered points representing irregular access
X_outliers = rng.uniform(low=-4, high=4, size=(20, 2))

# Combine datasets
X_combined = np.r_[X_normal_train, X_outliers]

# --- AI MODEL TRAINING ---
# Isolation Forest: Efficient for detecting anomalies in high-volume data
clf = IsolationForest(max_samples=100, random_state=rng, contamination=0.1)
clf.fit(X_combined)

# Predict: 1 = Normal, -1 = Anomaly
y_pred = clf.predict(X_combined)

# --- VISUALIZATION ---
plt.figure(figsize=(10, 6))
plt.title("AI Defense: Detecting Hospital Network Anomalies")

# Plot the data points
scatter = plt.scatter(X_combined[:, 0], X_combined[:, 1], c=y_pred, cmap='coolwarm', s=50, edgecolors='k')

# Add legend manually for clarity
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Normal Traffic'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Detected Attack')
]

plt.legend(handles=legend_elements, loc='upper right')
plt.xlabel("Feature 1: Access Frequency (Normalized)")
plt.ylabel("Feature 2: Data Volume Downloaded (Normalized)")
plt.grid(True)
plt.savefig('ai_defense_anomalies.png', dpi=300)

print("AI Model Trained. Plot saved as 'ai_defense_anomalies.png'.")
