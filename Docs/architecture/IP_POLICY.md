# Intellectual Property Policy

This document defines ownership, permitted use, collaboration boundaries, and redistribution constraints for Catholic Network Tools.

---

## 1. Ownership

### Current Ownership

Catholic Network Tools is **community-owned infrastructure** stewarded by its contributors and adopting parishes.

- **Code ownership**: Contributors retain moral rights; Project retains CC BY-NC-ND 4.0 distribution rights
- **Data ownership**: Each parish owns its own operational data (attendance, donations, records)
- **Collective governance**: License and governance changes require majority community consent

### Future Ownership Transitions

If the project transfer to another steward, these principles apply:

1. **Non-profit requirement**: Successor must be a Catholic organization or non-profit
2. **Community consent**: Majority of active parish users must approve the transfer
3. **License preservation**: CC BY-NC-ND 4.0 remains in effect unless all contributors agree otherwise
4. **Data portability**: All parish data remains portable (export in standard formats)

---

## 2. Permitted Uses

### ✅ Allowed

**Community Use:**
- Installation in parishes (any diocese, any country)
- Adaptation for local needs (maintaining CC BY-NC-ND 4.0)
- Integration with other open-source tools (same license)
- Educational use (teaching about community tech)
- Research (with attribution and community benefit)

**Individual/Organizational Use:**
- Forking under CC BY-NC-ND 4.0
- Creating derivative works (must remain open, non-commercial)
- Submitting improvements back (via CLA)
- Commercial support/consulting (around the tool, not extracting data)

### ❌ Not Allowed

**Commercial Extraction:**
- Selling access to the tool or parish data
- Creating a SaaS version to monetize parishes
- Licensing the tool to third parties without CC BY-NC-ND
- Using parish data for advertising, analytics, or resale

**Data Misuse:**
- Selling or sharing parish donation data
- Using attendance data for social pressure or surveillance
- Profiling parishioners for external use
- Sharing sacramental records with non-authorized parties

**Competitive Forking:**
- Creating a proprietary fork to undercut the original project
- Claiming the tool as your own without attribution
- Modifying to hide that it's based on Catholic Network Tools

---

## 3. Collaboration Boundaries

### When Collaboration is Welcome

- **Bug fixes and improvements**: Submit via pull request (requires CLA)
- **Documentation and translations**: Always welcome
- **New modules serving community needs**: Design discussion first, then PR
- **Integration with other Catholic tech**: Coordinate to prevent duplication

### When Collaboration is Not Permitted

- **Extracting confidential parish data**
- **Building commercial extensions without community approval**
- **Forking to create a proprietary competitor**
- **Using the tool to surveil or control parishioners**

### Collaboration Process

1. **Open an issue** describing your proposed change
2. **Wait for feedback** from maintainers (max 7 days)
3. **Design discussion** if it's a significant change (optional)
4. **Submit PR** with tests and documentation
5. **Sign CLA** (if first-time contributor)
6. **Merge** once approved

---

## 4. Attribution & Credit

### Required Attribution

Any use of Catholic Network Tools must include:

1. **Visible acknowledgment** that this is based on Catholic Network Tools
2. **Link to GitHub repository**: https://github.com/gabrielmahia/catholic-network-tools
3. **License notice**: "Licensed under CC BY-NC-ND 4.0"

### Contributor Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` (automatic on merge)
- Release notes for their features
- Annual project acknowledgments
- Academic citations (if published)

### Parish Attribution

Parishes using the tool are invited to be listed in:
- `PARISHES.md` (with permission only)
- Community case studies
- Documentation examples

---

## 5. Redistribution Constraints

### Under CC BY-NC-ND 4.0

You **may**:
- Share the code with other parishes (non-commercial)
- Modify the code for your own use
- Create derivative works for community use
- Distribute under the same CC BY-NC-ND license

You **may not**:
- Use commercially or sell access
- Create closed-source derivatives
- Remove attribution or license notices
- Distribute modified versions under different terms

### If You Want Different Terms

**Alternative licenses require community approval:**

If you want to use Catholic Network Tools under different terms (e.g., MIT, Apache 2.0, proprietary), you must:

1. Contact contact@aikungfu.dev with your use case
2. Describe why you need different terms
3. Propose how you'll maintain community benefit
4. Wait for community vote (if significant change)
5. Implement changes only after approval

**This protects against:**
- Surprise license changes
- Sudden commercial extraction
- Loss of community control

---

## 6. Data Governance

### Real vs. Demo Data

**Real Data** (audit-protected):
- Parish attendance records
- Donation and stewardship data
- Volunteer hours and assignments
- Sacramental records (baptism, marriage, funeral)
- Stored with encryption, audit trails, access control

**Demo Data** (sample use):
- Fake parish templates
- Synthetic volunteer profiles
- Test donation amounts
- Clearly labeled as demo in all outputs

**Rule**: Real and demo data are in separate databases. Never mixed.

### Parish Data Rights

Each parish:
- **Owns** its own data (attendance, donations, records)
- **Controls** who accesses its data
- **Can export** data at any time in standard formats (CSV, JSON)
- **Can delete** its data from the system
- **Is not surveilled** by the tool authors for analytics

### Audit Trail Requirement

All changes to real data are logged:
- Who made the change
- What changed
- When it changed
- Why (linked to event or feature)

Audit logs are:
- Accessible to parish administrators
- Exportable for external audit
- Never used for surveillance
- Protected under data governance policy

---

## 7. Security & Privacy

### Encryption Standards

- **At rest**: AES-256 for parish data
- **In transit**: TLS 1.3 for all communications
- **Keys**: Rotated annually, stored securely

### Privacy Boundaries

- No analytics on parish usage
- No tracking of volunteer activity
- No profiling of parishioners
- No third-party integrations without explicit parish consent

### External Access

- Donations data: Never shared externally
- Attendance: Retained for parish use only
- Sacramental records: Only accessible to authorized parish staff

---

## 8. Enforcement & Violations

### Reporting IP Violations

If you discover unauthorized use:

1. Email contact@aikungfu.dev with:
   - What is being violated (license, data sharing, etc.)
   - How you discovered it
   - Impact on the community
   - Proposed resolution

2. Maintainers will investigate within 7 days
3. Action taken within 14 days (cease-and-desist, DMCA, etc.)

### Community Remedy

The community (parishes and contributors) may:
- Vote to ban a contributor or fork
- Require a violator to relicense under CC BY-NC-ND
- Fork the project if governance fails

---

## 9. Amendments to This Policy

Changes to IP policy require:

1. **Community discussion**: 14-day comment period
2. **Contributor vote**: 2/3 majority of active contributors
3. **Parish approval**: Majority of active parish users (if significant)
4. **Retroactive effect**: Applies to future contributions only

Past contributions retain their original license terms.

---

## 10. Questions?

For IP questions, email: contact@aikungfu.dev

Examples:
- "Can I use this in my commercial Catholic app?"
- "Can I fork this to create a proprietary product?"
- "Can I share parish data with my analytics vendor?"
- "Can I license this under Apache 2.0?"

