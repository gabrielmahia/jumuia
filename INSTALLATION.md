# Installation & Deployment Guide

## For Your Parish

### Option 1: Use Our Hosted Instance (Easiest)

Visit **https://catholic-network-tools.streamlit.app/**

Click "Select Your Parish" and start using immediately. No installation needed.

---

### Option 2: Deploy Your Own Instance (Recommended for Privacy)

Your parish can have its own **private or public** Streamlit app in 15 minutes.

#### **Step 1: Fork the Repository** (3 min)

1. Go to https://github.com/gabrielmahia/catholic-network-tools
2. Click **Fork** (top right)
3. Choose your account (or create a GitHub account first—free)

#### **Step 2: Create Streamlit Account** (2 min)

1. Go to https://streamlit.io/cloud
2. Click **Sign up with GitHub**
3. Authorize Streamlit (takes 30 seconds)

#### **Step 3: Deploy Your App** (5 min)

In Streamlit Cloud:
1. Click **Create new app**
2. Select your forked repository
3. Select **main** branch
4. Main file path: **app/01_Home.py**
5. Click **Deploy**

**That's it.** Streamlit builds + deploys automatically.

Your parish now has: **https://[your-username]-catholic-network-tools.streamlit.app/**

#### **Step 4: Customize Your Parish Data** (5 min)

1. Go back to your GitHub fork
2. Edit `app/config/parish-config.json`:
   ```json
   {
     "parish_name": "All Saints Catholic Church",
     "location": "Virginia",
     "diocese": "Arlington",
     "priest": "Fr. Steve Johnson",
     "contact_email": "allsaints@example.com",
     "founded": 1895,
     "parishioners": 650
   }
   ```
3. Commit changes (GitHub will auto-redeploy in 1 min)
4. Done! Your app now shows your parish info

#### **Step 5: Invite Parishioners** (ongoing)

Share the link in:
- Sunday bulletin
- Parish WhatsApp group
- Email newsletter
- Church announcements

Parishioners create GitHub accounts (free) and log in to contribute data.

---

## Data Storage (GitHub)

All parish data is stored in simple files:

```
parishes/
├── allsaints-Virginia/
│   ├── config.json (parish info)
│   ├── attendance.csv (who attended Mass?)
│   ├── sacraments.json (baptisms, marriages, etc.)
│   ├── volunteers.csv (who's available when?)
│   ├── giving.csv (donations—anonymously if desired)
│   ├── pastoral-care.csv (visits made)
│   ├── justice-campaigns.csv (advocacy activities)
│   └── formation.csv (catechesis attendance)
│
├── consolata-westlands/
│   ├── config.json
│   ├── attendance.csv
│   └── [same structure]
│
└── template/ (copy this to create a new parish)
    ├── config.json
    ├── attendance.csv
    └── [empty templates]
```

### How Data Works

**Parishioner enters data in Streamlit app:**
```
App → Validates → Formats → Commits to GitHub
```

**GitHub stores it permanently:**
- All changes tracked (who changed what, when?)
- History accessible (revert mistakes instantly)
- Fully transparent (anyone can see the data)
- Forkable (anyone can create their own copy)

**Streamlit reads from GitHub:**
```
App → Reads CSVs/JSONs → Displays dashboards
```

No database needed. No server needed. **Costs $0.**

---

## For Dioceses (Multiple Parishes)

### Option A: Unified Dashboard (Recommended)

One app aggregates data from all diocesan parishes.

**Setup (30 min):**
1. Fork the repository
2. Configure for each parish (edit `config.json` for each)
3. Deploy main app
4. Deploy sub-app for each parish (or embed in main)
5. Diocese sees: aggregate data across all parishes

**Bishop sees:**
- Total parishioners engaged (all parishes)
- Which parishes leading in justice work?
- Formation trends (are young people engaging?)
- Giving patterns (is stewardship healthy?)
- Best practices (St. James doing well with youth—share with others)

### Option B: Each Parish Owns Their Data

Each parish manages its own Streamlit instance. Diocese compiles reports manually.

(Less elegant but ensures maximum parish autonomy.)

---

## Tech Requirements

- ✅ **GitHub account** (free)
- ✅ **Streamlit account** (free)
- ✅ **Internet connection**

That's all. No servers. No credit card needed. No coding experience needed.

---

## Common Questions

**Q: Is my data private?**

A: You control privacy levels:
- Public parish: Data on GitHub (anyone can see)
- Private parish: Data in private GitHub repo (only invited parishioners see)

We recommend: **Public is better.** Transparency builds trust. But it's your choice.

**Q: What if Streamlit Cloud shuts down?**

A: Your data is on GitHub (permanent). You can:
1. Deploy to another Streamlit instance
2. Run locally on a computer (`streamlit run app/01_Home.py`)
3. Export data to Excel/CSV

You own your data. It's never locked in.

**Q: Can we use this offline?**

A: Yes!

Option 1: Clone repo, run locally (no internet needed for reading data)
```bash
git clone https://github.com/yourname/catholic-network-tools
cd catholic-network-tools
pip install -r requirements.txt
streamlit run app/01_Home.py
```

Option 2: Download CSVs, run Excel/Google Sheets (data stored offline)

**Q: How do we handle conflicts if 2 people edit same data?**

A: GitHub handles it:
- Last edit wins
- Full history available (can revert)
- Notifications sent to admins

Best practice: Designate one person per dimension to edit data (e.g., pastoral coordinator edits pastoral-care.csv).

**Q: Do we need a webmaster?**

A: No! Streamlit auto-deploys when you update GitHub. No technical knowledge needed.

One person can manage:
1. Update CSVs (using GitHub's web interface)
2. Check Streamlit app (autorefreshes)
3. Done

**Q: How do we handle sensitive data (abuse, mental health)?**

A: 

Option 1: Keep sensitive notes in password-protected Google Doc (linked from app but not public)

Option 2: Streamlit authentication (password-protect certain pages)

Option 3: Don't store sensitive data—just track "needs pastoral care, category: mental health" and keep details private with pastoral team

---

## Costs

| Tier | Cost | Use Case |
|---|---|---|
| Streamlit Cloud (free) | $0 | Single parish, <1M page views/month |
| Streamlit Cloud (paid) | $5/month | 2-3 parishes, unlimited usage |
| GitHub (free) | $0 | Unlimited repos, unlimited users |
| Domain name (optional) | $12/year | Custom URL (e.g., stmary.catholic-network.org) |

**Total cost for a parish: $0 - $17/year**

(Compare to typical parish management software: $300-1000/year)

---

## Support

**Questions?**

1. **GitHub Discussions:** https://github.com/gabrielmahia/catholic-network-tools/discussions
2. **Email:** contact@aikungfu.dev
3. **Streamlit Docs:** https://docs.streamlit.io

**Videos:**
- Coming soon: 5-min setup video
- Coming soon: How to invite parishioners
- Coming soon: How to customize for your parish

---

## Next Steps

1. **This week:** Fork the repo + deploy your instance
2. **Next week:** Customize parish config + invite pastoral team
3. **Week 3:** Invite parishioners + start with one dimension (e.g., sacraments or pastoral care)
4. **Month 2:** Add more dimensions based on parish priorities
5. **Month 3+:** See engagement + adjust based on what matters to your community

---

**You've got this.** The hardest part is belief that it's possible. It is. And it's simpler than you think.

🙏 Let's build this together.
