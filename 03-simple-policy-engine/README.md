# Simple Policy Engine POC

## Problem

Authorization rules embedded directly into application code become difficult to maintain, audit, and change as applications evolve.

## Goal

Demonstrate policy-based authorization by moving authorization decisions outside the application and into an external policy.

## Architecture

```
Request
   │
   ▼
Application
   │
   ▼
Policy Engine
   │
   ├── principals.json
   └── policy.json
   │
   ▼
ALLOW / DENY
   │
   ▼
Application Enforces Decision
```

## Success Criteria

| Check                                                             | Status |
| ----------------------------------------------------------------- | :----: |
| Application delegates authorization to the Policy Engine          |   ✅   |
| Policy stored outside application code                            |   ✅   |
| Authorization request evaluated successfully                      |   ✅   |
| Authorization behavior changes without modifying application code |   ✅   |
