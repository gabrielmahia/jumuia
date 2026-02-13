# 🔧 Fix Your Streamlit Deployment Form

You're on the right page! Just **fix these 2 fields** and you're done.

---

## ❌ CURRENT (WRONG)

```
Repository:  gabrielmahia/catholic-network-tools  ✓ CORRECT
Branch:      master                               ✗ WRONG (red error)
Main file:   streamlit_app.py                     ✗ WRONG (red error)
App URL:     catholic-network-tools-sjpfc8x2xh7nm nbwip4nj6.streamlit.app ✓ OK
```

---

## ✅ CORRECT (CHANGE TO THIS)

```
Repository:  gabrielmahia/catholic-network-tools  ✓ KEEP AS IS
Branch:      main                                 ← CHANGE: master → main
Main file:   app/01_Home.py                       ← CHANGE: streamlit_app.py → app/01_Home.py
App URL:     (auto-generated, leave as is)
```

---

## 📝 EXACT CHANGES

### Change 1: Branch Field

**Clear the field** (it currently says "master")

**Type:** `main`

---

### Change 2: Main File Path Field

**Clear the field** (it currently says "streamlit_app.py")

**Type:** `app/01_Home.py`

---

## ✅ AFTER CHANGES, YOUR FORM WILL SHOW:

```
Repository:  gabrielmahia/catholic-network-tools
Branch:      main                                 ← GREEN checkmark ✓
Main file:   app/01_Home.py                       ← GREEN checkmark ✓
App URL:     Domain is available (green)
```

---

## 🚀 THEN CLICK "DEPLOY"

That's it! Takes 30-60 seconds and your app is live.

**You'll see:**
```
Deploying...
Installing packages...
Launching Streamlit app...
✓ Your app is live!
```

---

## 📱 YOUR LIVE APP URL

After deployment completes, visit:

```
https://gabrielmahia-catholic-network-tools.streamlit.app
```

(Exact URL shown in Streamlit Cloud dashboard)

---

## ✨ WHAT HAPPENS NEXT

1. **App loads** with all 7 dimensions visible
2. **Login screen** appears (click "Login with GitHub")
3. **Select parish** from dropdown (Consolata Shrine or your custom one)
4. **Explore** - click through all 7 dimension pages
5. **Share link** with your parish

---

## 🎯 TL;DR - TWO CHANGES ONLY

| Field | Current | Change To |
|-------|---------|-----------|
| Branch | `master` | `main` |
| Main file | `streamlit_app.py` | `app/01_Home.py` |

**Everything else:** Leave as is.

**Click Deploy.**

**Done!** ✅

---

## 🆘 IF IT STILL SAYS "NOT FOUND"

After you click Deploy and it says "branch/file not found":

**This means it's checking gabrielmahia/catholic-network-tools repo directly.**

### Solution: Use YOUR Fork Instead

Change Repository field to:
```
YOUR-USERNAME/catholic-network-tools
```

(Replace YOUR-USERNAME with your actual GitHub username)

Then use:
```
Branch: main
Main file: app/01_Home.py
```

---

## 📸 VISUAL GUIDE

```
┌─────────────────────────────────────────┐
│ Deploy an app                           │
├─────────────────────────────────────────┤
│                                         │
│ Repository                              │
│ ┌─────────────────────────────────────┐ │
│ │gabrielmahia/catholic-network-tools │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Branch                                  │
│ ┌─────────────────────────────────────┐ │
│ │ main          ← TYPE THIS            │ │
│ └─────────────────────────────────────┘ │
│ (Should turn GREEN ✓)                   │
│                                         │
│ Main file path                          │
│ ┌─────────────────────────────────────┐ │
│ │ app/01_Home.py    ← TYPE THIS       │ │
│ └─────────────────────────────────────┘ │
│ (Should turn GREEN ✓)                   │
│                                         │
│ App URL (optional)                      │
│ ┌─────────────────────────────────────┐ │
│ │catholic-network-tools-sjpf...      │ │
│ └─────────────────────────────────────┘ │
│ (Domain is available - GREEN ✓)         │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │         [Deploy Button]             │ │
│ └─────────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

---

## ✅ You're Done!

Two field changes → Click Deploy → App is live in 1 minute.

**Welcome to Streamlit!** 🎉
