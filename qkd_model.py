import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURATION PARAMETERS ---
# Standard Telecom Fiber (SMF-28) attenuation at 1550nm
ATTENUATION_DB_PER_KM = 0.2
# Detector efficiency (how good the hardware is)
DETECTOR_EFFICIENCY = 0.1
# Dark count rate (noise in the system)
DARK_COUNT_RATE = 1e-6
# Source pulse rate (1 GHz system)
SOURCE_RATE_HZ = 1e9

def calculate_photon_survival(distance_km):
    """Calculates probability of a photon surviving the fiber journey."""
    # Loss in dB = alpha * L
    loss_db = ATTENUATION_DB_PER_KM * distance_km
    # Convert dB to linear transmittance: T = 10^(-dB/10)
    transmittance = 10 ** (-loss_db / 10)
    return transmittance

def estimate_secure_key_rate(distance_km):
    """
    Estimates the Secure Key Rate (SKR) in bits per second.
    Simplified GLLP formula for simulation purposes.
    """
    transmittance = calculate_photon_survival(distance_km)
    
    # Raw detection rate
    raw_rate = SOURCE_RATE_HZ * transmittance * DETECTOR_EFFICIENCY
    
    # Approximate SKR (subtracting noise/overhead)
    # If signal is too low (below noise floor), SKR drops to 0
    skr = raw_rate * (1 - (DARK_COUNT_RATE / (transmittance * DETECTOR_EFFICIENCY)))
    
    # Ensure no negative rates
    skr = np.maximum(skr, 0)
    return skr

# --- SIMULATION ---
distances = np.linspace(0, 150, 100) # Simulate 0 to 150 km
skr_values = [estimate_secure_key_rate(d) for d in distances]

# --- PLOTTING ---
plt.figure(figsize=(10, 6))
plt.semilogy(distances, skr_values, 'b-', linewidth=2, label='Secure Key Rate')
plt.axvline(x=100, color='r', linestyle='--', label='Max Secure Distance (~100km)')
plt.title('QKD Feasibility: Secure Key Rate vs. Distance')
plt.xlabel('Fiber Distance (km)')
plt.ylabel('Key Rate (bits/second) - Log Scale')
plt.grid(True, which="both", ls="-")
plt.legend()
plt.tight_layout()
plt.savefig('qkd_skr_vs_distance.png', dpi=300)

print(f"Simulation Complete. Graph saved as 'qkd_skr_vs_distance.png'.")
