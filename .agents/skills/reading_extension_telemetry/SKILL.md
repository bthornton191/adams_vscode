# Adams VS Code Extension Telemetry API

Use this skill when a coding agent needs to investigate errors, diagnose user-reported bugs, or understand failure patterns in the VS Code extension telemetry dashboard.

## API Endpoints

All endpoints accept optional `start` and `end` query params (ISO-8601 date strings) to scope the date window.

### 1. Primary: Global Error Summary

```
GET /api/events/errors/summary
```

Returns every unique error message across **all** event types, enriched with affected versions, users, and event names.

```json
[
  {
    "message": "Cannot read properties of undefined (reading 'document')",
    "count": 47,
    "last_seen": "2026-05-28T14:32:00+00:00",
    "user_count": 3,
    "versions": ["2.0.6", "2.0.7"],
    "affected_users": ["user_alpha", "user_beta"],
    "event_names": ["cmd_completion_provider", "UnhandledError"]
  }
]
```

This is the **best single endpoint** for an agent to call first — it gives a complete picture of every error, its frequency, which users/versions are affected, and which extension features it appeared in.

### 2. Per-Event Error Detail

```
GET /api/events/{event_name}/errors
```

Same schema as above, scoped to a single event type. Event names are auto-resolved — pass any name (aliased, prefixed, or raw) and the backend normalises it.

### 3. Overall Health

```
GET /api/stats/summary
```

Quick pulse: active users (7d/24h), total events, last sync time.

```json
{
  "all_time_users": 12,
  "active_7d": 8,
  "active_24h": 3,
  "new_24h": 0,
  "total_events": 18420,
  "last_sync": "2026-05-29T10:00:00+00:00"
}
```

### 4. Version Distribution

```
GET /api/stats/versions
```

Which extension versions users are running (semver-sorted, newest first). Correlate with error versions from the summary to see if a specific version rollout introduced errors.

```json
[
  { "version": "2.0.7", "user_count": 5, "pct": 41.7 },
  { "version": "2.0.6", "user_count": 3, "pct": 25.0 }
]
```

### 5. Event Properties (context around errors)

```
GET /api/events/{event_name}/properties
```

Returns string property distributions and numeric stats for a specific event. Useful when the agent needs to understand the **context** in which errors occur (e.g. "which file types were being edited", "was LSP enabled").

### 6. User Profile

```
GET /api/users/{username}
```

Returns a user's top events, daily activity, and current version. Useful when `affected_users` from the error summary points to a specific pattern.

## Error Schema (key fields)

Errors come from two possible `raw_json` keys (checked in order, first wins):
- `error_message` — structured error property set by the extension
- `error` — fallback key

Errors are extracted via `_parse_raw_json_errors()` in `backend/app/routers/events.py` — a single table scan of the `raw_json` column, no JOINs.

## Agent workflow recommendation

1. Call `GET /api/events/errors/summary` — get all unique errors with versions, users, event types
2. If a specific error stands out, call `GET /api/events/{event_name}/errors` for that event type to see per-event breakdown
3. Call `GET /api/stats/versions` to cross-reference: "is this error on a recently-released version?"
4. Call `GET /api/stats/summary` for overall health context (active users, sync status)
5. Optionally, call `GET /api/users/{username}` for a specific affected user's full profile and activity
