"""
MCP Server for Electrodermal Activity (EDA) & Skin Conductance Phasic Response.
Exposes JSON-RPC endpoints for decomposing tonic SCL, detecting phasic SCR bursts, and scoring arousal.
"""

import json
import sys
from client import ElectrodermalActivityClient

client = ElectrodermalActivityClient()


def handle_request(request: dict) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "analyze_eda_stream",
                        "description": "Decomposes raw skin conductance timeseries into tonic SCL and phasic SCR bursts, calculating NSSCR frequency and Autonomic Arousal Index.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "conductance_samples_us": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Skin conductance readings in microsiemens (uS)"
                                },
                                "sample_rate_hz": {
                                    "type": "number",
                                    "default": 10.0,
                                    "description": "Sampling frequency in Hertz"
                                },
                                "scr_threshold_us": {
                                    "type": "number",
                                    "default": 0.05,
                                    "description": "Minimum peak threshold in uS for phasic SCR detection"
                                }
                            },
                            "required": ["conductance_samples_us"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "analyze_eda_stream":
            res = client.analyze_eda_stream(
                conductance_samples_us=args.get("conductance_samples_us", []),
                sample_rate_hz=args.get("sample_rate_hz", 10.0),
                scr_threshold_us=args.get("scr_threshold_us", 0.05)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {tool_name} not found"}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": "Invalid Request"}
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
