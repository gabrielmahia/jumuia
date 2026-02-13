# Catholic Network Tools — Architecture Design

---

## Core Design Principles

1. **Offline-first**: Works 7+ days disconnected; sync on reconnect without data loss
2. **CRDT-based**: Conflict Resolution-free Datatype for simultaneous edits
3. **Event-sourced**: Audit trail of every change; no data destruction
4. **Trust-native**: Parish data is sacred; never extracted for external use
5. **SMS-capable**: Works on dumb phones in low-connectivity zones (Marallal)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                         │
├─────────────────┬──────────────────┬──────────────────────┤
│  Web UI (Svelte)│  SMS Gateway     │  Mobile App (Offline) │
│  [Westlands]    │ [Marallal]       │  [Both]              │
└─────────────────┴──────────────────┴──────────────────────┘
                          ↓
         ┌─────────────────────────────────────┐
         │      FastAPI Server (Hub)           │
         │  - REST API                         │
         │  - WebSocket (real-time sync)       │
         │  - SMS webhook handler              │
         └─────────────────────────────────────┘
                          ↓
         ┌─────────────────────────────────────┐
         │   Sync Engine (Yjs + CRDT)          │
         │  - Offline-first reconciliation     │
         │  - Conflict resolution              │
         │  - Event log                        │
         └─────────────────────────────────────┘
                          ↓
      ┌──────────────────────────────────────┐
      │         Data Layer (SQLite/Postgres)  │
      ├──────────────────────────────────────┤
      │ Real Data | Demo Data | Event Log    │
      │ (Separated, encrypted, audited)      │
      └──────────────────────────────────────┘
```

---

## Data Layers

### Layer 1: Real Data (Audit-Protected)

**Stored Data:**
- Attendance records
- Donation/stewardship logs
- Volunteer assignments
- Sacramental records (baptism, marriage, funeral)
- Parish member profiles

**Properties:**
- Encrypted at rest (AES-256)
- TLS 1.3 in transit
- Audit trail (who, what, when, why)
- Accessible only to authorized parish staff
- Exportable at any time by parish

**Retention:**
- Kept indefinitely (per parish request)
- Can be deleted in bulk (with audit log)
- Backups encrypted and geographically separated

### Layer 2: Demo Data (Synthetic, Clearly Labeled)

**Example Data:**
- Sample parish: "St. Mary Westlands"
- Fake volunteers with synthetic names
- Test donations (100-1000 KES amounts)
- Mock events and schedules

**Properties:**
- Separated from real data (different database)
- Clearly marked "DEMO" in UI/exports
- Refreshes with each deployment
- Used only for training and testing

**Usage:**
- New coordinators learn the interface
- Developers test features
- UI demonstrations

### Layer 3: Event Log (Immutable)

**Events Logged:**
- Every data change (create, update, delete)
- User actions (login, export, access)
- Sync events (when conflict resolved)
- System events (backup, upgrade)

**Properties:**
- Immutable (write-once)
- Timestamped with millisecond precision
- Linked to user and parish context
- Queryable for compliance audits

---

## Offline-First Architecture

### When Online (Westlands Scenario)

```
┌──────────────┐
│ Local SQLite │ ← Editing
└──────────────┘
       ↓ (real-time sync via WebSocket)
┌──────────────┐
│ Server       │ ← Persisted
└──────────────┘
```

- Changes saved to local DB immediately
- Sync to server in background (every 30 seconds or on reconnect)
- If server unavailable, client queues changes

### When Offline (Marallal Scenario)

```
┌──────────────┐
│ Local SQLite │ ← Editing (7+ days possible)
└──────────────┘
   (No connection)
```

- All operations work locally
- No sync attempted
- Sync on reconnect (automatic)

### Conflict Resolution (Both Scenarios)

When reconnecting after offline edit + server change:

```
Local:   attendance[person_id=123] = "present"   [edit @ 2:15pm]
Server:  attendance[person_id=123] = "late"      [edit @ 2:00pm]

CRDT Algorithm:
- Each edit has timestamp + user ID
- Latest timestamp wins
- Result: "late" (server edit was earlier, but local was later)
- Both versions logged in audit trail

No data loss. Both edits visible in history.
```

**CRDT Implementation:**
- Yjs (Conflict-free Replicated Data Type)
- Operational Transformation fallback (simple text)
- Event sourcing ensures every change logged

---

## Module Structure

```
catholic-network-tools/
├── coordination/          # Attendance, events, scheduling
│   ├── attendance.py
│   ├── events.py
│   ├── volunteers.py
│   └── sync_engine.py
│
├── stewardship/          # Donations, finance, resources
│   ├── donations.py
│   ├── allocations.py
│   ├── financial_reports.py
│   └── audit_trail.py
│
├── resilience/           # Offline mode, SMS, backup
│   ├── offline_mode.py
│   ├── sms_handler.py
│   ├── sync_protocol.py
│   └── backup.py
│
├── formation/            # Sermons, teachings, records
│   ├── content_library.py
│   ├── sacramental.py
│   └── resources.py
│
├── accessibility/        # UI for low-connectivity zones
│   ├── sms_ui.py
│   ├── ussd.py
│   └── mobile_sync.py
│
├── api/                  # FastAPI endpoints
│   ├── auth.py
│   ├── routes/
│   ├── sync.py
│   └── webhooks.py
│
└── ui/                   # Web UI (Svelte)
    ├── pages/
    ├── components/
    └── stores/
```

---

## API Design

### REST Endpoints

```
GET    /api/parish/{id}              Get parish info
GET    /api/parish/{id}/attendance   List attendance
POST   /api/parish/{id}/attendance   Add attendance record
GET    /api/parish/{id}/donations    List donations
POST   /api/parish/{id}/donations    Add donation
GET    /api/parish/{id}/volunteers   List volunteers
POST   /api/parish/{id}/volunteers   Add volunteer
GET    /api/audit-log                Get audit trail
POST   /api/sync                     Sync offline changes
```

### WebSocket (Real-time Sync)

```
Client sends:
  { "action": "sync", "changes": [...], "last_sync": timestamp }

Server responds:
  { "status": "ok", "merged": {...}, "conflicts": [...] }
```

---

## Data Security

### Encryption

- **At rest**: SQLAlchemy + sqlalchemy_encrypted (AES-256)
- **In transit**: TLS 1.3 required
- **Keys**: Stored in environment variables (not in code)

### Access Control

- Parish admins can only see their own data
- Volunteers see only their own records
- API keys scoped to parish + read/write permissions
- All access logged

### Audit Trail

Every change includes:
- User ID (who made change)
- Timestamp (when)
- Change description (what)
- Reason/context (why)
- IP address (where)

---

## Sync Protocol

### Initial Sync (New Device/Offline Mode)

1. Client requests full dataset: `GET /api/parish/{id}/export`
2. Server sends encrypted snapshot (JSON + audit log)
3. Client imports locally, sets `last_sync` timestamp
4. Ready for offline operation

### Incremental Sync (Reconnect)

1. Client sends changes since `last_sync`: `POST /api/sync`
2. Server applies changes with CRDT resolution
3. Server sends server changes since `last_sync`
4. Client merges with CRDT, updates `last_sync`
5. Both sides in sync

### SMS Fallback (No Data Connection)

1. User sends SMS: `ATTEND +John +Present` to short code
2. SMS handler parses (regex-based)
3. Creates attendance event in local queue
4. On reconnect, queued events sync to server
5. No data loss

---

## Testing Strategy

### Unit Tests
- Individual functions (donation calc, sync logic)
- Edge cases (zero balance, simultaneous edits)

### Integration Tests
- End-to-end workflows (create event → add attendance → sync)
- Offline + online transitions

### Offline Tests
- Disconnect network, edit data, reconnect
- Verify no data loss, conflicts resolved

### SMS Tests
- Parse various SMS formats
- Verify SMS creates correct database changes

### Security Tests
- Encryption working (can't read raw DB)
- Access control enforced (user A can't see user B's data)
- Audit log complete (no missing changes)

---

## Deployment

### Single Parish (Marallal)

```bash
docker run --env-file .env \
  -v ./data:/app/data \
  -p 8000:8000 \
  catholic-network-tools:latest
```

### Diocese Hub (Nairobi)

```bash
helm install catholic-network-tools \
  --values diocesan-values.yaml \
  ./chart/
```

Includes:
- PostgreSQL (multi-tenant)
- Redis (caching + locks)
- SMS gateway (Africa's Talking)
- Backup to encrypted S3

---

## Performance Targets

- **Page load**: <2 seconds (even on 2G networks)
- **Offline query**: <100ms (local SQLite)
- **Sync**: <5 seconds for 1000 records over 3G
- **SMS parsing**: <30 seconds latency

---

## Known Limitations

1. **No real-time collaboration** — CRDT resolves conflicts but doesn't show simultaneous cursors
2. **No version history UI** — Audit log exists but not user-visible yet
3. **SMS is one-way** — SMS sends data in, but responses are email-based
4. **Sacramental records are simplified** — Doesn't replace official parish records

---

## Future Directions

1. **Swahili + Kikuyu UI** — Translate entire interface
2. **Mobile app** — React Native for offline-first phone app
3. **Blockchain audit** — Immutable log on-chain (optional)
4. **Integration with USSD** — Kenya's dumb-phone protocol
5. **Solar + offline mesh** — Work in zero-connectivity remote areas

