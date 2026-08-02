# AWS Account Inventory

## Problem

Understanding what resources exist in an AWS account is the foundation for security, governance, and cost optimization. Manual inventory through the AWS Console does not scale.

## Goal

Inventory AWS resources by classifying them as CloudFormation-managed or unmanaged and identifying their relationships.

## Architecture

```text
AWS Account
     │
     ├──────────────┐
     ▼              ▼
CloudFormation   AWS Services
     │              │
     ▼              ▼
Managed       Unmanaged
Resources      Resources
      \          /
       \        /
        ▼      ▼
    Account Inventory
```

## Success Criteria

| Outcome                                                  | Status |
| -------------------------------------------------------- | :----: |
| CloudFormation stacks are discovered                     |   ✅   |
| Managed resources are inventoried across stacks          |   ✅   |
| Unmanaged resources are identified                       |   ✅   |
| Managed resources can be traced to CloudFormation stacks |   ✅   |
