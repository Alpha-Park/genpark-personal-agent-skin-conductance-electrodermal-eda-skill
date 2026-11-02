"""
Example usage for Electrodermal Activity (EDA) & Skin Conductance Skill.
Demonstrates analyzing synthetic skin conductance stream and detecting phasic bursts.
"""

import math
from client import ElectrodermalActivityClient


def generate_synthetic_eda(duration_sec: float = 60.0, sample_rate: float = 10.0):
    samples = []
    total_pts = int(duration_sec * sample_rate)
    base_scl = 4.2
    for i in range(total_pts):
        t = i / sample_rate
        # Slow drift
        drift = base_scl + 0.5 * math.sin(2.0 * math.pi * 0.02 * t)
        # Add discrete phasic spikes at t = 12s, 28s, 44s
        phasic = 0.0
        for spike_t in [12.0, 28.0, 44.0]:
            dt = t - spike_t
            if 0.0 <= dt <= 3.5:
                phasic += 0.35 * math.exp(-dt / 1.2) * math.sin(math.pi * dt / 3.5)
        samples.append(round(drift + phasic, 4))
    return samples


def main():
    client = ElectrodermalActivityClient()

    print("=== 1. Analyzing 60-Second EDA Stream ===")
    eda_stream = generate_synthetic_eda(duration_sec=60.0, sample_rate=10.0)
    res = client.analyze_eda_stream(eda_stream, sample_rate_hz=10.0)

    print(f"Total Duration: {res['total_duration_sec']} s")
    print(f"Mean Tonic SCL: {res['mean_tonic_scl_us']} uS")
    print(f"SCR Event Count: {res['scr_event_count']} (Frequency: {res['nsscr_frequency_per_min']} bursts/min)")
    print(f"Mean SCR Amplitude: {res['mean_scr_amplitude_us']} uS")
    print(f"Autonomic Arousal Index: {res['autonomic_arousal_index']} / 100")
    print(f"Status: {res['status']}")
    print(f"Guidance: {res['actionable_guidance']}")


if __name__ == "__main__":
    main()
