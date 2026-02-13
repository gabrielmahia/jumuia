"""
Catholic Network Tools — Administration & Coordination
Track schedules, volunteer assignments, facilities, compliance
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Administration", layout="wide")

st.title("📋 Administration & Coordination")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Masses/Week", "4", "Sun + weekday")
with col2:
    st.metric("Volunteers Scheduled", "23", "100% coverage")
with col3:
    st.metric("Facility Bookings", "45/month", "0 conflicts")
with col4:
    st.metric("Compliance Status", "100%", "✓ All current")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Mass Schedule", "Volunteer Assignments", "Facility Calendar", "Safety & Compliance", "Directory"])

with tab1:
    st.markdown("## Sunday Mass Schedule")
    
    schedule = pd.DataFrame({
        "Time": ["7:00 AM", "9:00 AM", "11:00 AM", "5:00 PM"],
        "Priest": ["Fr. Emmanuel", "Fr. Steve", "Fr. Emmanuel", "Deacon John"],
        "Reader": ["Tom", "Maria", "Grace", "David"],
        "Altar Server": ["Marcus (setup)", "Emma + James", "Samuel + Luke", "Isabella"],
        "Cantor": ["Sister Anne", "Youth choir (10)", "Adult choir (15)", "Tom (solo)"],
        "Est. Attendance": ["45", "120", "180", "65"],
        "Language": ["English/Swahili", "English", "English", "English/Spanish"]
    })
    st.dataframe(schedule, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Weekday Masses")
    
    weekday = pd.DataFrame({
        "Day": ["Monday-Friday", "Saturday (morning)"],
        "Time": ["6:30 AM", "8:00 AM"],
        "Priest": ["Rotating", "Fr. Emmanuel"],
        "Avg Attendance": ["12-18", "8-12"],
        "Notes": ["Before work", "No homily"]
    })
    st.dataframe(weekday, use_container_width=True)

with tab2:
    st.markdown("## Volunteer Assignment Schedule")
    
    st.markdown("### This Week's Volunteer Needs")
    
    volunteer_schedule = pd.DataFrame({
        "Role": ["Lectors (readers)", "Altar Servers", "Ushers", "Greeters", "Coffee Hour", "Nursery"],
        "Sun 7am": ["Tom", "Marcus", "Joseph", "Maria", "—", "Sister Anne"],
        "Sun 9am": ["Grace", "Emma/James", "David + Paul", "Rachel", "Agnes + Tom Jr", "Linda"],
        "Sun 11am": ["Samuel", "Samuel/Luke", "Robert + James", "Sofia", "Volunteers", "Patricia"],
        "Sun 5pm": ["Isabella", "Lucas", "Michael", "David Sr", "Youth group", "Grace"],
        "Status": ["✓ Full", "✓ Full", "✓ Full", "✓ Full", "✓ Full", "✓ Full"]
    })
    st.dataframe(volunteer_schedule, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Upcoming Volunteer Needs (Next Month)")
    
    needs = pd.DataFrame({
        "Role": ["Altar Servers", "Lectors", "Ushers (3 needed)", "Children's Liturgy Leaders"],
        "Currently Assigned": [4, 6, 5, 3],
        "Needed": [6, 8, 6, 4],
        "Gap": ["+2", "+2", "+1", "+1"],
        "Action": ["Recruit from youth", "Training scheduled", "Ask James to mentor", "Youth training next month"]
    })
    st.dataframe(needs, use_container_width=True)

with tab3:
    st.markdown("## Facility Calendar & Bookings")
    
    st.markdown("### Space Availability")
    
    facilities = pd.DataFrame({
        "Space": ["Main Church", "Parish Hall", "Classrooms (3)", "Office Space", "Parking Lot"],
        "Capacity": ["400", "150", "25-30 each", "Staff + clergy", "80 vehicles"],
        "Available Hours": ["6am-9pm", "9am-9pm Sat/Sun", "9am-6pm weekdays", "9am-5pm weekdays", "24/7"],
        "Status": ["Maintained", "Recently painted", "Wi-Fi + projectors", "Phones + computers", "Paved + lit"]
    })
    st.dataframe(facilities, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### This Month's Bookings (45 total)")
    
    bookings = pd.DataFrame({
        "Event": ["Youth Group Meetings", "Bible Studies", "Funerals/Memorials", "Wedding Rehearsals", "RCIA Classes", "Parish Events"],
        "Frequency": ["3x/month", "2x/month", "1-2/month", "2-3/month", "Weekly", "As scheduled"],
        "Space Used": ["Parish Hall", "Classrooms", "Church", "Church", "Classroom", "All"],
        "Avg Duration": ["2 hrs", "1.5 hrs", "2 hrs", "1.5 hrs", "1.5 hrs", "Varies"]
    })
    st.dataframe(bookings, use_container_width=True)

with tab4:
    st.markdown("## Safety & Compliance")
    
    st.markdown("### Annual Compliance Checklist")
    
    compliance = pd.DataFrame({
        "Area": [
            "Background Checks (volunteers)",
            "Safeguarding Training (all staff)",
            "Fire Safety Inspection",
            "Building Insurance",
            "Staff Certifications",
            "Ministry Health Screening"
        ],
        "Required By": ["Quarterly", "Annually", "Annually", "Monthly", "Varies", "Annually"],
        "Last Completed": ["Feb 10, 2024", "Jan 15, 2024", "Jan 20, 2024", "Feb 1, 2024", "Varies", "Feb 1, 2024"],
        "Next Due": ["May 10, 2024", "Jan 15, 2025", "Jan 20, 2025", "Mar 1, 2024", "Varies", "Feb 1, 2025"],
        "Status": ["✓", "✓", "✓", "✓", "✓", "✓"]
    })
    st.dataframe(compliance, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Emergency Preparedness")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Emergency Contacts (Updated Monthly)**
        - 🚑 Ambulance: 911
        - 🔥 Fire: 911
        - 👮 Police: 911
        - 🏥 Nearest Hospital: Mercy Hospital (5 min)
        - ⛪ Bishop on-call: [Number]
        
        **Defibrillator (AED) Locations**
        - Main church entrance
        - Parish hall
        - Office area
        
        **All staff trained (CPR/First Aid)**
        """)
    
    with col2:
        st.markdown("""
        **Evacuation Plan**
        - Meet at parking lot (north side)
        - Sound alarm if needed
        - Check-in roster at office
        - Report to fire marshal
        
        **Drills**
        - Fire drill: Quarterly
        - Weather event: Annually
        - Last fire drill: Jan 15, 2024
        
        **Safeguarding Protocols**
        - Never 1-on-1 with children
        - Always 2 adults in rooms
        - Report concerns to pastor
        """)

with tab5:
    st.markdown("## Directory & Contact List")
    
    st.markdown("### Staff & Leadership")
    
    staff = pd.DataFrame({
        "Role": ["Pastor", "Parochial Vicar", "Deacon", "Pastoral Associate", "DRE (Formation)", "Admin"],
        "Name": ["Fr. Emmanuel", "Fr. Steve", "Deacon John", "Sister Mary", "Agnes", "Tom"],
        "Email": ["fre@parish.org", "frs@parish.org", "dj@parish.org", "sm@parish.org", "dre@parish.org", "admin@parish.org"],
        "Phone": ["+254 701 1111", "+254 701 2222", "+254 701 3333", "+254 701 4444", "+254 701 5555", "+254 701 6666"]
    })
    st.dataframe(staff, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Ministry Coordinators")
    
    coordinators = pd.DataFrame({
        "Ministry": ["Justice & Advocacy", "Youth Formation", "Pastoral Care", "Liturgy", "Finance", "Building/Maintenance"],
        "Coordinator": ["Thomas", "Agnes", "Grace", "Fr. Emmanuel", "Paul (Finance Council Chair)", "Joseph"],
        "Contact": ["thomas@email.com", "agnes@email.com", "grace@email.com", "fre@parish.org", "paul@email.com", "joseph@email.com"],
        "Volunteers": ["8", "12", "6", "15", "7 council members", "4"]
    })
    st.dataframe(coordinators, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### How to Reach Us")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Main Office**
        - Phone: +254 701 0000
        - Hours: Mon-Fri 9am-5pm
        
        **Sacraments**
        - Contact: Fr. Emmanuel
        - Email: sacraments@parish.org
        
        **Emergency (After hours)**
        - Call: +254 701 1111 (Fr. Emmanuel cell)
        """)
    
    with col2:
        st.markdown("""
        **Website:** www.parishname.org
        **Email:** info@parish.org
        **Facebook:** /ParishName
        **WhatsApp:** Join our broadcast list
        
        **Newsletter**
        - Sent weekly on Wednesday
        - Includes Mass schedule, announcements, prayer intentions
        """)

st.markdown("---")

st.info("""
📋 **Good administration is invisible until it breaks down.**

When schedules work, when volunteers are clear on their roles, when the building is safe—parishioners just experience smooth parish life. 
They don't see the coordination that made it possible.

But when Father isn't notified of a funeral, when volunteers show up to conflicting assignments, when the building isn't maintained—
everything falls apart.

This tracking ensures the Church operates smoothly so **everyone can focus on what matters: mission.**
""")
