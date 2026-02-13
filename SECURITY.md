# Security Policy

## Reporting a Vulnerability

If you discover an error:

DO NOT open a public issue.

Email directly to:

contact@aikungfu.dev

---

## Reporting Guidelines

When reporting a vulnerability, please include:

1. **Description**: Clear explanation of the vulnerability
2. **Steps to Reproduce**: How to trigger the issue
3. **Impact Assessment**: What data or systems are affected
4. **Environment**: OS, Python version, configuration where discovered

**Expected Response Time:** 48 hours

---

## Security Scope

This project covers:

- Data encryption (at rest and in transit)
- Authentication and authorization
- SQL injection and code injection vulnerabilities
- Cross-site scripting (XSS) vulnerabilities
- Insecure deserialization
- Dependency vulnerabilities (via CodeQL)
- Configuration and secret management

---

## Supported Versions

| Version | Status | Support |
|---------|--------|---------|
| Latest | Active | Full security support |
| Previous | Maintenance | Critical fixes only |
| Older | End-of-Life | No support |

---

## Security Best Practices for Users

### For Parish Coordinators

1. **Never share API keys or credentials** in issues or discussions
2. **Keep the tool updated** to get security patches
3. **Use strong passwords** for admin accounts
4. **Enable offline mode** to prevent data exposure during transit
5. **Audit access logs** regularly

### For Deployers

1. **Use HTTPS** for all web communications
2. **Rotate secrets** regularly
3. **Restrict network access** to SMS and database services
4. **Monitor audit trails** for unauthorized access
5. **Test backup/recovery** procedures monthly

---

## Vulnerability Disclosure Timeline

- **Day 1**: Vulnerability reported to contact@aikungfu.dev
- **Day 2**: Acknowledgment and initial assessment
- **Day 3-7**: Patch development and testing
- **Day 8**: Public disclosure (if not already patched)
- **Day 9**: Full postmortem available

---

## Credits

We thank all security researchers and community members who responsibly disclose vulnerabilities.

