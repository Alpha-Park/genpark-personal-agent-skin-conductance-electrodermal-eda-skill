"""
Electrodermal Activity (EDA) & Skin Conductance Phasic Response Engine.
Provides deterministic, zero-dependency decomposition of tonic Skin Conductance Level (SCL)
and phasic Skin Conductance Responses (SCR), quantifying autonomic sympathetic arousal.
"""

import math
from typing import Dict, Any, List, Optional


class ElectrodermalActivityClient:
    """
    Deterministic client for analyzing Electrodermal Activity (EDA / GSR) in microsiemens (uS).
    Pure Python standard library implementation based on Boucsein and Society for Psychophysiological Research standards.
    """

    def __init__(self):
        pass

    def analyze_eda_stream(
        self,
        conductance_samples_us: List[float],
        sample_rate_hz: float = 10.0,
        scr_threshold_us: float = 0.05
    ) -> Dict[str, Any]:
        """
        Decomposes EDA timeseries into tonic baseline (SCL) and phasic event peaks (SCRs).
        conductance_samples_us: skin conductance in microsiemens (uS).
        scr_threshold_us: minimum peak amplitude to count as a genuine SCR (default: 0.05 uS).
        """
        n = len(conductance_samples_us)
        if n < 10:
            return {"error": "At least 10 EDA samples required for analysis"}

        total_duration_sec = n / sample_rate_hz
        duration_minutes = total_duration_sec / 60.0

        mean_scl = sum(conductance_samples_us) / n
        min_scl = min(conductance_samples_us)
        max_scl = max(conductance_samples_us)

        # Baseline window for tonic SCL extraction (simple moving average over ~4 seconds)
        window_size = max(3, int(sample_rate_hz * 4))
        phasic_components = []
        for i in range(n):
            start = max(0, i - window_size)
            local_baseline = sum(conductance_samples_us[start:i + 1]) / (i - start + 1)
            phasic = conductance_samples_us[i] - local_baseline
            phasic_components.append(max(0.0, phasic))

        # Peak detection on phasic signal
        scr_peaks = []
        in_peak = False
        peak_val = 0.0

        for i in range(1, n - 1):
            val = phasic_components[i]
            prev_val = phasic_components[i - 1]
            next_val = phasic_components[i + 1]

            if val > scr_threshold_us and val >= prev_val and val >= next_val:
                scr_peaks.append({
                    "timestamp_sec": round(i / sample_rate_hz, 2),
                    "amplitude_us": round(val, 3)
                })

        scr_count = len(scr_peaks)
        nsscr_frequency_per_min = round(scr_count / max(0.1, duration_minutes), 2)
        mean_peak_amplitude = round(sum(p["amplitude_us"] for p in scr_peaks) / scr_count, 3) if scr_count > 0 else 0.0

        # Autonomic Arousal Index (AAI, 0 - 100):
        # Normal resting: SCL 2-8 uS, NSSCRs 1-3 / min
        # High arousal: SCL > 12 uS, NSSCRs > 7 / min
        scl_factor = min(40.0, (mean_scl / 12.0) * 40.0)
        freq_factor = min(60.0, (nsscr_frequency_per_min / 8.0) * 60.0)
        aai_score = round(min(100.0, max(5.0, scl_factor + freq_factor)), 1)

        if aai_score <= 30.0:
            status = "PARASYMPATHETIC_DOMINANCE_CALM"
            guidance = "Low tonic conductance with minimal phasic bursts; autonomic system is calm and settled."
        elif aai_score <= 65.0:
            status = "BALANCED_COGNITIVE_ALERTNESS"
            guidance = "Moderate sudomotor activity consistent with productive engagement and active cognitive focus."
        elif aai_score <= 85.0:
            status = "ELEVATED_SYMPATHETIC_HYPERAROUSAL"
            guidance = "Frequent spontaneous SCR bursts (> 5/min). Acute sympathetic surge; schedule a 3-minute somatic reset."
        else:
            status = "CRITICAL_ACUTE_STRESS_SPIKE"
            guidance = "Continuous sudomotor discharge with high tonic SCL. Execute prolonged exhalation breathing immediately."

        return {
            "total_duration_sec": round(total_duration_sec, 2),
            "mean_tonic_scl_us": round(mean_scl, 3),
            "min_scl_us": round(min_scl, 3),
            "max_scl_us": round(max_scl, 3),
            "scr_event_count": scr_count,
            "nsscr_frequency_per_min": nsscr_frequency_per_min,
            "mean_scr_amplitude_us": mean_peak_amplitude,
            "autonomic_arousal_index": aai_score,
            "status": status,
            "actionable_guidance": guidance,
            "detected_peaks": scr_peaks[:10]  # First 10 peaks preview
        }
