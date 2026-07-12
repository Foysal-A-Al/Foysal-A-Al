from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
required = [
    ROOT / "README.md",
    ROOT / "SETUP.md",
    ROOT / "assets" / "hero.svg",
    ROOT / "assets" / "research-ecosystem.svg",
    ROOT / "assets" / "portfolio-lab.svg",
    ROOT / "assets" / "thesis-dashboard.svg",
    ROOT / "assets" / "footer.svg",
    ROOT / "github-metrics.svg",
    ROOT / ".github" / "workflows" / "metrics.yml",
    ROOT / ".github" / "workflows" / "summary-cards.yml",
    ROOT / ".github" / "workflows" / "profile-3d.yml",
    ROOT / ".github" / "workflows" / "snake.yml",
]

errors = []
for path in required:
    if not path.exists():
        errors.append(f"Missing: {path.relative_to(ROOT)}")

for svg in ROOT.rglob("*.svg"):
    try:
        ET.parse(svg)
    except Exception as exc:
        errors.append(f"Invalid SVG {svg.relative_to(ROOT)}: {exc}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for target in re.findall(r'src="(\./[^\"]+)"', readme):
    path = ROOT / target[2:]
    if not path.exists():
        errors.append(f"README references missing local file: {target}")

for placeholder in ["ADD_", "YOUR_USERNAME", "example.com"]:
    if placeholder in readme:
        errors.append(f"Unresolved placeholder: {placeholder}")

for path in [ROOT / "README.md", ROOT / "SETUP.md", *ROOT.rglob("*.svg")]:
    text = path.read_text(encoding="utf-8")
    if chr(0x2014) in text or chr(0x2013) in text:
        errors.append(f"Large dash character found in {path.relative_to(ROOT)}")

if errors:
    print("Profile validation failed:\n- " + "\n- ".join(errors))
    sys.exit(1)

print("Profile validation passed.")
