"""Dreaper v0.1 command-line entry point."""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys

from src.nmap_runner import NmapError, run_nmap
from src.parser import parse_nmap_xml
from src.reporter import write_json_report


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dreaper",
        description="Evidence-first network reconnaissance for authorised lab targets.",
    )
    parser.add_argument("--target", required=True, help="IP address or hostname of your authorised lab target.")
    parser.add_argument(
        "--authorized",
        action="store_true",
        help="Acknowledge that you own the target or have explicit permission to scan it.",
    )
    parser.add_argument("--timeout", type=int, default=300, help="Nmap timeout in seconds (default: 300).")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if not args.authorized:
        print("Refusing to scan: pass --authorized only when you have permission to test this target.")
        return 2

    if args.timeout < 1:
        print("Error: --timeout must be a positive number.")
        return 2

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    scan_path = PROJECT_ROOT / "scans" / f"scan-{timestamp}.xml"
    report_path = PROJECT_ROOT / "output" / f"report-{timestamp}.json"

    print("DREAPER v0.1 — Reconnaissance")
    print(f"[+] Target: {args.target}")
    print("[+] Running Nmap service/version scan...")

    try:
        run_nmap(args.target, scan_path, timeout=args.timeout)
        print(f"[+] Raw XML saved: {scan_path.relative_to(PROJECT_ROOT)}")

        data = parse_nmap_xml(scan_path)
        data["target"] = args.target
        data["generated_at"] = timestamp

        write_json_report(data, report_path)
        print(f"[+] JSON report saved: {report_path.relative_to(PROJECT_ROOT)}")

        for host in data["hosts"]:
            print(f"\nHost: {host['address']}")
            if not host["ports"]:
                print("  No port records found in the scan output.")
            for port in host["ports"]:
                version = " ".join(part for part in (port["product"], port["version"]) if part)
                print(
                    f"  {port['port']}/{port['protocol']} "
                    f"{port['state']} {port['service']} {version}".rstrip()
                )

        print("\n[!] A discovered service or version is not proof of a vulnerability.")
        print("[+] Scan processing complete.")
        return 0

    except (NmapError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
