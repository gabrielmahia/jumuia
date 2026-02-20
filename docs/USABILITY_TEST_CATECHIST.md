# Catechist Coordinator — Usability Test Protocol
**Catholic Parish Steward · Week 2 Test**  
Version 1.0 · February 2026

---

## Purpose
Validate that a parish catechist coordinator can complete their core weekly tasks 
without instruction, using only the app interface. Identify friction points before 
broader rollout.

## Test profile
**Who to recruit:** Parish catechist coordinator or DRE (Director of Religious Education)  
**Technical level:** Comfortable with WhatsApp and M-Pesa. May never have used a 
web dashboard.  
**Language:** Conduct in English or Kiswahili — follow the participant's preference.  
**Duration:** 45–60 minutes  
**Location:** On their phone (mobile-first) or laptop if available

---

## Before the session

1. Open `catholicparishsteward.streamlit.app` on a device the participant will use
2. Navigate to **Catechists** page — confirm demo data is visible
3. Have a notebook ready — write down exact words they say, not interpretations
4. Do NOT explain what the app does. Let them discover it.
5. Start with this framing only:

> *"This is a tool being built for parish coordinators. I want to understand 
> what's easy and what's confusing — there are no wrong answers. 
> If something doesn't make sense, that's the app's problem, not yours."*

---

## Tasks (give one at a time — do not help unless stuck for >2 minutes)

### Task 1 — Find information (3 min)
> *"You want to know which catechists have their certification renewal coming up 
> in the next 3 months. Can you find that?"*

**Watch for:** Can they find the Catechists page? Do they understand the renewal 
date column? Do they try to filter or sort?

**Success:** They identify at least one renewal-due catechist  
**Failure signal:** They can't find the page, or find it but can't interpret the data

---

### Task 2 — Add a record (5 min)
> *"A new catechist just finished her Basic certification — her name is 
> [use a local name they suggest]. Can you add her to the register?"*

**Watch for:** Do they find the "Add" button? Is the form clear? Do they know 
what "Ministry Area" means? Do they notice the save confirmation?

**Success:** Record added and saved  
**Failure signal:** Form confusion, or they save but aren't sure it worked

---

### Task 3 — Log a training session (5 min)
> *"That same catechist just attended a 4-hour training day last Saturday. 
> Can you record that?"*

**Watch for:** Do they know where the Training Log is? (Tab 3 on Catechists page)  
Do they understand "hours" vs "sessions"?

**Success:** Training entry logged  
**Failure signal:** They look for it in the wrong place entirely

---

### Task 4 — Check today's reading (2 min)
> *"You're preparing for tomorrow's catechism class. Where would you find 
> today's scripture reading?"*

**Watch for:** Do they find Daily Prayers? Do they understand the liturgical 
season display?

**Success:** They reach the Daily Prayers page and see the reading  
**Failure signal:** They don't understand the sidebar navigation

---

### Task 5 — Open-ended exploration (10 min)
> *"Take a few minutes to explore anything else that looks useful for your work."*

**Watch for:** What do they click first? What do they ignore? What do they ask 
about? What do they try to do that the app doesn't support?

---

## Post-session questions (ask verbally, write answers)

1. **"What was the most useful thing you saw?"**
2. **"What was confusing or missing?"**
3. **"Would you use this instead of your current system? Why or why not?"**
4. **"What do you currently use to track catechists?"** *(exercise book? WhatsApp group? nothing?)*
5. **"If a bishop asked you to describe this tool in one sentence, what would you say?"**
6. **"What would make you tell another catechist coordinator about this?"**

---

## What to capture

After the session, fill in:

| Question | Answer |
|---|---|
| What was their current system? | |
| Time to complete Task 1 | |
| Time to complete Task 2 | |
| Did they notice save indicators? | Y / N |
| Did they understand liturgical season? | Y / N |
| Top friction point (their words) | |
| Top praise (their words) | |
| Feature they asked for that doesn't exist | |
| Would they use it? (1–5) | |

---

## Red flags that require immediate fixes before broader rollout

- Can't find Catechists page from homepage
- "Add Catechist" form fields are confusing
- Doesn't trust that data was saved
- Can't navigate back after going deep into a page
- Mobile display is broken

---

## Green lights for broader rollout

- Completes Tasks 1–3 without help
- Spontaneously says "this is better than [current method]"
- Asks "can I share this with my parish priest?"
- Understands what the USSD code is for

