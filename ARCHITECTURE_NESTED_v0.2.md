"""
CATHOLIC SPIRITUAL OS - NESTED ARCHITECTURE GUIDE
Single app, 5 permission-based lenses, one database
"""

# ============================================================================
# ARCHITECTURAL OVERVIEW
# ============================================================================

"""
Catholic Spiritual OS v0.2 (Nested Architecture)

CONCEPT:
A single Streamlit application with five permission-based "lenses"
that allow users at different organizational levels to zoom in/out
like Google Maps, viewing different levels of aggregated data.

LENSES:
┌─────────────────────────────────────────────────────────┐
│ 🧑 Personal (You)                                        │
│    • Your private data only                             │
│    • Rule of Life, Journal, Sacraments                  │
│    • Can peek at parish aggregates (if opt-in)          │
│    • Can share with spiritual director                  │
│                                                          │
│ 🏛️ Parish (Your Community)                              │
│    • Aggregated member statistics (never individual)    │
│    • Operations: bulletin, events, volunteers           │
│    • See parish trends (formation, justice, growth)     │
│    • Coordinator level: Edit content, manage events     │
│                                                          │
│ ⛪ Diocese (Leadership)                                 │
│    • Aggregated parish statistics (50 parishes)         │
│    • Strategic planning dashboard                       │
│    • Justice campaign coordination (12 active)          │
│    • Transparency report (public-facing)                │
│    • Bishop level: Edit strategic priorities            │
│                                                          │
│ 🌍 Global (Justice Network)                             │
│    • Campaign aggregates (250 parishes, 26K workers)    │
│    • Cross-diocesan coordination (47 dioceses)          │
│    • Top diocese leaderboard, impact tracking           │
│    • Global coordinator level: Coordinate globally      │
│                                                          │
│ 🚨 Crisis (Emergency Response)                          │
│    • Temporary coordination during disasters            │
│    • Volunteer mobilization, resource matching          │
│    • Auto-purges after 90 days (privacy by design)      │
│    • Crisis responder level: Activate emergency mode    │
└─────────────────────────────────────────────────────────┘

KEY PRINCIPLE: Privacy by Design
- Individuals control their data visibility
- Aggregation happens automatically at each level
- Users can only see UP the hierarchy, never DOWN
- Opt-in at each level

# ============================================================================
# DATA FLOW ARCHITECTURE
# ============================================================================

INDIVIDUAL LAYER (private):
  user_001: {
    rule_of_life: [{name: "Morning prayer", duration: 15, ...}],
    journal_entries: [{...}],
    sacrament_milestones: [{...}],
    opt_in_to_parish_aggregates: true,
  }

  (John volunteers: 1 person)
  (John does Rule of Life: 1 person, 15 min average)
  (John gave $50 to justice: $50)

        ↓↓↓ AGGREGATED (if opted-in)

PARISH LAYER (aggregated):
  st_marys_parish: {
    aggregated_members_count: 487,
    aggregated_formation_participants: 342,
    aggregated_avg_practice_minutes: 23.0,  ← computed from all members
    aggregated_volunteer_count: 45,
    aggregated_justice_campaigns: ["living_wage"],
  }

  (Individual John never visible here)
  (Only statistics visible)
  (Diocese can only see these aggregates, not individual parishes)

        ↓↓↓ AGGREGATED (if opted-in)

DIOCESE LAYER (aggregated):
  diocese_springfield: {
    aggregated_parishes_count: 50,
    aggregated_total_catholics: 98000,
    aggregated_weekly_attendance: 34000,
    aggregated_formation_participants: 16800,
    aggregated_workers_helped: 26000,  ← from 12 campaigns
    aggregated_policy_wins: 3,
  }

  (Individual parishes never visible here)
  (Only diocese-level aggregates visible)
  (Global coordinator can only see these aggregates)

        ↓↓↓ AGGREGATED (if opted-in)

GLOBAL LAYER (aggregated):
  living_wage_campaign: {
    dioceses_joined: ["diocese_kenya", "diocese_uganda"],
    parishes_joined_count: 250,
    aggregated_workers_affected: 26000,  ← sum across all dioceses
    aggregated_wage_increase_percent: 26.0,
    aggregated_income_increase_dollars: 45000000,
    aggregated_policy_wins: 3,
  }

  (Individual dioceses/parishes/people never visible)
  (Only campaign-level aggregates visible)

# ============================================================================
# PERMISSION MATRIX
# ============================================================================

WHO CAN SEE WHAT:

INDIVIDUAL (John Smith)
├─ Sees: Own personal data only
├─ Can access: Personal lens
├─ Can peek: Parish aggregates (if opted-in to sharing)
├─ Sees: "342 people in Rule of Life at St. Mary's, 23 min avg"
├─ Does NOT see: Any other individual's data
├─ Does NOT see: Parish-level details
└─ Actions: Create Rule of Life, journal, share with director

PARISH COORDINATOR (Sarah Johnson, St. Mary's)
├─ Sees: St. Mary's aggregated member statistics
├─ Can access: Personal lens, Parish lens
├─ Can edit: Bulletin, events, volunteer assignments
├─ Sees: "342 members, +8% growth, 45 volunteers available"
├─ Does NOT see: Individual member's practices/journals
├─ Does NOT see: Other parishes' data
├─ Does NOT see: Diocese-level data directly
└─ Actions: Update bulletin, create events, coordinate volunteers

DIOCESAN LEADER (Bishop Michael, Diocese of Springfield)
├─ Sees: 50 parishes' aggregated statistics
├─ Can access: Personal, Parish (aggregates), Diocese, Global
├─ Can edit: Diocesan strategic priorities, transparency report
├─ Sees: "50 parishes, 98K Catholics, 16.8K in formation, +12% YoY"
├─ Does NOT see: Individual parish data
├─ Does NOT see: Individual parishioner data
├─ Does NOT see: Other dioceses' data
└─ Actions: Update strategic plan, activate justice campaigns, report

GLOBAL COORDINATOR (Global Justice Lead)
├─ Sees: Campaign-level aggregates worldwide
├─ Can access: All lenses (all aggregates)
├─ Can edit: Campaign descriptions, coordinate globally
├─ Sees: "250 parishes on living wage, 26K workers, +26% impact"
├─ Does NOT see: Individual parishes, dioceses, parishioners
├─ Does NOT see: Any non-aggregated data
└─ Actions: Coordinate campaigns, analyze trends, celebrate wins

CRISIS RESPONDER (Emergency Coordinator)
├─ Sees: Temporary crisis data only
├─ Can access: Crisis lens
├─ Can edit: Volunteer assignments, resource allocation
├─ Sees: "2100 volunteers, 45K people aided, $2.1M raised"
├─ Data: Auto-purged 90 days after crisis
├─ Does NOT see: Individual personal data
└─ Actions: Mobilize volunteers, match resources, coordinate

# ============================================================================
# AUTHENTICATION FLOW
# ============================================================================

1. User visits app
2. Login screen shown (demo credentials available)
3. User logs in or creates account
4. Permission context created based on role
5. User redirected to their primary lens
6. Navigation buttons limited by permissions
7. All data queries filtered by permissions

DEMO ACCOUNTS:
- Individual: john@example.com / demo
- Parish Coordinator: sarah@example.com / demo
- Diocesan Leader: bishop@example.com / demo
- Global Coordinator: global@example.com / demo
- Crisis Responder: crisis@example.com / demo

# ============================================================================
# DATABASE SCHEMA
# ============================================================================

SQLITE TABLES:

users
  id, name, email, role, parish_id, diocese_id
  opt_in_to_parish_aggregates (boolean)
  opt_in_to_diocese_aggregates (boolean)
  opt_in_to_global_aggregates (boolean)
  privacy_level (0=only me, 1=director, 2=parish)
  rule_of_life (JSON)
  journal_entries (JSON)
  sacrament_milestones (JSON)
  created_at, updated_at

parishes
  id, name, diocese_id, coordinator_id
  bulletin_text, events (JSON), volunteer_signups (JSON)
  aggregated_members_count
  aggregated_formation_participants
  aggregated_avg_practice_minutes
  aggregated_sacrament_stats (JSON)
  aggregated_justice_campaigns (JSON)
  aggregated_volunteer_count
  created_at, updated_at

dioceses
  id, name, bishop_name, region
  transparency_priorities, strategic_plan
  aggregated_parishes_count
  aggregated_total_catholics
  aggregated_weekly_attendance
  aggregated_formation_participants
  aggregated_justice_campaigns (JSON)
  aggregated_workers_helped
  aggregated_policy_wins
  created_at, updated_at

justice_campaigns
  id, name, campaign_type
  dioceses_joined (JSON), parishes_joined_count
  aggregated_workers_affected
  aggregated_wage_increase_percent
  aggregated_income_increase_dollars
  aggregated_policy_wins
  success_stories (JSON)
  created_at, updated_at

crisis_events (temporary)
  id, name, event_type, location
  affected_dioceses, activated_parishes (JSON)
  volunteers, resources, needs (JSON)
  people_affected, people_receiving_aid, total_funds_raised
  auto_delete_date (90 days post-crisis)
  created_at, updated_at

# ============================================================================
# MODULE RESPONSIBILITIES
# ============================================================================

models.py
├─ User: Individual with private data
├─ Parish: Aggregated parish statistics
├─ Diocese: Aggregated diocese statistics
├─ JusticeCampaign: Campaign-level aggregates
├─ CrisisEvent: Temporary crisis data
├─ UserRole: Enum of roles
├─ PermissionContext: Who can see what
└─ Purpose: Data structures and access control logic

aggregation.py
├─ AggregationEngine: Compute aggregates from detail data
│   ├─ aggregate_parish_from_users()
│   ├─ aggregate_diocese_from_parishes()
│   └─ aggregate_campaign_impact()
├─ QueryBuilder: Permission-aware data queries
│   ├─ get_visible_users()
│   ├─ get_visible_parishes()
│   ├─ get_visible_dioceses()
│   └─ get_visible_campaigns()
└─ Purpose: Keep aggregates in sync, filter by permissions

database.py
├─ Database class: SQLite persistence
│   ├─ init_schema(): Create tables
│   ├─ save_user(), get_user()
│   ├─ save_parish(), get_parish()
│   ├─ get_users_in_parish()
│   └─ cleanup_expired_crises()
└─ Purpose: Durable storage, automatic cleanup

forms.py
├─ PersonalForms: Rule of Life, journal, sacraments
├─ ParishForms: Bulletin, events, volunteers
├─ DioceseForums: Transparency, strategic plan
├─ CrisisForms: Volunteers, resources, needs
└─ Purpose: Streamlit forms for data input

visualizations.py
├─ Visualizations: Charts and metrics
├─ Reports: Render reports as text/markdown
├─ Exports: Generate downloadable files
└─ Purpose: Data presentation and sharing

auth.py
├─ Authentication: Login, registration, password hashing
├─ PermissionManager: Access control matrix
└─ Purpose: User auth and permission enforcement

app.py
├─ Main Streamlit app
├─ 5 lenses (personal, parish, diocese, global, crisis)
├─ Sidebar navigation
├─ Login screen
└─ Purpose: User interface and orchestration

# ============================================================================
# DEPLOYMENT CHECKLIST
# ============================================================================

BEFORE DEPLOYMENT:
- [ ] All modules import without errors
- [ ] Database schema creates successfully
- [ ] Demo accounts work for all 5 roles
- [ ] All 5 lenses render without errors
- [ ] Permissions work correctly (tested with each role)
- [ ] Aggregation computes correctly
- [ ] Forms save and load data
- [ ] Reports generate correctly
- [ ] Auth system functional
- [ ] Privacy checks working

DEPLOYMENT:
- [ ] Push to GitHub: main branch
- [ ] Go to https://share.streamlit.io/new
- [ ] Select repo: gabrielmahia/catholic-network-tools
- [ ] Branch: main
- [ ] Main file: app.py
- [ ] Deploy

POST-DEPLOYMENT:
- [ ] Test login with each demo account
- [ ] Test each lens navigation
- [ ] Create test data at each level
- [ ] Verify aggregation works
- [ ] Test permission boundaries
- [ ] Monitor logs for errors
- [ ] Get user feedback

# ============================================================================
# FUTURE ENHANCEMENTS
# ============================================================================

v0.3:
- Real-time data sync (WebSocket)
- Mobile app (React Native)
- Advanced analytics (dashboards, trends)

v0.4:
- Multi-language support
- Regional customization
- API for third-party integration

v1.0:
- Enterprise features (SSO, audit logs)
- Advanced reporting
- Geographic mapping

v2.0:
- Blockchain for transparency
- Decentralized federation
- IoT integration (crisis response)
"""
