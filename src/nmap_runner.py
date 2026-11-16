"""Run Nmap and preserve its XML output."""

from pathlib import Path
import shutil
import subprocess


class NmapError(RuntimeError):
    """Raised when Nmap cannot complete a scan."""


def run_nmap(target: str, xml_path: Path, timeout: int = 300) -> None:
    """Run service/version detection for one explicitly authorised target.

    Uses an argument list (never a shell command) and writes Nmap XML to disk.
    """
    nmap_path = shutil.which("nmap")
    if nmap_path is None:
        raise NmapError("Nmap was not found. Install Nmap and ensure it is on PATH.")

    if not target or target.startswith("-") or any(ch.isspace() for ch in target):
        raise ValueError("Provide one valid IP address or hostname.")

    xml_path.parent.mkdir(parents=True, exist_ok=True)
    command = [nmap_path, "-sV", "-oX", str(xml_path), target]

    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise NmapError(f"Nmap scan exceeded the {timeout}-second timeout.") from exc
    except OSError as exc:
        raise NmapError(f"Could not start Nmap: {exc}") from exc

    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "Unknown Nmap error"
        raise NmapError(detail)

    if not xml_path.exists() or xml_path.stat().st_size == 0:
        raise NmapError("Nmap finished but did not produce an XML file.")
