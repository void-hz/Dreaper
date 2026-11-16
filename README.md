# Dreaper

**AI-assisted network reconnaissance and security analysis platform.**

Dreaper is an educational, evidence-first security tooling project. Its initial release focuses on running Nmap service detection against explicitly authorised lab targets, parsing Nmap XML, and producing a structured JSON report.

> **Project status:** Early development — v0.1 reconnaissance foundation. AI analysis, vulnerability intelligence, exploit references, controlled validation, and the web dashboard are planned, not implemented yet.

## v0.1 goals

- Run an Nmap service/version scan against an authorised target.
- Preserve the original Nmap XML output as scan evidence.
- Parse discovered hosts, ports, states, services, and version information.
- Produce a machine-readable JSON report.
- Keep scan execution separate from parsing and reporting code.

## Planned architecture

```text
Authorised lab target
        |
        v
   Nmap scan
        |
        v
   scan.xml (evidence)
        |
        v
 Python XML parser
        |
        v
   report.json
        |
        v
 Human review
```

Future milestones may add vulnerability-intelligence correlation, AI-assisted investigation hypotheses, controlled lab-only validation, report generation, and a web dashboard. AI-generated hypotheses will always be distinguished from observed evidence and human-validated findings.

## Requirements

- Python 3.10 or newer
- Nmap installed and available on your PATH
- Git

The initial implementation uses only Python's standard library; no Python packages are required.

## Setup

Clone the repository:

```bash
git clone https://github.com/void-hz/Dreaper.git
cd Dreaper
```

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\\Scripts\\Activate.ps1
```

Check the prerequisites:

```bash
python --version
nmap --version
```

## Usage

Only scan systems you own or have explicit permission to assess. Start with an isolated lab VM.

```bash
python -m src.main --target 192.168.56.101 --authorized
```

Replace the example address with the IP or hostname of your own authorised lab target.

Dreaper writes:

- `scans/scan-<timestamp>.xml` — original Nmap XML output.
- `output/report-<timestamp>.json` — parsed scan data.

The `--authorized` option is an explicit acknowledgement that you have permission to scan the target; it is not a technical verification of permission.

## Safety and limitations

- Use Dreaper only on systems you own or are explicitly authorised to test.
- The tool does not exploit targets.
- An open port or detected version is not proof of a vulnerability.
- Version strings can be incomplete or misleading; validate findings independently.
- Scan outputs can contain sensitive information. They are ignored by Git and should not be committed.

## Development roadmap

- [x] Define project scope and evidence-first design
- [ ] v0.1: Nmap execution, XML parsing, JSON reporting, tests
- [ ] Vulnerability-intelligence correlation (CVE references and affected-version checks)
- [ ] AI-assisted analysis with structured, clearly labelled hypotheses
- [ ] Human-led validation and controlled lab-only checks
- [ ] Report generation and scan history
- [ ] Web dashboard and API

## Contributing

This is a learning project. The code will be developed incrementally with an emphasis on understanding each component, testing it, and documenting design decisions.

## License

No license has been selected yet. Until one is added, normal copyright restrictions apply; reuse is not automatically permitted.
