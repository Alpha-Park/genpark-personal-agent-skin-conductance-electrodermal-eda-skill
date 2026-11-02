---
name: genpark-personal-agent-skin-conductance-electrodermal-eda-skill
description: Deterministic decomposition of Electrodermal Activity (EDA/GSR), tonic Skin Conductance Level (SCL), phasic SCR bursts, and autonomic arousal monitoring.
version: 1.0.0
author: GenPark Autonomous Agents Ecosystem
license: MIT
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
---

# Electrodermal Activity (EDA) & Skin Conductance Skill

## Overview
The `genpark-personal-agent-skin-conductance-electrodermal-eda-skill` provides sovereign personal agents with real-time psychophysiological monitoring of electrodermal activity (EDA), also known as Galvanic Skin Response (GSR). Palmar and plantar eccrine sweat glands are uniquely innervated by postganglionic sympathetic cholinergic fibers. By decomposing continuous conductance signals into slow tonic background (Skin Conductance Level, SCL) and rapid phasic fluctuations (Skin Conductance Responses, SCRs), this skill tracks cognitive workload, orienting responses, and acute sympathetic arousal surges.

## Physiological Model & Mathematics
1. **Tonic vs Phasic Decomposition**:
   $$\text{EDA}(t) = \text{SCL}_{\text{tonic}}(t) + \text{SCR}_{\text{phasic}}(t)$$
2. **Non-Specific SCR Frequency ($NSSCR$ rate)**:
   $$\text{NSSCR Frequency} = \frac{N_{\text{peaks}}}{\Delta T_{\text{minutes}}}$$
   - **Resting / Relaxed Baseline**: $1 - 3\text{ peaks/min}$.
   - **Active Alert Engagement**: $4 - 6\text{ peaks/min}$.
   - **Acute Sympathetic Hyperarousal**: $\ge 7 - 8\text{ peaks/min}$.
3. **Phasic Peak Detection Criterion**:
   $$\Delta \text{Conductance} \ge 0.05\,\mu\text{S} \quad (\text{rise time } 1 - 3\text{ seconds})$$
4. **Autonomic Arousal Index ($AAI$)**:
   Synthesizes mean tonic SCL and phasic burst frequency into a normalized 0 to 100 arousal metric.

## Tools & Endpoints
- `analyze_eda_stream`: Decomposes raw conductance data, detects individual SCR events, and computes the Autonomic Arousal Index.
