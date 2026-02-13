"""Smoke tests for governance and trust validation."""

import os
from pathlib import Path


def test_repository_structure():
    """Verify essential repository files exist."""
    root = Path(__file__).parent.parent.parent
    
    required_files = [
        "README.md",
        "LICENSE",
        "SECURITY.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "CHANGELOG.md",
        "CLA.md",
        "NOTICE",
        "pyproject.toml",
        "Makefile",
        ".gitignore",
        ".env.example",
    ]
    
    for file in required_files:
        assert (root / file).exists(), f"Required file missing: {file}"


def test_governance_docs_exist():
    """Verify governance documentation exists."""
    root = Path(__file__).parent.parent.parent
    
    required_docs = [
        "Docs/architecture/IP_POLICY.md",
        "Docs/architecture/DESIGN.md",
    ]
    
    for doc in required_docs:
        assert (root / doc).exists(), f"Required doc missing: {doc}"


def test_readme_contains_trust_sections():
    """Verify README contains required trust and transparency sections."""
    root = Path(__file__).parent.parent.parent
    readme = (root / "README.md").read_text()
    
    required_sections = [
        "DEMO vs REAL",
        "License",
        "IP & Collaboration",
        "Security & Vulnerability",
        "Ownership",
        "AS-IS",
    ]
    
    for section in required_sections:
        assert section in readme, f"README missing section: {section}"


def test_security_contact_configured():
    """Verify security contact is configured."""
    root = Path(__file__).parent.parent.parent
    security_md = (root / "SECURITY.md").read_text()
    
    assert "contact@aikungfu.dev" in security_md, "Security contact not configured"
    assert "DO NOT open a public issue" in security_md, "Missing vulnerability reporting guidance"


def test_license_is_cc_by_nc_nd():
    """Verify license is CC BY-NC-ND 4.0."""
    root = Path(__file__).parent.parent.parent
    license_text = (root / "LICENSE").read_text()
    
    assert "CC BY-NC-ND" in license_text or "NonCommercial" in license_text, \
        "License must be CC BY-NC-ND 4.0"


def test_cla_exists():
    """Verify Contributor License Agreement exists."""
    root = Path(__file__).parent.parent.parent
    cla = (root / "CLA.md").read_text()
    
    assert "Contributor License Agreement" in cla, "CLA document incomplete"
    assert "Community Benefit" in cla, "CLA missing community benefit clause"


def test_ip_policy_covers_data_governance():
    """Verify IP policy covers data governance."""
    root = Path(__file__).parent.parent.parent
    ip_policy = (root / "Docs/architecture/IP_POLICY.md").read_text()
    
    required_sections = [
        "Data Governance",
        "Real vs. Demo",
        "Parish Data Rights",
        "Audit Trail",
    ]
    
    for section in required_sections:
        assert section in ip_policy, f"IP policy missing: {section}"


if __name__ == "__main__":
    test_repository_structure()
    test_governance_docs_exist()
    test_readme_contains_trust_sections()
    test_security_contact_configured()
    test_license_is_cc_by_nc_nd()
    test_cla_exists()
    test_ip_policy_covers_data_governance()
    print("✓ All governance smoke tests passed")

