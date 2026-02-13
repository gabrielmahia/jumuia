# Contributing to Catholic Network Tools

Thank you for your interest in contributing to Catholic Network Tools. This document provides guidance on how to contribute effectively while respecting the community's stewardship values.

---

## Contributor License Agreement (CLA)

All contributors must sign the **Contributor License Agreement** before their first contribution is merged. The CLA protects:

- **Contributors**: Your legal rights to your work
- **Community**: The project's ability to operate under CC BY-NC-ND 4.0
- **Parishes**: That contributed code serves community interests, not commercial extraction

### How to Sign

1. Fork and clone the repository
2. Open your first pull request
3. A bot will post a link to sign the CLA digitally
4. Sign it (takes 2 minutes)
5. Your PR will be eligible for review

See `CLA.md` for full text.

---

## Types of Contributions

### Code Contributions

**Bug Fixes:**
- File an issue first (or email contact@aikungfu.dev if security-sensitive)
- Create a branch: `git checkout -b fix/issue-name`
- Include test cases
- Submit PR with fix description + test results

**Features:**
- Start a GitHub Discussion to discuss design
- Wait for architecture feedback
- Create a branch: `git checkout -b feature/feature-name`
- Follow module structure (see `Docs/architecture/DESIGN.md`)
- Include tests and documentation
- Submit PR

**Refactoring:**
- Document why refactor improves code quality
- Ensure all existing tests pass
- Add new tests if coverage gaps exist

### Documentation Contributions

- **Architecture**: Update `Docs/architecture/` if design changes
- **Guides**: Add user guides to `Docs/guides/`
- **API**: Update docstrings if API changes
- **Translations**: Contribute Swahili or other language translations

### Community Contributions

- **Help in Discussions**: Answer questions, provide examples
- **Test Reports**: Test on Marallal/offline networks, report findings
- **UI/UX**: Suggest interface improvements for low-bandwidth zones
- **Translations**: Swahili, Kikuyu, other local languages

---

## Development Workflow

### Setup

```bash
git clone https://github.com/gabrielmahia/catholic-network-tools.git
cd catholic-network-tools
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
pre-commit install
```

### Making Changes

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes, write tests
make test
make lint

# Commit with clear messages
git commit -m "feat: add offline sync conflict resolution"

# Push and open PR
git push origin feature/your-feature-name
```

### Testing Requirements

All contributions must include:

1. **Unit tests** for new functions
2. **Integration tests** for new features
3. **Smoke tests** for offline/online mode transitions
4. **Pass lint checks**: `make lint`
5. **Pass security scan**: `make security`

### Code Style

- **Python**: Follow PEP 8 (enforced by Ruff)
- **Git commits**: Clear, descriptive messages (see examples below)
- **Documentation**: Update docstrings for public APIs

#### Commit Message Examples

```
feat: add parish volunteer tracking module
fix: resolve offline sync conflict in donation records
docs: update offline architecture section
test: add CRDT merge test for simultaneous edits
refactor: simplify event sourcing storage layer
chore: update dependencies
```

---

## Pull Request Process

1. **Fill out PR template** with:
   - What changes, why
   - Testing done
   - Checklist of requirements

2. **Expect review** from maintainers within 7 days

3. **Address feedback** in follow-up commits (don't rebase)

4. **Merge** once approved and all checks pass

---

## Code of Conduct

All contributors agree to the Code of Conduct (see `CODE_OF_CONDUCT.md`). In summary:

- **Respect** parish and diocesan authority
- **Include** contributors from diverse backgrounds and regions
- **Communicate** clearly and charitably
- **Avoid** personal attacks, harassment, discrimination
- **Report** violations to contact@aikungfu.dev

---

## Questions or Ideas?

- **Feature discussion**: GitHub Discussions
- **Bug reports**: GitHub Issues (or email if security-sensitive)
- **Architecture questions**: Open a Discussion or email
- **Community feedback**: Email contact@aikungfu.dev

---

## Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` (automatic on merge)
- Release notes
- Annual acknowledgments

Thank you for serving the Catholic community through code!

