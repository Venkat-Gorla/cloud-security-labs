# AWS STS AssumeRole POC

## Problem

Applications running outside AWS often rely on long-lived IAM user credentials. A more secure approach is to obtain temporary credentials by assuming an IAM role.

## Goal

Demonstrate how an IAM user assumes an IAM role through AWS STS to obtain temporary credentials and access AWS services.

## Architecture

```text
IAM User
    │
    │ AssumeRole
    ▼
AWS STS
    │
    │ Temporary Credentials
    ▼
Assumed Role
    │
    ▼
Amazon S3
```

## Success Criteria

| Check                                                    | Status |
| -------------------------------------------------------- | :----: |
| IAM role created with appropriate trust relationship     |   ✅   |
| IAM user successfully assumes the role using AWS STS     |   ✅   |
| Caller identity changes from IAM User to Assumed Role    |   ✅   |
| Temporary credentials successfully access an AWS service |   ✅   |
