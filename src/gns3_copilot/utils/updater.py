import json
import subprocess
import sys
import urllib.request

from packaging.version import InvalidVersion, Version

PYPI_URL = "https://pypi.org/pypi/gns3-copilot/json"


def get_installed_version() -> str:
    from gns3_copilot import __version__

    return __version__


def get_latest_version() -> str:
    with urllib.request.urlopen(PYPI_URL, timeout=5) as response:
        data = json.loads(response.read().decode())
        return data["info"]["version"]


def is_update_available() -> tuple[bool, str, str]:
    current = get_installed_version()
    latest = get_latest_version()

    try:
        if current == "unknown":
            return False, current, latest
        return Version(latest) > Version(current), current, latest
    except InvalidVersion:
        return False, current, latest


def run_update() -> tuple[bool, str]:
    """Update gns3-copilot from PyPI"""
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "gns3-copilot",
            ],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

        if result.returncode == 0:
            # Check if anything was actually upgraded
            if (
                "Successfully installed" in result.stdout
                or "Requirement already satisfied" in result.stdout
            ):
                return (
                    True,
                    "✅ Update completed successfully. Please restart GNS3 Copilot to use the new version.",
                )
            else:
                return (
                    True,
                    "✅ No updates needed. You're already on the latest version.",
                )
        else:
            return False, f"❌ Update failed:\n{result.stderr}"

    except subprocess.TimeoutExpired:
        return False, "❌ Update timed out after 5 minutes. Please try again."
    except Exception as e:
        return False, f"❌ Unexpected error during update: {str(e)}"
