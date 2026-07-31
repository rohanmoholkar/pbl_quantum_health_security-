import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# --- DATA: Performance Metrics (Approximated from NIST Round 3) ---
algorithms = ['RSA-2048', 'ECC-256', 'Kyber-512 (PQC)', 'Dilithium-II (PQC)']

# Key Generation Time (microseconds) - Lower is better
key_gen_time = [160000, 200, 10, 20] 

# Security Level (Bits) - Higher is better
security_bits = [112, 128, 128, 128] # Note: RSA-2048 is only ~112 bits effective

# --- PLOTTING ---
x = np.arange(len(algorithms))
width = 0.35

fig, ax1 = plt.subplots(figsize=(10, 6))

# Bar 1: Speed (Key Gen Time)
color = 'tab:blue'
ax1.set_xlabel('Algorithm')
ax1.set_ylabel('Key Gen Time (microseconds) - Log Scale', color=color)
rects1 = ax1.bar(x - width/2, key_gen_time, width, label='Speed (Latency)', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_yscale('log') # Log scale because RSA is SO slow compared to PQC

# Bar 2: Security Level
ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('Security Strength (Bits)', color=color)
rects2 = ax2.bar(x + width/2, security_bits, width, label='Security Strength', color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(0, 200)

# Labels
ax1.set_xticks(x)
ax1.set_xticklabels(algorithms)
plt.title('Comparison: Classical vs. Post-Quantum Algorithms')

fig.tight_layout()
plt.savefig('pqc_comparison.png', dpi=300)

print("Comparison generated. Graph saved as 'pqc_comparison.png'.")
