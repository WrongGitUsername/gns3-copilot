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
        response_text = response.read().decode()
        data: dict = json.loads(response_text)
        info: dict = data["info"]
        version: str = info["version"]
        return version


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
        result: subprocess.CompletedProcess[str] = subprocess.run(
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
                success_message: str = "Update completed successfully. Please restart GNS3 Copilot to use the new version."
                return True, success_message
            else:
                no_update_message: str = (
                    "No updates needed. You're already on the latest version."
                )
                return True, no_update_message
        else:
            error_message: str = f"Update failed:\n{result.stderr}"
            return False, error_message

    except subprocess.TimeoutExpired:
        timeout_message: str = "Update timed out after 5 minutes. Please try again."
        return False, timeout_message
    except Exception as e:
        exception_message: str = f"Unexpected error during update: {str(e)}"
        return False, exception_message
