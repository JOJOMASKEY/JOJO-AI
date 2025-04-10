# Final full code for src/power_mode.py

import json
from pathlib import Path

POWER_MODE_PATH = Path("data/power_mode.json")
DEFAULT_MODE = "medium"
VALID_MODES = ["low", "medium", "full"]

def get_power_mode():
    if POWER_MODE_PATH.exists():
        try:
            with open(POWER_MODE_PATH, "r") as f:
                data = json.load(f)
                mode = data.get("mode", DEFAULT_MODE)
                return mode if mode in VALID_MODES else DEFAULT_MODE
        except Exception:
            return DEFAULT_MODE
    return DEFAULT_MODE

def set_power_mode(mode):
    if mode not in VALID_MODES:
        raise ValueError(f"Invalid power mode: {mode}")
    POWER_MODE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(POWER_MODE_PATH, "w") as f:
        json.dump({"mode": mode}, f, indent=2)

def is_gpt_enabled():
    return get_power_mode() in ["medium", "full"]

def is_voice_enabled():
    return get_power_mode() in ["medium", "full"]

def is_gpt4_enabled():
    return get_power_mode() == "full"
