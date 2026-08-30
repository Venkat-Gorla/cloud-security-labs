# IAM Access Analyzer External Access

## Problem

AWS resources can unintentionally expose data or actions outside an account's intended trust boundary. Architects need visibility into external access and a way to determine whether that access is intentional or requires remediation.

## Goal

Demonstrate programmatically, using Python and the AWS SDK, how IAM Access Analyzer identifies external access to AWS resources, reports a finding, and supports architectural evaluation of that access.

## Architecture

```text
AWS Resource
    │
    │ Resource Policy
    ▼
IAM Access Analyzer
    │
    │ Access Finding
    ▼
External Access
    │
    │ Architectural Evaluation
    ▼
Accept / Remediate / Redesign
```

## Success Criteria

| Check                                         | Status |
| --------------------------------------------- | :----: |
| External access finding identified            |   ✅   |
| Underlying resource configuration inspected   |   ✅   |
| Access determined to be intentional           |   ✅   |
| Potential architecture improvement identified |   ✅   |

## Key Observations

- External access is not necessarily a security issue; it must be evaluated against the intended architecture.
- Existing resources can reveal security exposure that may otherwise remain unnoticed.

## Future Work

Evaluate serving the S3 static client through Amazon CloudFront while restricting direct access to the S3 bucket.
