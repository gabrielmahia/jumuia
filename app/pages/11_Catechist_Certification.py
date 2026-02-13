"""
Catechist Certification - Catholic Spiritual OS

Track and manage catechist formation, certification, and renewal.

Supports diocesan-level certification standards for lay catechists
teaching faith formation in parishes.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.spiritual_os.domain.catechist import (
    CatechistCertification,
    CertificationLevel,
    CertificationStatus,
    CourseCategory,
    BASIC_CERT_REQUIREMENTS,
    MASTER_CERT_REQUIREMENTS,
    DEMO_CATECHIST
)

# Page config
st.set_page_config(
    page_title="Catechist Certification | Catholic Spiritual OS",
    page_icon="✝️",
    layout="wide"
)

# Data mode indicator
st.info("📊 **Data Mode**: DEMO — Sample catechist data for demonstration", icon="ℹ️")

st.title("📚 Catechist Certification")

st.markdown("""
Track formation and certification for lay catechists serving in parish faith formation programs.

**Catechists** are lay ministers who teach the Catholic faith in religious education, sacramental preparation, 
RCIA, and other formation settings. Most dioceses require certification to ensure quality catechesis.
""")

# ============================================================================
# PARISH CATECHIST OVERVIEW
# ============================================================================

st.header("Parish Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Active Catechists",
        value="12"
    )

with col2:
    st.metric(
        label="Fully Certified",
        value="10",
        delta="83%"
    )

with col3:
    st.metric(
        label="In Progress",
        value="2"
    )

with col4:
    st.metric(
        label="Renewal Due (6 mo)",
        value="3"
    )

st.divider()

# ============================================================================
# INDIVIDUAL CATECHIST PROFILE
# ============================================================================

st.header(f"Catechist Profile: {DEMO_CATECHIST.name}")

# Status badge
status_colors = {
    CertificationStatus.ACTIVE: "🟢 Active",
    CertificationStatus.IN_PROGRESS: "🟡 In Progress",
    CertificationStatus.RENEWAL_DUE: "🟠 Renewal Due",
    CertificationStatus.EXPIRED: "🔴 Expired"
}

st.markdown(f"### {status_colors.get(DEMO_CATECHIST.status, DEMO_CATECHIST.status.value)}")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"""
    **Name**: {DEMO_CATECHIST.name}  
    **Email**: {DEMO_CATECHIST.email}  
    **Phone**: {DEMO_CATECHIST.phone}
    
    **Certification Level**: {DEMO_CATECHIST.level.value.capitalize()}  
    **Certificate #**: {DEMO_CATECHIST.current_certificate_number}  
    **Issue Date**: {DEMO_CATECHIST.issue_date.strftime('%B %d, %Y')}  
    **Expires**: {DEMO_CATECHIST.expiration_date.strftime('%B %d, %Y')}
    """)

with col2:
    st.markdown(f"""
    **Years Serving**: {DEMO_CATECHIST.years_serving}  
    **Languages**: {', '.join(DEMO_CATECHIST.languages_taught)}  
    **Specializations**: {', '.join(DEMO_CATECHIST.specializations)}
    """)

# Current assignments
st.markdown("### Current Teaching Assignments")
for assignment in DEMO_CATECHIST.current_assignments:
    st.write(f"- {assignment}")

st.divider()

# ============================================================================
# CERTIFICATION PROGRESS
# ============================================================================

st.header("Certification Requirements")

tab1, tab2, tab3 = st.tabs(["📊 Progress", "📖 Courses", "👁️ Observations"])

with tab1:
    st.markdown("### Formation Hours Completed")
    
    # Progress bar
    progress = min(DEMO_CATECHIST.total_formation_hours / BASIC_CERT_REQUIREMENTS.total_hours_required, 1.0)
    st.progress(progress)
    
    st.markdown(f"""
    **{DEMO_CATECHIST.total_formation_hours} / {BASIC_CERT_REQUIREMENTS.total_hours_required} hours completed** ({int(progress * 100)}%)
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Required Categories")
        st.write(f"✅ Sacred Scripture: {BASIC_CERT_REQUIREMENTS.scripture_hours}h")
        st.write(f"✅ Doctrine: {BASIC_CERT_REQUIREMENTS.doctrine_hours}h")
        st.write(f"⏳ Liturgy & Sacraments: {BASIC_CERT_REQUIREMENTS.liturgy_hours}h")
        st.write(f"⏳ Moral Teaching: {BASIC_CERT_REQUIREMENTS.moral_teaching_hours}h")
        st.write(f"⏳ Social Teaching: {BASIC_CERT_REQUIREMENTS.social_teaching_hours}h")
        st.write(f"⏳ Catechetical Methods: {BASIC_CERT_REQUIREMENTS.methods_hours}h")
    
    with col2:
        st.markdown("#### Safety & Formation")
        
        if DEMO_CATECHIST.background_check_date:
            st.write(f"✅ Background Check ({DEMO_CATECHIST.background_check_status})")
        else:
            st.write("❌ Background Check: Required")
        
        if DEMO_CATECHIST.safe_environment_training_date:
            st.write("✅ Safe Environment Training")
        else:
            st.write("❌ Safe Environment Training: Required")
        
        if DEMO_CATECHIST.mandated_reporter_training_date:
            st.write("✅ Mandated Reporter Training")
        else:
            st.write("❌ Mandated Reporter Training: Required")
        
        st.write(f"✅ Spiritual Formation: {DEMO_CATECHIST.spiritual_formation_hours}h / {BASIC_CERT_REQUIREMENTS.spiritual_formation_hours}h")

with tab2:
    st.markdown("### Courses Completed")
    
    for course in DEMO_CATECHIST.courses_completed:
        with st.expander(f"{course.title} ({course.hours}h)"):
            st.markdown(f"""
            **Category**: {course.category.value.replace('_', ' ').title()}  
            **Provider**: {course.provider}  
            **Date Completed**: {course.date_completed.strftime('%B %d, %Y')}  
            **Instructor**: {course.instructor}  
            **Certificate #**: {course.certificate_number}
            """)
            if course.notes:
                st.info(f"**Notes**: {course.notes}")

with tab3:
    st.markdown("### Classroom Observations")
    
    for obs in DEMO_CATECHIST.observations_completed:
        with st.expander(f"{obs.observation_date.strftime('%B %d, %Y')} - {obs.class_observed}"):
            st.markdown(f"""
            **Observer**: {obs.observer_name}  
            **Role**: {obs.observer_role}  
            **Overall Rating**: {obs.overall_rating}
            """)
            
            st.markdown("**Strengths Noted**:")
            for strength in obs.strengths_noted:
                st.write(f"- {strength}")
            
            st.markdown("**Areas for Growth**:")
            for area in obs.areas_for_growth:
                st.write(f"- {area}")
            
            st.info(f"**Recommendations**: {obs.recommendations}")

st.divider()

# ============================================================================
# RENEWAL TRACKING
# ============================================================================

st.header("Renewal Requirements")

days_until_renewal = (DEMO_CATECHIST.expiration_date - datetime.now()).days

if days_until_renewal < 180:
    st.warning(f"⚠️ Renewal due in {days_until_renewal} days ({DEMO_CATECHIST.expiration_date.strftime('%B %d, %Y')})")
else:
    st.info(f"Next renewal: {DEMO_CATECHIST.expiration_date.strftime('%B %d, %Y')} ({days_until_renewal} days)")

renewal_progress = min(DEMO_CATECHIST.renewal_hours_completed / DEMO_CATECHIST.renewal_hours_required, 1.0)
st.progress(renewal_progress)

st.markdown(f"""
**{DEMO_CATECHIST.renewal_hours_completed} / {DEMO_CATECHIST.renewal_hours_required} renewal hours completed** ({int(renewal_progress * 100)}%)
""")

st.markdown("""
### Renewal Options
- Diocesan workshops and conferences
- Approved online courses (Franciscan University, Catholic Distance University, etc.)
- Scripture study programs
- Catechetical methodology courses
- Spiritual retreats (limited hours apply)
""")

st.divider()

# ============================================================================
# CERTIFICATION REQUIREMENTS GUIDE
# ============================================================================

st.header("Certification Requirements Guide")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Basic Certification")
    st.markdown(f"""
    **Total Hours**: {BASIC_CERT_REQUIREMENTS.total_hours_required}  
    **Timeline**: Complete within first 2 years of service  
    **Renewal**: Every {BASIC_CERT_REQUIREMENTS.renewal_cycle_years} years ({BASIC_CERT_REQUIREMENTS.renewal_hours_per_cycle}h)
    
    **Course Requirements**:
    - Sacred Scripture: {BASIC_CERT_REQUIREMENTS.scripture_hours}h
    - Catholic Doctrine: {BASIC_CERT_REQUIREMENTS.doctrine_hours}h
    - Liturgy & Sacraments: {BASIC_CERT_REQUIREMENTS.liturgy_hours}h
    - Moral Teaching: {BASIC_CERT_REQUIREMENTS.moral_teaching_hours}h
    - Social Teaching: {BASIC_CERT_REQUIREMENTS.social_teaching_hours}h
    - Catechetical Methods: {BASIC_CERT_REQUIREMENTS.methods_hours}h
    - Spiritual Formation: {BASIC_CERT_REQUIREMENTS.spiritual_formation_hours}h
    
    **Practical Requirements**:
    - Classroom observations: {BASIC_CERT_REQUIREMENTS.observation_count_required} ({BASIC_CERT_REQUIREMENTS.observation_hours_required}h)
    - Background check (required)
    - Safe environment training (required)
    - Mandated reporter training (required)
    """)

with col2:
    st.markdown("### Master Certification")
    st.markdown(f"""
    **Total Hours**: {MASTER_CERT_REQUIREMENTS.total_hours_required}  
    **Eligibility**: Experienced catechists, DREs, principals  
    **Renewal**: Every {MASTER_CERT_REQUIREMENTS.renewal_cycle_years} years ({MASTER_CERT_REQUIREMENTS.renewal_hours_per_cycle}h)
    
    **Advanced Requirements**:
    - Deep Scripture study: {MASTER_CERT_REQUIREMENTS.scripture_hours}h
    - Advanced doctrine: {MASTER_CERT_REQUIREMENTS.doctrine_hours}h
    - Liturgical theology: {MASTER_CERT_REQUIREMENTS.liturgy_hours}h
    - Moral & social teaching: {MASTER_CERT_REQUIREMENTS.moral_teaching_hours + MASTER_CERT_REQUIREMENTS.social_teaching_hours}h
    - Advanced methodology: {MASTER_CERT_REQUIREMENTS.methods_hours}h
    - Spiritual formation: {MASTER_CERT_REQUIREMENTS.spiritual_formation_hours}h
    
    **Mentorship Role**:
    - Observe and mentor Basic catechists
    - {MASTER_CERT_REQUIREMENTS.observation_count_required} observations required ({MASTER_CERT_REQUIREMENTS.observation_hours_required}h)
    """)

st.divider()

# ============================================================================
# RESOURCES
# ============================================================================

st.header("Formation Resources")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Approved Course Providers")
    st.markdown("""
    **Online Programs**:
    - Catholic Distance University
    - Franciscan University Catechetical Institute
    - Loyola Press Catechetical Formation Series
    - Echoes of Faith (RCL Benziger)
    
    **Diocesan Programs**:
    - Archdiocese of Nairobi Office of Catechesis
    - AMECEA Pastoral Institute (Gaba, Uganda)
    - Catholic University of Eastern Africa
    """)

with col2:
    st.markdown("### Catechetical Resources")
    st.markdown("""
    **Key Documents**:
    - Catechism of the Catholic Church
    - General Directory for Catechesis
    - National Directory for Catechesis
    
    **Methodology**:
    - Catechesis of the Good Shepherd
    - Montessori-based approaches
    - Lectio Divina methods
    - Age-appropriate pedagogy
    """)

st.markdown("---")
st.caption("Catholic Spiritual OS | [GitHub](https://github.com/gabrielmahia/catholic-network-tools) | CC BY-NC-ND 4.0")
