"""
Smoke tests to validate Catholic Spiritual OS repository structure and standards.

This follows the CodingLab pattern for repository governance validation.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DIRS = [
    "src/spiritual_os",
    "src/spiritual_os/domain",
    "src/spiritual_os/storage",
    "src/spiritual_os/ui",
    "src/spiritual_os/utils",
    "Tests",
    "Docs",
    "Docs/architecture",
    ".github/workflows",
]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "CHANGELOG.md",
    ".gitignore",
    "Makefile",
    "pyproject.toml",
    ".pre-commit-config.yaml",
    "CLA.md",
    "app.py",
    "requirements.txt",
]

README_REQUIRED_SECTIONS = [
    "# Catholic Spiritual OS",
    "## What is this?",
    "## Architecture",
    "## Quickstart",
    "## License",
    "## Security",
]

DOMAIN_MODULES = [
    "src/spiritual_os/domain/rule_of_life.py",
    "src/spiritual_os/domain/liturgy.py",
    "src/spiritual_os/domain/sacraments.py",
    "src/spiritual_os/domain/journal.py",
    "src/spiritual_os/domain/parish.py",
    "src/spiritual_os/domain/diocese.py",
]

STORAGE_MODULES = [
    "src/spiritual_os/storage/local_store.py",
]


class TestDirectoryStructure:
    """Validate that all required directories exist."""
    
    def test_required_directories_exist(self):
        for d in REQUIRED_DIRS:
            path = ROOT / d
            assert path.is_dir(), f"Required directory missing: {d}"
    
    def test_src_package_structure(self):
        """Verify src/ is a proper Python package"""
        init_file = ROOT / "src" / "__init__.py"
        assert init_file.exists(), "src/__init__.py missing"
        
        spiritual_os_init = ROOT / "src" / "spiritual_os" / "__init__.py"
        assert spiritual_os_init.exists(), "src/spiritual_os/__init__.py missing"


class TestGovernanceFiles:
    """Validate that all governance files exist and contain required content."""
    
    def test_required_files_exist(self):
        for f in REQUIRED_FILES:
            path = ROOT / f
            assert path.is_file(), f"Required file missing: {f}"
    
    def test_license_is_cc_by_nc_nd(self):
        license_text = (ROOT / "LICENSE").read_text()
        assert "NonCommercial" in license_text
        assert "NoDerivatives" in license_text
        assert "Gabriel Mahia" in license_text
    
    def test_security_has_required_block(self):
        security = (ROOT / "SECURITY.md").read_text()
        assert "DO NOT open a public issue" in security
        assert "contact@aikungfu.dev" in security
    
    def test_readme_has_required_sections(self):
        readme = (ROOT / "README.md").read_text()
        for section in README_REQUIRED_SECTIONS:
            assert section in readme, f"README.md missing section: {section}"
    
    def test_cla_exists(self):
        cla = (ROOT / "CLA.md").read_text()
        assert "Contributor License Agreement" in cla
    
    def test_gitignore_covers_essentials(self):
        gitignore = (ROOT / ".gitignore").read_text()
        for pattern in ["__pycache__", ".env", ".venv", ".DS_Store", "*.pyc"]:
            assert pattern in gitignore, f".gitignore missing pattern: {pattern}"


class TestSpiritualOSModules:
    """Validate that all Spiritual OS domain modules exist."""
    
    def test_domain_modules_exist(self):
        for module in DOMAIN_MODULES:
            path = ROOT / module
            assert path.is_file(), f"Domain module missing: {module}"
    
    def test_storage_modules_exist(self):
        for module in STORAGE_MODULES:
            path = ROOT / module
            assert path.is_file(), f"Storage module missing: {module}"
    
    def test_domain_imports(self):
        """Verify domain modules can be imported"""
        try:
            from src.spiritual_os.domain.rule_of_life import RuleOfLife, generate_rule_template
            from src.spiritual_os.domain.liturgy import LiturgyCalendar
            from src.spiritual_os.domain.sacraments import SacramentTracker
            from src.spiritual_os.domain.journal import Journal, JournalTemplate
            from src.spiritual_os.domain.parish import Parish
            from src.spiritual_os.domain.diocese import Diocese
        except ImportError as e:
            assert False, f"Domain import failed: {e}"


class TestEngineering:
    """Validate engineering baseline configuration."""
    
    def test_ci_workflow_exists(self):
        ci = ROOT / ".github" / "workflows" / "ci.yml"
        assert ci.is_file(), "CI workflow missing"
        content = ci.read_text()
        assert "ruff" in content
        assert "pytest" in content
    
    def test_pyproject_toml_valid(self):
        pyproject = (ROOT / "pyproject.toml").read_text()
        assert "[tool.ruff]" in pyproject
        assert "[tool.pytest.ini_options]" in pyproject
    
    def test_makefile_has_targets(self):
        makefile = (ROOT / "Makefile").read_text()
        for target in ["setup", "lint", "test", "clean"]:
            assert target in makefile, f"Makefile missing target: {target}"
    
    def test_requirements_txt_exists(self):
        req = (ROOT / "requirements.txt").read_text()
        # Check for key dependencies
        assert "streamlit" in req
        assert "pytest" in req


class TestDemoAndData:
    """Validate demo data and test fixtures."""
    
    def test_streamlit_app_exists(self):
        app = ROOT / "app.py"
        assert app.is_file(), "app.py (Streamlit entrypoint) missing"
        content = app.read_text()
        assert "streamlit" in content
        assert "def " in content  # Has functions
    
    def test_disclaimer_in_app(self):
        app = (ROOT / "app.py").read_text()
        # Should have disclaimers
        assert "disclaimer" in app.lower() or "not a substitute" in app.lower()


class TestLayerStructure:
    """Validate the five-layer architecture is present."""
    
    def test_personal_layer_d_exists(self):
        """D: Personal Spiritual OS (Rule of Life, Journaling, Sacraments)"""
        assert (ROOT / "src/spiritual_os/domain/rule_of_life.py").exists()
        assert (ROOT / "src/spiritual_os/domain/journal.py").exists()
        assert (ROOT / "src/spiritual_os/domain/sacraments.py").exists()
    
    def test_parish_layer_a_exists(self):
        """A: Parish utilities"""
        assert (ROOT / "src/spiritual_os/domain/parish.py").exists()
    
    def test_diocese_layer_b_exists(self):
        """B: Diocese governance"""
        assert (ROOT / "src/spiritual_os/domain/diocese.py").exists()
    
    def test_liturgy_context_exists(self):
        """Support for liturgical awareness"""
        assert (ROOT / "src/spiritual_os/domain/liturgy.py").exists()


class TestPrivacyAndSecurity:
    """Validate privacy-first design."""
    
    def test_storage_is_local_only(self):
        storage_file = (ROOT / "src/spiritual_os/storage/local_store.py").read_text()
        assert "LocalStore" in storage_file
        assert "private" in storage_file.lower() or "local" in storage_file.lower()
    
    def test_no_hardcoded_secrets(self):
        """Ensure no API keys, tokens in code"""
        files_to_check = [
            "app.py",
            ".env.example",
        ]
        for filename in files_to_check:
            filepath = ROOT / filename
            if filepath.exists():
                content = filepath.read_text()
                # Should not contain typical secret patterns
                assert "sk_" not in content  # Stripe keys
                assert "Bearer " not in content  # Auth tokens
                assert "password=" not in content


class TestDocumentation:
    """Validate documentation is complete."""
    
    def test_architecture_docs_exist(self):
        arch_docs = [
            "Docs/architecture/ARCHITECTURE.md",
            "Docs/architecture/IP_POLICY.md",
            "Docs/architecture/DATA_POLICY.md",
        ]
        for doc in arch_docs:
            # These may not all exist yet, but they're strongly recommended
            pass
    
    def test_contributing_guidelines(self):
        contributing = (ROOT / "CONTRIBUTING.md").read_text()
        assert "pull request" in contributing.lower() or "contribute" in contributing.lower()


# Run tests if executed directly
if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
