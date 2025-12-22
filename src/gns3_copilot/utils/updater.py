
import sys
import json
import subprocess
import urllib.request
from typing import Tuple
from packaging.version import Version, InvalidVersion

PYPI_URL = "https://pypi.org/pypi/gns3-copilot/json"


def get_installed_version() -> str:
    from gns3_copilot import __version__
    return __version__


def get_latest_version() -> str:
    with urllib.request.urlopen(PYPI_URL, timeout=5) as response:
        data = json.loads(response.read().decode())
        return data["info"]["version"]


def is_update_available() -> Tuple[bool, str, str]:
    current = get_installed_version()
    latest = get_latest_version()

    try:
        if current == "unknown":
            return False, current, latest
        return Version(latest) > Version(current), current, latest
    except InvalidVersion:
        return False, current, latest


def run_update() -> Tuple[bool, str]:
    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "gns3-copilot",
            ]
        )
        return True, "Update completed successfully. Please restart GNS3 Copilot."
    except subprocess.CalledProcessError as exc:
        return False, f"pip failed: {exc}"
