# Changelog

All notable changes to Catholic Network Tools will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- **Governance Foundation**
  - CC BY-NC-ND 4.0 licensing with community stewardship protection
  - Contributor License Agreement (CLA) framework
  - Security policy with vulnerability reporting channel
  - Code of Conduct emphasizing parish-centered values
  - IP hardening: copyright headers, ownership statements

- **Architecture Documentation**
  - Offline-first data synchronization design
  - CRDT-based conflict resolution strategy
  - Event-sourced audit trail specification
  - Data classification (REAL vs DEMO zones)
  - SMS fallback protocol for low-bandwidth zones

- **Development Infrastructure**
  - Python 3.11+ project structure
  - Pre-commit hooks (lint, format, security)
  - Ruff linting configuration
  - pytest test framework baseline
  - GitHub Actions CI/CD (lint, test, security scan)
  - Makefile automation for common tasks

- **Project Templates**
  - Coordination module scaffold
  - Stewardship module scaffold
  - Resilience module scaffold
  - Formation module scaffold
  - Accessibility module scaffold

- **Documentation**
  - README with quick-start guides (Westlands/Marallal contexts)
  - Contributing workflow documentation
  - Deployment guide (Docker, k3s)
  - SMS integration setup
  - Offline mode testing guide

### Changed

- N/A (initial release planning)

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- N/A

### Security

- Vulnerability reporting email: contact@aikungfu.dev
- No public security issues
- All dependencies tracked for vulnerability scanning

---

## Versioning Strategy

### Major (X.0.0)
- Significant architectural changes
- Breaking API changes
- License or governance changes

### Minor (0.X.0)
- New features (offline sync, new modules)
- Backward-compatible additions
- Documentation improvements

### Patch (0.0.X)
- Bug fixes
- Security patches (released immediately)
- Minor improvements

### Pre-release
- Alpha: Early feature testing
- Beta: Community testing in real parishes
- RC: Ready for production deployment

---

## Release Notes Template

For each release, include:

1. **Summary**: What problem does this solve?
2. **For Coordinators**: How to update and what's new for them
3. **For Developers**: What APIs changed, deprecations, migration guide
4. **For Deployers**: How to upgrade, config changes, data migration
5. **Security**: Any vulnerabilities fixed
6. **Contributors**: Who helped make this release

---

## Deprecation Policy

- Features marked deprecated receive 2 releases notice
- Breaking changes only in major versions
- Security changes may break compatibility without notice

---

## Historical Context

Catholic Network Tools began as a response to coordination challenges in Catholic parishes across Kenya's diverse contexts—from high-connectivity urban areas (Westlands) to resource-constrained rural zones (Marallal).

Initial design principles:
1. **Offline-first**: Must work 7+ days without connectivity
2. **Trust-native**: Data is sacred; never extracted for external use
3. **Canonically-respecting**: Never supersedes diocesan authority
4. **Community-owned**: Licensed under CC BY-NC-ND 4.0 to prevent commercial fork
5. **Humble technology**: Succeed with SMS fallback before betting on WiFi

