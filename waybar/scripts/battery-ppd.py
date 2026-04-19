#!/usr/bin/env python3
"""battery-ppd.py — Waybar custom module: battery icon + power-profile cycling.

Place at: ~/.config/waybar/scripts/battery-ppd.py

Displays battery icon (matching your original Nerd Font glyphs).
Tooltip shows percentage and current power profile.
On click (SIGRTMIN from waybar), cycles through power profiles.
"""

import json
import signal
import subprocess
import threading
import sys
from pathlib import Path

BAT = "BAT1"
BAT_PATH = Path(f"/sys/class/power_supply/{BAT}")

# ── Font Awesome 5 — discharging icons (low → full) ──
ICONS_DEFAULT = [
    "\uf244",  # 0-10%
    "\uf243",  # 11-30%
    "\uf242",  # 31-50%
    "\uf241",  # 51-75%
    "\uf240",  # 76-100%
]

# ── Material Design Icons — charging icons (11 steps) ──
ICONS_CHARGING = [
    "\U000f089f",  # 0-5%
    "\U000f089c",  # 6-14%
    "\U000f0086",  # 15-23%
    "\U000f0087",  # 24-32%
    "\U000f0088",  # 33-41%
    "\U000f089d",  # 42-50%
    "\U000f0089",  # 51-59%
    "\U000f089e",  # 60-68%
    "\U000f008a",  # 69-77%
    "\U000f008b",  # 78-90%
    "\U000f0085",  # 91-100%
]

PROFILES = ["balanced", "performance", "power-saver"]
PROFILE_LABELS = {
    "balanced": "Balanced",
    "performance": "Performance",
    "power-saver": "Power Saver",
}

# Event used to wake the main loop immediately after a profile change
wake = threading.Event()


def get_profile() -> str:
    try:
        result = subprocess.run(
            ["powerprofilesctl", "get"],
            capture_output=True, text=True, timeout=2,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def cycle_profile(_signum=None, _frame=None):
    current = get_profile()
    try:
        idx = PROFILES.index(current)
        next_profile = PROFILES[(idx + 1) % len(PROFILES)]
    except ValueError:
        next_profile = "balanced"
    subprocess.run(
        ["powerprofilesctl", "set", next_profile],
        capture_output=True, timeout=2,
    )
    wake.set()


def get_battery():
    try:
        capacity = int((BAT_PATH / "capacity").read_text().strip())
        status = (BAT_PATH / "status").read_text().strip()
    except (FileNotFoundError, ValueError):
        capacity, status = 0, "Unknown"
    return capacity, status


def pick_icon(capacity: int, status: str) -> str:
    if status == "Charging":
        idx = min(capacity * 10 // 100, 10)
        return ICONS_CHARGING[idx]
    else:
        if capacity <= 10:
            return ICONS_DEFAULT[0]
        elif capacity <= 30:
            return ICONS_DEFAULT[1]
        elif capacity <= 50:
            return ICONS_DEFAULT[2]
        elif capacity <= 75:
            return ICONS_DEFAULT[3]
        else:
            return ICONS_DEFAULT[4]


def pick_class(capacity: int, status: str) -> str:
    if status == "Charging":
        return "charging"
    # "Full", "Discharging", "Not charging", etc. all use default accent
    if capacity <= 10:
        return "critical"
    if capacity <= 25:
        return "warning"
    return "discharging"


def output():
    capacity, status = get_battery()
    icon = pick_icon(capacity, status)
    css_class = pick_class(capacity, status)
    profile = PROFILE_LABELS.get(get_profile(), "Unknown")

    data = {
        "text": icon,
        "tooltip": f"{capacity}% \u2014 {profile}",
        "class": css_class,
    }
    print(json.dumps(data, ensure_ascii=False), flush=True)


def main():
    signal.signal(signal.SIGRTMIN, cycle_profile)

    while True:
        output()
        wake.wait(timeout=30)
        wake.clear()


if __name__ == "__main__":
    main()
