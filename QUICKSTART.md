# Catholic Network Tools — Complete Setup Guide

## Welcome! 👋

You're about to deploy a global platform for parish coordination. This guide will walk you through it step-by-step.

**Total time:** 15 minutes  
**Technical skill needed:** None (copy-paste is enough)  
**Cost:** $0

---

## **STEP 1: Create Accounts (5 minutes)**

### GitHub Account (if you don't have one)

1. Go to https://github.com/signup
2. Enter email + password
3. Verify email
4. Done! (You now have a GitHub account)

### Streamlit Account

1. Go to https://streamlit.io/cloud
2. Click "Sign up with GitHub"
3. Authorize Streamlit
4. Done!

---

## **STEP 2: Fork the Repository (2 minutes)**

1. Go to https://github.com/gabrielmahia/catholic-network-tools
2. Click the **Fork** button (top right)
3. Select your account
4. Wait 5 seconds for fork to complete
5. You now have your own copy! URL will be: `https://github.com/YOUR-USERNAME/catholic-network-tools`

---

## **STEP 3: Deploy to Streamlit Cloud (5 minutes)**

1. In **Streamlit Cloud**, click "Create new app"
2. Select:
   - **GitHub repo:** your-username/catholic-network-tools
   - **Branch:** main
   - **Main file path:** app/01_Home.py
3. Click "Deploy"
4. Streamlit builds (takes 1-2 minutes)
5. Your app is live at: `https://your-username-catholic-network-tools.streamlit.app`

**Test it:** Click the app link. You should see the home dashboard with 7 dimensions.

---

## **STEP 4: Customize Your Parish (3 minutes)**

### Edit Parish Configuration

1. In GitHub, navigate to: `parishes/consolata-westlands/config.json`
2. Click the **pencil icon** (edit button)
3. Change these values to your parish:

```json
{
  "parish_name": "All Saints Catholic Church",
  "location": "Virginia",
  "diocese": "Arlington",
  "founded": 1895,
  "parishioners": 650,
  "dimensions_tracking": ["spiritual", "material", "community", "justice", "formation", "stewardship", "admin"]
}
```

4. Click "Commit changes"
5. Streamlit auto-deploys (watch the app refresh in ~1 minute)

---

## **STEP 5: Invite Your Parish (Ongoing)**

### Share the Link

1. Your app URL: `https://your-username-catholic-network-tools.streamlit.app`
2. Share in:
   - **Parish bulletin** (print or digital)
   - **WhatsApp group** (if you have one)
   - **Email newsletter** (to all parishioners)
   - **Church announcements**
   - **Social media** (Facebook, Instagram)

### What Parishioners Do

1. Visit the link
2. Click "Login with GitHub" (or create free GitHub account)
3. Select parish from dropdown
4. Fill profile
5. Start using!

---

## **OPTIONAL: Customize Further**

### Change Colors/Theme

The app uses green (Catholic color). To customize:

1. Edit `.streamlit/config.toml`
2. Change primaryColor, backgroundColor, etc.
3. Commit → Auto-deploys

### Add More Parishes

1. Duplicate `parishes/template/` folder
2. Rename to your parish name (e.g., `parishes/allsaints-Virginia/`)
3. Edit the config.json inside
4. Commit → Your new parish is available in the dropdown

### Add Sample Data

CSV files in `data/sample/` are used by the dashboard:

- `attendance.csv` — Mass attendance
- `giving.csv` — Donations
- More can be added (volunteers, pastoral care, etc.)

---

## **TROUBLESHOOTING**

### "My changes aren't showing up"

**Solution:** Streamlit takes 30-60 seconds to auto-deploy. Refresh the browser (Ctrl+R or Cmd+R).

### "Login button doesn't work"

**Solution:** Make sure you have a GitHub account and are logged in to GitHub.

### "App says 'Select your parish' but mine isn't listed"

**Solution:** 
1. Go to GitHub
2. Check `parishes/` folder
3. Make sure your parish folder has a `config.json` file
4. Refresh the Streamlit app

### "I want to delete my fork and start over"

**Solution:**
1. Go to GitHub → Settings → Danger Zone → Delete repository
2. Fork again from the original

---

## **USING THE APP**

### For Parishioners

**Sacraments Page:**
- See upcoming baptisms, marriages
- Add prayer intentions
- Join prayer circles

**Pastoral Care Page:**
- See who needs visits
- Log visits you make
- Join grief support groups

**Justice Page:**
- See active campaigns
- RSVP for rallies
- Write/share advocacy letters

**Formation Page:**
- Sign up for catechesis
- Track RCIA progress
- Join Bible studies

**Stewardship Page:**
- Make donations
- See where money goes
- Track impact

**Admin Page:**
- View Mass schedule
- See volunteer needs
- Access directory

### For Pastoral Teams

**Dashboard:**
- See all 7 dimensions at a glance
- KPIs (key metrics)
- Recent activity feed

**Each Dimension:**
- Track detailed data
- Log activities
- Generate reports

---

## **DATA MANAGEMENT**

### Where is my data stored?

Data is stored in **GitHub** (CSV/JSON files in the `parishes/` folder).

### Is my data private?

By default, **public** (visible to anyone). To make private:

1. Go to GitHub repo → Settings
2. Change visibility to "Private"
3. Only invited people can see data

### Can I backup my data?

Yes! Click "Download" button in Streamlit app, or download CSVs directly from GitHub.

### How do I delete my parish data?

Delete the CSV rows directly in GitHub (edit the file).

---

## **CONNECTING MULTIPLE PARISHES (Diocese)**

### Single Dashboard for All Parishes

To see all parishes in one view:

1. Create a new Streamlit app
2. Point to the same forked repository
3. Add a "Diocese View" page that aggregates all parish folders
4. Each parish folder feeds data to diocese dashboard

**Example:** Diocese of Arlington sees attendance + justice engagement from 22 parishes on one dashboard.

---

## **NEXT STEPS**

### Week 1: Foundation
- ✅ Deploy your app
- ✅ Invite pastoral team
- ✅ Test with sample data

### Week 2: First Dimension
- Pick the most important dimension (e.g., Sacraments or Pastoral Care)
- Start tracking real data
- Celebrate first entries!

### Week 3: Expand
- Add second dimension
- Train coordinators (DRE, pastoral associate, etc.)
- Share early wins in bulletin

### Month 2+: Full Scale
- All 7 dimensions active
- 50%+ of parishioners registered
- Monthly dashboard reports to leadership

---

## **SUPPORT**

### Questions?

1. **GitHub Discussions:** https://github.com/gabrielmahia/catholic-network-tools/discussions
2. **Email:** contact@aikungfu.dev
3. **Streamlit Docs:** https://docs.streamlit.io

### Feature Requests?

Open an issue on GitHub with:
- What you need
- Why it matters for your parish
- What problem it solves

### Found a Bug?

Report in GitHub Issues with:
- What happened
- What you expected
- How to reproduce it

---

## **Theology Refresh**

Remember **why** you're doing this:

The Church touches people's **whole lives**. This platform makes that visible + coordinated.

- 🛐 **Spiritual:** Sacraments = encounter with Christ
- 🍞 **Material:** Food = Gospel's care for hungry
- 👥 **Community:** Belonging = healing from isolation
- ⚖️ **Justice:** Advocacy = faith in action
- 👦 **Formation:** Education = faith deepens
- 💰 **Stewardship:** Transparency = trust built
- 📋 **Admin:** Order = mission enabled

---

## **You've Got This!** 🙏

In 15 minutes, you've deployed a global platform.

Your parish is now part of a worldwide network of Catholic communities transforming how we coordinate ministry.

**From Nairobi to Virginia to Manila—together, we're building the Church.**

---

**Questions? Email contact@aikungfu.dev or start a GitHub Discussion.**

**Made with ❤️ for parishes everywhere.**
