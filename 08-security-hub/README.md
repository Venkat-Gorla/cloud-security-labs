# Security Hub

## Problem

AWS environments can have security issues across many AWS services and resources. Security teams need a centralized way to identify security findings, assess their severity, and determine where remediation should be focused.

## Goal

Demonstrate programmatically, using Python, the AWS SDK, and Pandas, how AWS Security Hub findings can be transformed into meaningful security-prioritization insights.

Validate the core Security Hub analysis using a custom pytest-like console program with representative in-memory DataFrames.

## Architecture

```text
AWS Security Hub
       │
       │ Findings
       ▼
Python / AWS SDK
       │
       │ Pandas DataFrame
       ▼
Pandas Analysis
       │
       ├── Severity Analysis
       ├── Control Prioritization
       ├── Resource Aggregation
       └── Finding Concentration
       │
       ▼
Security Insights
       │
       │ Prioritize remediation
       ▼
Security Action
```

## Success Criteria

| Check                                      | Status |
| ------------------------------------------ | :----: |
| Security Hub status inspected              |   ✅   |
| Security findings analyzed and prioritized |   ✅   |
| Resource-level insights identified         |   ✅   |
| Finding concentration analyzed             |   ✅   |
| Core analysis validated                    |   ✅   |

## Key Observations

- Pandas makes it practical to move beyond raw Security Hub findings and analyze security data from multiple perspectives.
- Resource-level analysis can reveal where findings are concentrated.
- Finding volume alone is not sufficient for prioritization; combining finding volume with severity provides a more useful remediation view.

## Takeaway

**AWS Security Hub provides the security findings; Pandas helps turn those findings into actionable prioritization insights.**
