# Electrodermal Activity (EDA) & Skin Conductance Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](https://github.com/alphaparkinc/genpark-personal-agent-skin-conductance-electrodermal-eda-skill)
[![OpenClaw Ready](https://img.shields.io/badge/OpenClaw-Compatible-purple.svg)](https://github.com/alphaparkinc/genpark-personal-agent-skin-conductance-electrodermal-eda-skill)
[![MCP Protocol](https://img.shields.io/badge/MCP-Standard-orange.svg)](https://modelcontextprotocol.io/)

A sovereign personal agent capability for computational psychophysiology, decomposing Electrodermal Activity (EDA/GSR), tracking tonic SCL, and quantifying phasic SCR sudomotor bursts.

## Architecture

```mermaid
flowchart TD
    SensorStream["Raw EDA Stream (microsiemens, uS)"] --> BaselineFilter["Moving Baseline Extraction Engine"]
    BaselineFilter --> TonicSCL["Tonic Skin Conductance Level (SCL: 2 - 15 uS)"]
    BaselineFilter --> PhasicDetrend["Phasic Signal Isolation (EDA - Baseline)"]
    PhasicDetrend --> PeakDetector["SCR Peak Detector (Delta >= 0.05 uS, Rise Time 1-3s)"]
    PeakDetector --> FrequencyEngine["Non-Specific SCR Frequency (NSSCRs / min)"]
    TonicSCL & FrequencyEngine --> AAI["Autonomic Arousal Index (AAI: 0 - 100)"]
    AAI --> Coaching["OpenClaw / Hermes Sympathetic Calming Protocols"]
```

## Quickstart

```python
from client import ElectrodermalActivityClient

client = ElectrodermalActivityClient()

# Analyze an EDA stream (10 Hz)
samples = [4.1, 4.15, 4.22, 4.58, 4.82, 4.70, 4.45, 4.25, 4.20]  # Example series
res = client.analyze_eda_stream(samples, sample_rate_hz=10.0)

print("Mean Tonic SCL:", res["mean_tonic_scl_us"], "uS")
print("NSSCR Frequency:", res["nsscr_frequency_per_min"], "bursts/min")
print("Arousal Index:", res["autonomic_arousal_index"], "/ 100")
print("Status:", res["status"])
```

## MCP Server Integration

Add to your `claude_desktop_config.json` or OpenClaw tool registry:

```json
{
  "mcpServers": {
    "electrodermal-activity": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-skin-conductance-electrodermal-eda-skill/mcp_server.py"]
    }
  }
}
```

## License
MIT License.
